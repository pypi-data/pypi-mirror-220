import abc
import datetime
import decimal
import enum
import re
from functools import partial
from typing import *
from uuid import UUID

from dateutil import parser
from kaiju_tools.exceptions import ValidationError


class FieldGroups(enum.Enum):
    """Attribute field group IDs."""

    BASE = 'Group.general'
    CONDITIONS = 'Group.validators'
    SEARCH = 'Group.search'
    LOOKUP = 'Group.lookup'


class NormalizationError(ValueError):
    """This exception class is used to track normalization problems. Use it
    in your onw normalizer."""


class _BaseFieldMeta(abc.ABCMeta):
    _name = None

    def __new__(mcs, name, superclasses, attr):
        new_cls = super().__new__(mcs, name, superclasses, attr)
        if abc.ABC not in new_cls.__bases__:
            if not new_cls._name:
                raise ValueError(f'{name}._name attribute must be set.')
        return new_cls

    @property
    def type(cls):
        return cls._name


class BaseField(abc.ABC, metaclass=_BaseFieldMeta):
    _name = None

    def __init__(
        self,
        required=False,
        default=None,
        disabled=False,
        is_system=False,
        group: str = None,
        read_only=False,
        grid_handler=None,
        normalizer: Callable = None,
        normalizer_es: Callable = None,
        validator: Callable = None,
        field_validator: Callable = None,
        dependence: list = None,
        nested=None,
        label: str = None,
        label_key: str = None,
        helper_text: str = None,
        helper_key: str = None,
        view_condition: dict = None
    ):
        """
        :param required:
        :param default:
        :param disabled:
        :param read_only:
        :param grid_handler:
        :param group: attribute parameter group, default is base
        :param normalizer: custom normalizer function
        :param validator: custom validation function
        :param dependence: dependence of fields
        :param field_validator: custom validation function for field parameter
        :param normalizer_es:
        :param label:
        :param nested:
        :param label_key:
        :param helper_text:
        :param helper_key:
        """

        if group is None:
            self.group = FieldGroups.BASE.value
        elif isinstance(group, enum.Enum):
            self.group = group.value
        else:
            self.group = str(group)

        self.required = required
        self.dependence = dependence
        self.is_system = is_system
        self.default = default
        self.disabled = disabled
        self.read_only = read_only
        self.grid_handler = grid_handler
        self.nested = nested
        self.label = label
        self.label_key = label_key
        self.helper_key = helper_key
        self.helper_text = helper_text
        self.view_condition = view_condition

        # normalizer settings

        if normalizer:
            if not callable(normalizer):
                raise TypeError('Normalizer "%s" must be callable.' % normalizer)
            self.normalize = normalizer

        if normalizer_es:
            if not callable(normalizer_es):
                raise TypeError('Normalizer "%s" must be callable.' % normalizer_es)
            self.normalize_es = normalizer_es

        # validator settings

        if validator:
            if not callable(validator):
                raise TypeError('Validator "%s" must be callable.' % validator)
            self.validate = validator

        if field_validator:
            if not callable(field_validator):
                raise TypeError('Validator "%s" must be callable.' % field_validator)
            self.field_validator = field_validator

    def processing(self):
        pass

    def __iter__(self):
        return iter(self.repr().items())

    def repr(self):
        return {
            'default': self.default,
            'disabled': self.disabled,
            'kind': self._name,
            'required': self.required,
            'dependence': self.dependence,
            'label': self.label,
            'label_key': self.label_key,
            'view_condition': self.view_condition,
            'helper_key': self.helper_key,
            'helper_text': self.helper_text,
        }

    @property
    def type(self):
        return self._name

    @staticmethod
    def compare(val1, val2):
        return val1 == val2


class RegExp:
    __slots__ = ('pattern', 'compiled', 'msg', '_repr')

    def __init__(self, pattern: str, msg: str = None):
        self.pattern = pattern
        self.compiled = re.compile(pattern)
        self.msg = msg
        self._repr = {
            'pattern': self.pattern,
            'msg': self.msg,
        }

    def __iter__(self):
        return iter(self.repr().items())

    def repr(self):
        return self._repr


class StringField(BaseField):
    _name = 'string'

    def __init__(self, *args, regex=None, behavior=None, field_type=None, min: int = None, max: int = None,
                 **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self.behavior = behavior
        self.field_type = field_type  # 'password', 'email'
        self.min = min
        self.max = max
        if regex:
            self.regex = RegExp(*regex)
        else:
            self.regex = None

    def repr(self):
        _r = super(StringField, self).repr()
        _r.update({
            'min': self.min,
            'max': self.max,
        })

        if self.regex:
            _r['regex'] = self.regex.repr()

        _r['behavior'] = self.behavior

        if self.field_type:
            _r['field_type'] = self.field_type

        return _r

    @staticmethod
    def normalize(value, behavior=None, **_):
        try:
            if behavior == 'list':
                if type(value) == list:
                    return [str(i) for i in value]
                else:
                    return [str(value)]

            return str(value)
        except ValueError as exc:
            raise NormalizationError(str(exc))


class TextField(StringField):
    _name = 'text'

    def __init__(self, *args, is_rich=None, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self.is_rich = is_rich

    def repr(self):
        _r = super(StringField, self).repr()
        _r['is_rich'] = self.is_rich
        return _r


class PasswordField(StringField):
    _name = 'string'

    def __init__(self, *args, new_password=False, **kwargs):
        super(StringField, self).__init__(*args, **kwargs)
        self.new_password = new_password  # field for new password or for old

    def repr(self):
        _r = super(StringField, self).repr()
        _r['field_type'] = 'password'
        _r['new_password'] = self.new_password

        return _r


class BaseKeyField(StringField):
    _name = 'key'


class BooleanField(BaseField):
    _name = 'boolean'

    @staticmethod
    def normalize(value, **_):
        try:
            return bool(value)
        except ValueError as exc:
            raise NormalizationError(str(exc))


class IntegerField(BaseField):
    _name = 'integer'

    def __init__(self, *args, negative_value=True, min: int = None, max: int = None, **kwargs):
        super(IntegerField, self).__init__(*args, **kwargs)
        self.negative_value = negative_value
        self.min = min
        self.max = max

    @staticmethod
    def normalize(value, **_):
        try:
            return int(value)
        except ValueError as exc:
            raise NormalizationError(str(exc))

    def repr(self):
        _repr = super(IntegerField, self).repr()
        _repr['negative_value'] = self.negative_value
        _repr.update({
            'min': self.min,
            'max': self.max,
        })
        return _repr


class DecimalField(IntegerField):
    _name = 'decimal'

    @staticmethod
    def normalize(value, **_):
        try:
            return decimal.Decimal(value)
        except (ValueError, decimal.InvalidOperation) as exc:
            raise NormalizationError(str(exc))


class DateField(BaseField):
    _name = 'date'

    @staticmethod
    def normalize_base(value, **_):
        if isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, datetime.date):
            return value
        else:
            try:
                return datetime.datetime.fromisoformat(value).date()
            except ValueError as exc:
                raise NormalizationError(str(exc))

    @staticmethod
    def normalize_es(value):
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        else:
            try:
                return parser.parse(value, fuzzy=False).isoformat()
            except:
                return None

    def __init__(self, *args, behavior=None, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)
        self.behavior = behavior

    def repr(self):
        _r = super(DateField, self).repr()
        _r['behavior'] = self.behavior

        return _r

    def normalize(self, value, behavior=None, **_):
        try:
            if behavior == 'list':
                if type(value) == list:
                    res = []
                    for _val in value:
                        res.append(self.normalize_base(_val))
                    return res
                else:
                    return [self.normalize_base(value)]
            elif behavior == 'range':
                if isinstance(value, dict):
                    _min = value.get('min', None)
                    _max = value.get('max', None)
                    res = {'min': None, 'max': None}
                    if _min:
                        res['min'] = self.normalize_base(_min)
                    if _max:
                        res['max'] = self.normalize_base(_max)

                else:
                    return {
                        'min': None,
                        'max': None,
                    }

            return self.normalize_base(value)
        except ValueError as exc:
            raise NormalizationError(str(exc))


class DateTimeField(BaseField):
    _name = 'datetime'

    def __init__(self, *args, behavior=None, **kwargs):
        super(DateTimeField, self).__init__(*args, **kwargs)
        self.behavior = behavior

    def repr(self):
        _r = super(DateTimeField, self).repr()
        _r['behavior'] = self.behavior
        _r['enable_time'] = True

        return _r

    @staticmethod
    def normalize_base(value, **_):
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value
        else:
            try:
                return datetime.datetime.fromisoformat(value).date()
            except ValueError as exc:
                raise NormalizationError(str(exc))

    def normalize(self, value, behavior=None, **_):
        try:
            if behavior == 'list':
                if type(value) == list:
                    res = []
                    for _val in value:
                        res.append(self.normalize_base(_val))
                    return res
                else:
                    return [self.normalize_base(value)]
            elif behavior == 'range':
                if isinstance(value, dict):
                    _min = value.get('min', None)
                    _max = value.get('max', None)
                    res = {'min': None, 'max': None}
                    if _min:
                        res['min'] = self.normalize_base(_min)
                    if _max:
                        res['max'] = self.normalize_base(_max)

                else:
                    return {
                        'min': None,
                        'max': None,
                    }

            return self.normalize_base(value)
        except ValueError as exc:
            raise NormalizationError(str(exc))

    @staticmethod
    def normalize_es(value):
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        else:
            try:
                return parser.parse(value, fuzzy=False).isoformat()
            except:
                return value


class SelectField(BaseField):
    _name = 'select'

    def __init__(self, *args, options_handler=None, options_params=None, **kwargs):
        super(SelectField, self).__init__(*args, **kwargs)
        self.options_handler = options_handler
        self.options_params = options_params

    @staticmethod
    def normalize(value, **_):
        return value

    def repr(self):
        r = super(SelectField, self).repr()
        r['options_handler'] = self.options_handler

        if 'params' not in r:
            r['params'] = self.options_params
        else:
            r['params'].update(**self.options_params)

        return r


class MultiselectField(SelectField):
    _name = 'multiselect'

    @staticmethod
    def normalize(value, **_):
        if isinstance(value, list):
            return value

        if not value:
            return []

        return [value]


class TagField(MultiselectField):
    _name = 'tag'


class LookupSelectField(SelectField):
    _name = 'lookup_select'

    @staticmethod
    def normalize(value, **_):
        return value


class LookupMultiselectField(SelectField):
    _name = 'lookup_multiselect'


class ProductSelectField(SelectField):
    _name = 'product_select'


class ProductMultiselectField(SelectField):
    _name = 'product_multiselect'


class MetricField(BaseField):
    _name = 'metric'

    def __init__(self, *args, family=None, options_handler=None, **kwargs):
        super(MetricField, self).__init__(*args, **kwargs)
        self.family = family
        self.options_handler = options_handler

    def repr(self):
        r = super(MetricField, self).repr()
        r['family'] = self.family
        r['options_handler'] = self.options_handler
        return r

    # @staticmethod
    # def normalize_es(value):
    #     if isinstance(value, (datetime.datetime, datetime.date)):
    #         return value.strftime('%Y-%m-%dT%H:%M:%S')
    #     else:
    #         return value

    @staticmethod
    def normalize(value, **_):
        if isinstance(value, dict):
            if not value.get('value'):
                return {}
            return value

        if not value:
            return {}

        return value


class CurrencyField(MetricField):
    _name = 'currency'


class VideoField(BaseField):
    _name = 'video'

    def __init__(self, limit=None, max_number_of_files=6, *args, **kwargs):
        super(VideoField, self).__init__(*args, **kwargs)
        self.limit = limit
        self.max_number_of_files = max_number_of_files

    def normalize(self, value, **_):
        return value

    def repr(self):
        repr = super(VideoField, self).repr()
        repr['max_number_of_files'] = self.max_number_of_files
        return repr


class DocumentField(BaseField):
    _name = 'document'

    def __init__(
        self,
        limit=None,
        upload_path=None,
        max_size_mb=1024,
        auto_proceed=False,
        allowed_types=None,
        max_number_of_files=6,
        *args,
        **kwargs,
    ):
        super(DocumentField, self).__init__(*args, **kwargs)
        self.limit = limit
        self.upload_path = upload_path
        self.max_size_mb = max_size_mb
        self.auto_proceed = auto_proceed
        self.allowed_types = allowed_types
        self.max_number_of_files = max_number_of_files

    def normalize(self, value, **_):
        return value

    def repr(self):
        repr = super(DocumentField, self).repr()
        repr['limit'] = self.limit
        repr['upload_path'] = self.upload_path
        repr['max_size_mb'] = self.max_size_mb
        repr['auto_proceed'] = self.auto_proceed
        repr['allowed_types'] = self.allowed_types
        repr['max_number_of_files'] = self.max_number_of_files
        return repr


class DocumentLinkField(BaseField):
    _name = 'document_link'

    def __init__(self, limit=None, *args, **kwargs):
        super(DocumentLinkField, self).__init__(*args, **kwargs)

    def normalize(self, value, **_):
        return value


class PhotoField(BaseField):
    _name = 'photo'

    def __init__(self, limit=None, max_number_of_files=6, *args, **kwargs):
        super(PhotoField, self).__init__(*args, **kwargs)
        self.limit = limit
        self.max_number_of_files = max_number_of_files

    def normalize(self, value, **_):
        return value

    def repr(self):
        repr = super(PhotoField, self).repr()
        repr['max_number_of_files'] = self.max_number_of_files
        return repr


# Для составных полей, таких как labels
class ObjectField(BaseField):
    _name = 'object'

    def __init__(self, *args, form_handler=None, **kwargs):
        super(ObjectField, self).__init__(*args, **kwargs)
        self.form_handler = form_handler


class OptionField(BaseField):
    _name = 'option'

    def __init__(self, *args, handler, **kwargs):
        super(OptionField, self).__init__(*args, **kwargs)
        self.handler = handler

    def repr(self):
        r = super(OptionField, self).repr()
        r['handler'] = self.handler
        return r


class DeleteField(BaseField):
    _name = 'delete'

    def __init__(self, *args, method=None, **kwargs):
        super(DeleteField, self).__init__(*args, **kwargs)
        self.method = method


class FiltersField(BaseField):
    _name = 'filters'


class EditField(BaseField):
    _name = 'edit'

    def __init__(self, *args, method=None, **kwargs):
        super(EditField, self).__init__(*args, **kwargs)
        self.method = method


class JSONObjectField(BaseField):
    _name = 'json_object'

    def __init__(self, *args, regex=None, behavior=None, field_type=None, **kwargs):
        super(JSONObjectField, self).__init__(*args, **kwargs)
        self.behavior = behavior
        self.field_type = field_type

        if regex:
            self.regex = RegExp(*regex)
        else:
            self.regex = None

    def repr(self):
        _r = super(JSONObjectField, self).repr()

        if self.regex:
            _r['regex'] = self.regex.repr()

        _r['behavior'] = self.behavior

        if self.field_type:
            _r['field_type'] = self.field_type

        if self.read_only:
            _r['read_only'] = self.read_only

        return _r

    @staticmethod
    def normalize(value, **_):
        return value


def _f_empty_value(key: str, value, ref, **__):
    if not value and not ref:
        raise ValidationError('Value must not be empty or null.', data=dict(key=key, value=value, code='ValueEmpty'))


def uuid_validator(key: str, value, ref, **__):
    if type(value) is not UUID:
        raise ValidationError('Value must be UUID.', data=dict(key=key, value=value, code='ValueMustBeUUID'))


def normalizer_value(value, **_):
    return str(value).lower()


SimpleIdField = partial(
    StringField,
    read_only=True,
    required=True,
    validator=_f_empty_value,
    normalizer=normalizer_value,
    regex=(r'^[a-z0-9_]+$', 'Regex.key'),
)

IdField = partial(
    StringField,
    read_only=True,
    required=True,
    validator=_f_empty_value,
    normalizer=normalizer_value,
    regex=(r'\S+', 'Regex.non_whitespace'),
)

UUIDField = partial(
    StringField, read_only=True, required=True, validator=uuid_validator, regex=(r'\S+', 'Regex.non_whitespace')
)


class MediaFileField(DocumentField):
    _name = 'media_file'


class MediaMultiselectField(SelectField):
    _name = 'media_multiselect'

    def compare(self, val1, val2):
        if val1 is not None:
            val1.sort()

        if val2 is not None:
            val2.sort()

        return val1 == val2


class MediaField(SelectField):
    _name = 'media'

    def compare(self, val1, val2):
        if val1 is not None:
            val1.sort()

        if val2 is not None:
            val2.sort()

        return val1 == val2


class NestedField(BaseField):
    _name = 'nested'

    def __init__(self, *args, **kwargs):
        self._fields = []
        self.init_fields(kwargs)
        super(NestedField).__init__(*args, **kwargs)

    def init_fields(self, fields: dict):
        for k, field in list(fields.items()):
            if isinstance(field, BaseField):
                fields.pop(k)
                self._fields.append({
                    'id': k,
                    **field.repr()
                })

    def repr(self):
        _r = super().repr()
        _r['fields'] = self._fields
        return _r

    @staticmethod
    def normalize(value, **_):
        # TODO NEED FIELD NOMALIZER

        return value


class NestedListField(NestedField):
    _name = 'nested_list'

    def normalize(self, value, **_):
        # TODO NEED FIELD NORMALIZER
        return value


class TextBlock(BaseField):
    _name = 'text_block'

    def __init__(self, *args, text: str = None, text_key: str = None, **kwargs):
        super(TextBlock).__init__(*args, **kwargs)
        self.text = text
        self.text_key = text_key

    def repr(self):
        _r = super(TextBlock).repr()
        _r['text'] = self.text
        _r['text_key'] = self.text_key
        return _r
