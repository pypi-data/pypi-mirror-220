import abc
import asyncio
import inspect
from collections import ChainMap
from enum import Enum
from types import SimpleNamespace
from typing import *

from kaiju_tools.services import ContextableService
from kaiju_tools.exceptions import ValidationError, APIException, InvalidLicense
from kaiju_tools.mapping import unflatten

# from .validators import *
from .fields import FieldGroups, BaseField, NormalizationError


class ServiceMeta(abc.ABCMeta):
    def __init__(cls, *args, **kws):
        super().__init__(*args, **kws)
        if abc.ABC not in cls.__bases__:
            cls._set_service_name(cls)
            cls._format_service_error_codes(cls)

    @staticmethod
    def _set_service_name(cls):
        if cls.service_name is None:
            cls.service_name = cls.__name__

    @staticmethod
    def _format_service_error_codes(cls):
        codes = {}

        if not getattr(cls, 'ErrorCodes', None):
            cls.__ErrorCodes = SimpleNamespace(**codes)
            return

        for code in dir(cls.ErrorCodes):
            if not code.startswith('_'):
                value = getattr(cls.ErrorCodes, code)
                codes[code] = cls._create_error_code(value)
        cls.__ErrorCodes = SimpleNamespace(**codes)


class Behavior(Enum):
    list = 'list'
    range = 'range'


class ModelValidationException(ValidationError):
    def __init__(self, fields: dict, data: dict = None, **kwargs):
        """
        Пример структуры:

        fields = {
            k: [dict(key=k, value=v, code='ValidationError.required')]
        }

        :param fields: инфо для формы
        :param data:
        :param kwargs:
        """
        if not data:
            data = {}

        data['fields'] = fields
        super(ModelValidationException, self).__init__('ModelValidationException', data=data, **kwargs)


class ModelMeta(ServiceMeta, abc.ABCMeta):
    __attr_name__ = None
    _name = None
    __value__ = None

    BASE_CLASSES = []

    def __new__(mcs, name, superclasses, attr):
        new_cls = super().__new__(mcs, name, superclasses, attr)

        # attribute type check

        if abc.ABC not in new_cls.__bases__:
            if not new_cls.__value__:
                raise ValueError(f'{name}.__value__ attribute must be set.')
            if not new_cls.__attr_name__:
                new_cls._name = new_cls.__value__.type
            else:
                new_cls._name = new_cls.__attr_name__
        else:
            mcs.BASE_CLASSES.append(new_cls)

        new_cls._base_fields = {}
        new_cls._optional_fields = {}
        new_cls._fields = {}
        new_cls._sync_validators = {}
        new_cls._async_validators = {}
        new_cls._sync_field_validators = {}
        new_cls._async_field_validators = {}

        # attribute fields processing

        for _cls in reversed(new_cls.mro()):
            for name in _cls.__dict__:
                attr = getattr(new_cls, name)
                if isinstance(attr, BaseField):

                    # value should not be in attribute parameters
                    if name != '__value__':
                        if attr.group == FieldGroups.BASE.value:
                            new_cls._base_fields[name] = attr
                        else:
                            new_cls._optional_fields[name] = attr

                    # but value field may have its own validator
                    validate = getattr(attr, 'validate', None)
                    if validate:
                        if inspect.iscoroutinefunction(attr.validate):
                            new_cls._async_validators[name] = attr.validate
                        else:
                            new_cls._sync_validators[name] = attr.validate

                    field_validator = getattr(attr, 'field_validator', None)
                    if field_validator:
                        if inspect.iscoroutinefunction(field_validator):
                            new_cls._async_field_validators[name] = field_validator
                        else:
                            new_cls._sync_field_validators[name] = field_validator

        new_cls._fields = ChainMap(new_cls._base_fields, new_cls._optional_fields)
        return new_cls

    @property
    def name(cls):
        return cls._name


class BaseModel(ContextableService, abc.ABC, metaclass=ModelMeta):
    # auto-set by a metaclass

    _base_fields = {}
    _optional_fields = {}
    _fields = {}
    _sync_validators = {}
    _async_validators = {}
    _field_validators = {}
    _name = None

    # ---

    __value__ = None  #: value field must be set in an actual attribute type
    __attr_name__ = None  #: you may define a custom attribute type name here

    def __init__(self, app=None, *_, init=True, logger=None, **kws):
        """
        :param _:
        :param init: pass False if you don't need to validate attribute settings
        :param kws: attribute settings
        """

        super().__init__(app=app, logger=logger)
        self._app = app
        self.base = {}
        self.settings = {}
        self.params = ChainMap(self.base, self.settings)
        self._init = init

        # attribute settings evaluation

        if init:
            for k, field in self._fields.items():
                v = kws.get(k)
                normalize = getattr(field, 'normalize', None)
                nested = getattr(field, 'nested', None)

                if (
                    (
                        v is None
                        or (type(v) is list and not v)
                        or (type(v) is dict and not v)
                        or (type(v) is str and not v)
                    )
                    and nested
                    and nested in kws
                ):
                    nested_values = kws[nested]

                    if isinstance(nested_values, dict):
                        v = nested_values.get(k)

                if (
                    v is None
                    or (type(v) is list and not v)
                    or (type(v) is dict and not v)
                    or (type(v) is str and not v)
                ):
                    if field.required:
                        fields = {k: [dict(key=k, value=v, code='ValidationError.required')]}

                        raise ModelValidationException(fields=fields)

                    else:
                        v = field.default
                elif normalize:
                    try:
                        behavior = getattr(field, 'behavior', None)
                        v = normalize(v, behavior=behavior, model=self) if behavior else normalize(v, model=self)
                    except NormalizationError:
                        fields = {k: [dict(key=k, value=v, code='ValidationError.WrongValueType')]}

                        raise ModelValidationException(fields=fields)

                regex = getattr(field, 'regex', None)
                if regex and v:
                    if not regex.compiled.fullmatch(v):
                        fields = {k: [dict(key=k, value=v, code='ValidationError.RegexMismatch')]}

                        raise ModelValidationException(fields=fields)

                if k in self._base_fields:
                    self.base[k] = v
                elif k in self._optional_fields:
                    self.settings[k] = v
                setattr(self, k, v)

        else:
            for k, field in self._fields.items():
                nested = getattr(field, 'nested', None)
                default = getattr(field, 'default', None)
                in_kws = False
                v = None
                if k in kws:
                    v = kws[k]
                    in_kws = True

                if (
                    (
                        v is None
                        or (type(v) is list and not v)
                        or (type(v) is dict and not v)
                        or (type(v) is str and not v)
                    )
                    and nested
                    and nested in kws
                ):
                    nested_values = kws[nested]

                    if isinstance(nested_values, dict):
                        v = nested_values.get(k)
                        in_kws = True

                if v is None and default is not None:
                    v = default
                    in_kws = True

                if in_kws:
                    if k in self._base_fields:
                        self.base[k] = v
                    elif k in self._optional_fields:
                        self.settings[k] = v
                    setattr(self, k, v)

        #
        # for k, v in kws.items():
        #         if k in self._fields:
        #             field = self._fields[k]
        #             nested = getattr(field, 'nested', None)
        #
        #             if k in self._base_fields:
        #                 self.base[k] = v
        #             elif k in self._optional_fields:
        #                 self.settings[k] = v
        #             setattr(self, k, v)

    async def init(self):
        if self._init:
            try:
                if self._sync_field_validators:
                    for name, validator in self._sync_field_validators.items():
                        value = self.params[name]
                        validator(name, value, None)
                if self._async_field_validators:
                    await asyncio.gather(
                        *(
                            validator(self._app, name, self.params[name], self.params)
                            for name, validator in self._async_field_validators.items()
                        )
                    )
            except ValidationError as e:
                raise ModelValidationException(base_exc=e, fields={e.data['key']: [e.data]})
            except InvalidLicense as e:
                raise e
            except Exception as e:
                raise APIException(message=e.__class__.__name__, base_exc=e)

    def __iter__(self):
        return iter(self.params.items())

    def to_dict(self):
        result = {}

        for key, field in self._fields.items():
            if field._name == 'text_block':
                continue
            if key in self.params:
                value = self.params[key]
                nested = getattr(field, 'nested', None)
                if nested:
                    result[f'{nested}.{key}'] = value
                else:
                    result[key] = value

        return unflatten(result)

    def repr(self):
        return {**self.params}

    @property
    def name(self):
        return self.__class__.name

    @property
    def type(self):
        return self.__class__.type

    @classmethod
    def get_fields(cls, default_values=None, exclude=None):
        """Returns attribute fields spec."""
        if type(default_values) is not dict:
            default_values = {}

        if type(exclude) is not set:
            exclude = set()

        base = {
            'id': FieldGroups.BASE.value,
            'fields': [
                {'id': name, **field.repr(), **default_values.get(name, {})}
                for name, field in cls._base_fields.items()
                if not field.is_system and name not in exclude
            ]
        }

        optional = {}

        for name, field in cls._optional_fields.items():
            if not field.is_system and name not in exclude:
                data = {'id': name, **field.repr(), **default_values.get(name, {})}

                if field.group in optional:
                    optional[field.group].append(data)
                else:
                    optional[field.group] = [data]

        optional = [{'id': key, 'fields': values} for key, values in optional.items()]

        return [base, *optional]

    def _is_required(self, value):

        if isinstance(value, list):
            is_empty = not all(value) and value
        elif isinstance(value, dict):
            is_empty = not value or None
        else:
            is_empty = value in {'', None}

        return not self.params.get('required') and is_empty

    async def validate(self, value: Any, behavior: str = None) -> Tuple[Any, List[ValidationError]]:
        behavior = getattr(self, 'behavior', None) or behavior or None

        # if self._is_required(value):
        #     return value, []

        # TODO какая-то хрень, возможно из-за старой базы ошибка возникает
        if behavior and type(behavior) != str:
            behavior = None

        if behavior is None:
            return await self._validate(value)

        if behavior == Behavior.list.value:
            if value and type(value) != list:
                return value, [
                    ValidationError(
                        'Value should be list',
                        data=dict(key=self.key, value=value, code='ValidationError.WrongValueType'),
                    )
                ]

            if not value:
                value = []

            list_values = []
            validation_errors = []

            for val in value:
                clean_value, errors = await self._validate(val)
                validation_errors.extend(errors)
                list_values.append(clean_value)

            return list_values, validation_errors

        if behavior == Behavior.range.value:
            if value and type(value) != dict:
                return value, [
                    ValidationError(
                        'Value should be dict',
                        data=dict(key=self.key, value=value, code='ValidationError.WrongValueType'),
                    )
                ]

            if not value:
                value = {}

            min_value = value.get('min')
            max_value = value.get('max')

            clean_val_min, error_min = await self._validate(min_value)
            clean_val_max, error_max = await self._validate(max_value)

            error_min.extend(error_max)

            return {'min': clean_val_min, 'max': clean_val_max}, error_min

        return value, [
            ValidationError(
                'Behavior mismatch.', data=dict(key=self.key, value=value, code='ValidationError.BehaviorNotExists')
            )
        ]

    async def _validate(self, value: Any) -> Tuple[Any, List[ValidationError]]:
        """Validates a field value against all validation functions.

        :returns: a normalized value and a list of validation errors if any
        """

        # normalization

        validation_errors = []

        if self._is_required(value):
            return value, validation_errors

        if self.__value__ is not None and self.__value__.normalize:
            try:
                value = self.__value__.normalize(value, model=self)
            except NormalizationError:
                validation_errors = [
                    ValidationError(
                        'Wrong value type.', data=dict(key=self.key, value=value, code='ValidationError.WrongValueType')
                    )
                ]
                return value, validation_errors

        # validation

        if self._sync_validators:
            for key, validator in self._sync_validators.items():
                ref = self.params.get(key)
                if ref is not None:
                    try:
                        validator(self.key, value, ref, model=self)
                    except ValidationError as exc:
                        validation_errors.append(exc)

        regex = getattr(self.__value__, 'regex', None)
        if regex and not regex.compiled.fullmatch(value):
            validation_errors.append(
                ValidationError(
                    'Regular expression mismatch.',
                    data=dict(key=self.key, value=value, code=regex.msg or 'RegexMismatch'),
                )
            )

        if self._async_validators:
            validators = await asyncio.gather(
                *(
                    validator(self._app, self.key, value, self.params[key], model=self)
                    for key, validator in self._async_validators.items()
                    if self.params[key] is not None
                ),
                return_exceptions=True,
            )

            for validator in validators:
                if isinstance(validator, ValidationError):
                    validation_errors.append(validator)
                elif isinstance(validator, Exception):
                    raise validator

        return value, validation_errors

    @classmethod
    def normalize_es(cls, value):
        """Custom value normalization for Elasticsearch."""

        normalizer = getattr(cls.__value__, 'normalize_es', None)
        if normalizer:
            return cls.__value__.normalize_es(value)
        else:
            return value

    @property
    def es_settings(self) -> Optional:
        """
        Elasticsearch field settings.
        Return None if you don't need to store the field in ES.
        """

        return

    @property
    def fields(self):
        """Returns attribute fields spec."""

        base = {
            'id': FieldGroups.BASE.value,
            'fields': [
                {'id': name, "value": self.params.get(name), **field.repr(), **self.modify(name, field), "disabled": self._fields[name].read_only}
                for name, field in self._base_fields.items() if not field.is_system
            ]
        }

        optional = {}

        for name, field in self._optional_fields.items():
            _modify = self.modify(name, field)
            if not _modify.get('is_system', field.is_system):
                data = {
                    'id': name,
                    'value': self.params.get(name),
                    **field.repr(),
                    'disabled': self._fields[name].read_only,
                    **self.modify(name, field),
                }
                if field.group in optional:
                    optional[field.group].append(data)
                else:
                    optional[field.group] = [data]

        optional = [{'id': key, 'fields': values} for key, values in optional.items()]

        return [base, *optional]

    def modify(self, *_, **__):
        return {}

    def form_normalize(self):
        pass
