import asyncio
import inspect
from collections import ChainMap

from kaiju_tools.services import ContextableService, Service
from kaiju_tools.registry import ClassRegistry

# from engine.modules.grid import handlers
from .base import BaseHandler


class GridHandlers(ClassRegistry):

    @classmethod
    def get_base_classes(cls):
        return BaseHandler,


grid_handler_service = GridHandlers()


class GridConstructor(ContextableService):
    def __init__(
        self,
        app,
        models: list,
        fields,
        logger=None,
        locale=None,
        _id='id',
        _meta=None,
        _grid_handler_service=grid_handler_service,
    ):
        super(GridConstructor, self).__init__(app=app, logger=logger)
        self._app = app
        self._fields = fields
        self._model = models
        self._grid = []
        self._id = _id
        self._locale = locale
        self._meta = _meta or {}

        self._sync_handlers = None
        self._async_handlers = None
        self._values = None
        self._grid_handler_service = _grid_handler_service

        self._init_handlers()

    async def init(self):
        results = await self._call_handlers()

        for _m in self._model:
            row = {}
            _id = getattr(_m, self._id, None)
            _is_system = getattr(_m, 'is_system', None)
            _is_default = getattr(_m, 'is_default', None)

            for k in self._fields:
                f = _m._fields.get(k)
                if f:
                    base_value = getattr(_m, k)
                    grid_handler = self._get_handler(f)
                    _behavior = getattr(f, 'behavior', None)

                    _d = {
                        'id': _id,
                        'key': k,
                        'kind': f.type,
                        'behavior': _behavior,
                        'value': base_value,
                        'base_value': base_value,
                    }

                    if grid_handler and grid_handler in self._grid_handler_service:
                        _value = results.get(k, {}).get(_id)
                        _d['value'] = _value

                    row[k] = _d

                    if _is_system is not None:
                        row[k]['is_system'] = _is_system

                    if _is_default is not None:
                        row[k]['is_default'] = _is_default

            self._grid.append(row)

    @property
    def grid(self):
        return self._grid

    def __iter__(self):
        return iter(self._grid)

    def repr(self):
        return self._grid

    @staticmethod
    def _get_handler(attr):
        handler = getattr(attr, 'grid_handler', None)
        return handler

    def _init_handlers(self):
        fields = set(self._fields)
        sync_handlers, async_handlers, values, models = {}, {}, {}, {}
        handlers = ChainMap(sync_handlers, async_handlers)

        for model in self._model:
            _id = getattr(model, self._id, None)

            for k, f in model._fields.items():
                grid_handler = self._get_handler(f)

                if grid_handler and grid_handler in self._grid_handler_service and k in fields:
                    if k not in handlers:
                        grid_handler = self._grid_handler_service[grid_handler]
                        grid_handler = grid_handler(app=self._app, locale=self._locale, meta=self._meta)
                        if inspect.iscoroutinefunction(grid_handler.call):
                            async_handlers[k] = grid_handler
                        else:
                            sync_handlers[k] = grid_handler

                    _val = getattr(model, k, None)

                    values.setdefault(k, []).append({'id': _id, 'value': _val, 'field': f, 'model': model})

        self._sync_handlers = sync_handlers
        self._async_handlers = async_handlers
        self._values = values

    async def _call_handlers(self) -> dict:
        results = {key: handler.call(self._values.get(key)) for key, handler in self._sync_handlers.items()}
        tasks = (handler.call(self._values.get(key)) for key, handler in self._async_handlers.items())
        tasks = await asyncio.gather(*tasks)
        results.update({key: result for key, result in zip(self._async_handlers.keys(), tasks)})
        return results


class ProductGridConstructor(GridConstructor):
    def __init__(
        self,
        app,
        attributes,
        rows,
        order,
        locale,
        logger=None,
        _id='id',
        _meta=None,
        _grid_handler_service=grid_handler_service,
    ):
        Service.__init__(self, app=app, logger=logger)
        self._app = app
        self._rows = rows
        self._attributes = attributes
        self._order = order if order else []
        self._grid = []
        self._id = _id
        self._locale = locale
        self._meta = _meta
        self._es_mapping = None

        self._sync_handlers = None
        self._async_handlers = None
        self._values = None
        self._grid_handler_service = _grid_handler_service

        self._init_handlers()

    async def init(self):
        results = await self._call_handlers()

        if type(self._attributes) is dict:
            _attributes = list(self._attributes.values())
        else:
            _attributes = self._attributes

        for _id in self._order:
            row = {}

            for _attr_object in _attributes:
                _key = _attr_object.params[self._id]
                behavior = _attr_object.params.get('behavior')
                attr_values = self._rows[_id]
                base_value = attr_values.get(_key)

                grid_handler = self._get_handler(_attr_object)

                if grid_handler and grid_handler in self._grid_handler_service:
                    _value = results.get(_key, {}).get(_id)
                else:
                    _value = base_value

                row[_key] = {
                    'id': _id,
                    'key': _key,
                    'behavior': behavior,
                    'kind': _attr_object.name,
                    'value': _value,
                    'base_value': base_value,
                }

            self._grid.append(row)

    @property
    def grid(self):
        return self._grid

    def __iter__(self):
        return iter(self._grid)

    def repr(self):
        return self._grid

    @staticmethod
    def _get_handler(attr):
        handler = attr.params.get('grid_handler')
        return handler

    def _init_handlers(self):
        sync_handlers, async_handlers, values = {}, {}, {}
        handlers = ChainMap(sync_handlers, async_handlers)

        if type(self._attributes) is dict:
            _attributes = list(self._attributes.values())
        else:
            _attributes = self._attributes

        for row, attrs in self._rows.items():
            for _attr_object in _attributes:
                _key = _attr_object.params[self._id]
                _current_value = attrs.get(_key)
                grid_handler = self._get_handler(_attr_object)

                if grid_handler and grid_handler in self._grid_handler_service:
                    if _key not in handlers:
                        grid_handler = self._grid_handler_service[grid_handler]
                        grid_handler = grid_handler(app=self._app, locale=self._locale, meta=self._meta)
                        if inspect.iscoroutinefunction(grid_handler.call):
                            async_handlers[_key] = grid_handler
                        else:
                            sync_handlers[_key] = grid_handler

                    values.setdefault(_key, []).append({'id': row, 'value': _current_value, 'model': _attr_object})

        self._sync_handlers = sync_handlers
        self._async_handlers = async_handlers
        self._values = values


class GridHeaderConstructor(ProductGridConstructor):
    def __init__(
        self,
        app,
        attributes: list,
        order,
        locale,
        logger=None,
        _id='id',
        _meta=None,
        _grid_handler_service=grid_handler_service,
    ):
        Service.__init__(self, app=app, logger=logger)
        self._app = app
        self._attributes = attributes
        self._order = order
        self._locale = locale
        self._id = _id
        self._meta = _meta
        self._grid = []
        self._sync_handlers = {}
        self._async_handlers = {}
        self._values = {}

        self._init_handlers()

    async def init(self):
        keys = {}
        result = await self._call_handlers()

        for _, _k in result.items():
            keys.update(_k)

        for i in self._order:
            _r = {'key': i}
            label = keys.get(i)
            if label:
                _r['label'] = label

            else:
                _r['label'] = f'[{i}]'

            self._grid.append(_r)

    def _init_handlers(self):
        sync_handlers, async_handlers, values = {}, {}, {}
        handlers = ChainMap(sync_handlers, async_handlers)

        if type(self._attributes) is dict:
            _attributes = list(self._attributes.values())
        else:
            _attributes = self._attributes

        for model in _attributes:
            str_grid_handler = self._get_handler(model._fields['labels'])
            # str_grid_handler = getattr(model._fields["labels"], "grid_handler")
            key = model.params['key']

            if str_grid_handler and str_grid_handler in self._grid_handler_service:
                if str_grid_handler not in handlers:
                    grid_handler = self._grid_handler_service[str_grid_handler]
                    grid_handler = grid_handler(app=self._app, locale=self._locale, meta=self._meta)
                    if inspect.iscoroutinefunction(grid_handler.call):
                        async_handlers[str_grid_handler] = grid_handler
                    else:
                        sync_handlers[str_grid_handler] = grid_handler

                k = values.setdefault(str_grid_handler, [])
                k.append({'id': key})

        self._sync_handlers = sync_handlers
        self._async_handlers = async_handlers
        self._values = values
