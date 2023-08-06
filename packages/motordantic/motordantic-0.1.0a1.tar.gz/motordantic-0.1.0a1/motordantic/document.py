import json
from typing import (
    Dict,
    Any,
    Union,
    Optional,
    List,
    Tuple,
    TYPE_CHECKING,
    ClassVar,
)

from bson import ObjectId, DBRef, decode as bson_decode
from bson.raw_bson import RawBSONDocument
from motor.core import AgnosticClientSession
from pydantic.main import ModelMetaclass as PydanticModelMetaclass, default_ref_template
from pydantic import (
    BaseModel as BasePydanticModel,
    root_validator,
    BaseConfig,
    ValidationError,
)
from pydantic.main import ValueItems, _missing
from pydantic.typing import resolve_annotations
from pydantic.fields import Undefined
from pymongo import IndexModel


from .relation import RelationManager
from .types import ObjectIdStr, RelationInfo, Relation
from .exceptions import (
    MotordanticValidationError,
    MotordanticConnectionError,
)
from .property import classproperty
from .query.extra import take_relation
from .fields import ComputedField, MotordanticFieldInfo
from .schema import model_schema
from .manager import ODMManager


__all__ = ('Document', 'DocumentMetaclass')

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from pydantic.main import MappingIntStrAny, TupleGenerator
    from .typing import DictStrAny, AbstractSetIntStr, SetStr
    from .query import QueryBuilder
    from .sync.query import SyncQueryBuilder


_is_document_class_defined = False


class DocumentMetaclass(PydanticModelMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):  # type: ignore
        annotations = resolve_annotations(
            namespace.get("__annotations__", {}), namespace.get("__module__")
        )
        mapping_query_fields = {'_id': '_id'}
        for field_name in annotations:
            value = namespace.get(field_name, Undefined)
            if isinstance(value, MotordanticFieldInfo):
                namespace[field_name] = value.pydantic_field_info
                mapping_query_fields[field_name] = value.db_field_name or field_name
            else:
                mapping_query_fields[field_name] = field_name
        namespace['__mapping_query_fields__'] = mapping_query_fields
        namespace['__mapping_from_fields__'] = {
            db_field: cls_field for cls_field, db_field in mapping_query_fields.items()
        }
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        indexes = set()
        config = BaseConfig
        if _is_document_class_defined and issubclass(cls, Document):
            db_refs = {}
            for k, v in cls.__fields__.items():
                relation_info = take_relation(v)
                if relation_info is not None:
                    db_refs[k] = relation_info
            setattr(cls, '__db_refs__', db_refs)
            if db_refs:
                setattr(cls, 'has_relations', True)
                setattr(cls, '__relation_manager__', RelationManager(cls))  # type: ignore
            computed_fields = {}
            for var_name, value in namespace.items():
                if isinstance(value, ComputedField):
                    computed_fields[var_name] = value
                    value.set_config_and_prepare_field(config)
            if computed_fields:
                setattr(cls, '__motordantic_computed_fields__', computed_fields)
        json_encoders = getattr(cls.Config, 'json_encoders', {})  # type: ignore
        json_encoders.update({ObjectId: lambda f: str(f)})
        setattr(cls.Config, 'json_encoders', json_encoders)  # type: ignore
        exclude_fields = getattr(cls.Config, 'exclude_fields', tuple())  # type: ignore
        collection_name = (
            getattr(cls.Config, 'collection_name', None) or cls.__name__.lower()
        )
        setattr(cls, '__collection_name__', collection_name)
        setattr(cls, '__indexes__', indexes)
        setattr(cls, '__database_exclude_fields__', exclude_fields)
        setattr(cls, '__manager__', ODMManager(cls))  # type: ignore
        return cls


class Document(BasePydanticModel, metaclass=DocumentMetaclass):
    __indexes__: 'SetStr' = set()
    __manager__: ODMManager
    __database_exclude_fields__: Union[Tuple, List] = tuple()
    __db_refs__: ClassVar[Optional[Dict[str, RelationInfo]]] = None
    __relation_manager__: Optional[RelationManager] = None
    __motordantic_computed_fields__: Dict[str, ComputedField] = {}
    __mapping_query_fields__: Dict[str, str] = {}
    __mapping_from_fields__: Dict[str, str] = {}
    __collection_name__: Optional[str] = None
    _id: Optional[ObjectIdStr] = None
    has_relations: ClassVar[bool] = False

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:
            raise MotordanticValidationError(e.errors, e)

    def __setattr__(self, key, value):
        if key == '_id':
            self.__dict__[key] = value
            return value
        else:
            return super().__setattr__(key, value)

    def __getattribute__(self, attr):
        attribute = super().__getattribute__(attr)
        if isinstance(attribute, ComputedField):
            return attribute.fget(self)
        return attribute

    @property
    def _io_loop(self) -> 'AbstractEventLoop':
        return self.manager._io_loop

    @classmethod
    async def ensure_indexes(cls):
        """method for create/update/delete indexes if indexes declared in Config property"""

        indexes = getattr(cls.__config__, 'indexes', [])
        if not all([isinstance(index, IndexModel) for index in indexes]):
            raise ValueError('indexes must be list of IndexModel instances')
        if indexes:
            db_indexes = await cls.Q.list_indexes()
            indexes_to_create = [
                i for i in indexes if i.document['name'] not in db_indexes
            ]
            indexes_to_delete = [
                i
                for i in db_indexes
                if i not in [i.document['name'] for i in indexes] and i != '_id_'
            ]
            result = []
            if indexes_to_create:
                try:
                    result = await cls.Q.create_indexes(indexes_to_create)
                except MotordanticConnectionError:
                    pass
            if indexes_to_delete:
                for index_name in indexes_to_delete:
                    await cls.Q.drop_index(index_name)
                db_indexes = await cls.Q.list_indexes()
            indexes = set(list(db_indexes.keys()) + result)
        setattr(cls, '__indexes__', indexes)

    @classmethod
    def _get_properties(cls) -> list:
        return [
            prop
            for prop in dir(cls)
            if prop
            not in (
                "__values__",
                "data",
                "querybuilder",
                "Q",
                "Qsync",
                "pk",
                "_query_data",
                "_mongo_query_data",
                "fields_all",
                "_io_loop",
            )
            and isinstance(getattr(cls, prop), property)
        ]

    @classmethod
    def parse_obj(cls, data: Any) -> Any:
        if cls.__motordantic_computed_fields__:
            data = {
                k: v
                for k, v in data.items()
                if k not in cls.__motordantic_computed_fields__
            }
        obj = super().parse_obj(data)
        if '_id' in data:
            obj._id = data['_id'].__str__()
        return obj

    async def save(
        self,
        updated_fields: Union[Tuple, List] = [],
        session: Optional[AgnosticClientSession] = None,
    ) -> Any:
        if self._id is not None:
            data = {
                '_id': (
                    self._id if isinstance(self._id, ObjectId) else ObjectId(self._id)
                )
            }
            if updated_fields:
                if not all(field in self.__fields__ for field in updated_fields) or any(
                    field in self.__motordantic_computed_fields__
                    for field in updated_fields
                ):
                    raise MotordanticValidationError('invalid field in updated_fields')
            else:
                updated_fields = tuple(self.__fields__.keys())
            for field in updated_fields:
                if field in self.__motordantic_computed_fields__:
                    continue
                else:
                    data[f'{field}__set'] = getattr(self, field)
            await self.Q.update_one(
                session=session,
                **data,
            )
            return self
        data = {
            field: value
            for field, value in self.__dict__.items()
            if field in self.__fields__
        }
        object_id = await self.Q.insert_one(
            session=session,
            **data,
        )
        self._id = object_id
        return self

    def save_sync(
        self,
        updated_fields: Union[Tuple, List] = [],
        session: Optional[AgnosticClientSession] = None,
    ):
        return self._io_loop.run_until_complete(self.save(updated_fields, session))

    async def delete(self) -> None:
        await self.Q.delete_one(_id=self.pk)

    def delete_sync(self) -> None:
        return self._io_loop.run_until_complete(self.delete())

    @classproperty
    def fields_all(cls) -> list:
        """return all fields with properties(not document fields)"""
        fields = list(cls.__fields__.keys())
        return_fields = fields + cls._get_properties()
        return return_fields

    @classproperty
    def manager(cls) -> ODMManager:
        return cls.__manager__

    @classproperty
    def Q(cls) -> 'QueryBuilder':
        return cls.manager.querybuilder

    @classproperty
    def Qsync(cls) -> 'SyncQueryBuilder':
        return cls.manager.sync_querybuilder

    def _iter(
        self,
        to_dict: bool = False,
        by_alias: bool = False,
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> 'TupleGenerator':

        # Merge field set excludes with explicit exclude parameter with explicit overriding field set options.
        # The extra "is not None" guards are not logically necessary but optimizes performance for the simple case.
        if exclude is not None or self.__exclude_fields__ is not None:
            exclude = ValueItems.merge(self.__exclude_fields__, exclude)

        if include is not None or self.__include_fields__ is not None:
            include = ValueItems.merge(self.__include_fields__, include, intersect=True)

        allowed_keys = self._calculate_keys(
            include=include, exclude=exclude, exclude_unset=exclude_unset  # type: ignore
        )
        if allowed_keys is None and not (
            to_dict or by_alias or exclude_unset or exclude_defaults or exclude_none
        ):
            # huge boost for plain _iter()
            yield from self.__dict__.items()
            return

        value_exclude = ValueItems(self, exclude) if exclude is not None else None
        value_include = ValueItems(self, include) if include is not None else None

        for field_key, v in self.__dict__.items():
            if (allowed_keys is not None and field_key not in allowed_keys) or (
                exclude_none and v is None
            ):
                continue

            if exclude_defaults:
                model_field = self.__fields__.get(field_key)
                if (
                    not getattr(model_field, 'required', True)
                    and getattr(model_field, 'default', _missing) == v
                ):
                    continue

            if by_alias and field_key in self.__fields__:
                dict_key = self.__fields__[field_key].alias
            else:
                dict_key = field_key

            if to_dict or value_include or value_exclude:
                v = self._get_value(
                    v,
                    to_dict=to_dict,
                    by_alias=by_alias,
                    include=value_include and value_include.for_element(field_key),
                    exclude=value_exclude and value_exclude.for_element(field_key),
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                )
            yield dict_key, v

        for field_key, v in self.__motordantic_computed_fields__.items():
            yield field_key, v.fget(self)

    def dict(  # type: ignore
        self,
        *,
        include: Optional['AbstractSetIntStr'] = None,
        exclude: Optional['AbstractSetIntStr'] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        with_props: bool = True,
    ) -> 'DictStrAny':
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        """
        attribs = super().dict(
            include=include,  # type: ignore
            exclude=exclude,  # type: ignore
            by_alias=by_alias,
            skip_defaults=skip_defaults,  # type: ignore
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if self.__motordantic_computed_fields__:
            for field, value in self.__motordantic_computed_fields__.items():
                attribs[field] = value.fget(self)
        if with_props:
            props = self._get_properties()
            # Include and exclude properties
            if include:
                props = [prop for prop in props if prop in include]
            if exclude:
                props = [prop for prop in props if prop not in exclude]

            # Update the attribute dict with the properties
            if props:
                attribs.update({prop: getattr(self, prop) for prop in props})
        else:
            if self.__motordantic_computed_fields__:
                for field in self.__motordantic_computed_fields__:
                    attribs.pop(field)
        if self.has_relations:
            for field in self.__db_refs__:  # type: ignore
                attrib_data = attribs[field]
                if attrib_data and not isinstance(attrib_data, dict):
                    attribs[field] = (
                        attrib_data.to_dict()
                        if not isinstance(attrib_data, list)
                        else [
                            a.to_dict() if not isinstance(a, dict) else a
                            for a in attrib_data
                        ]
                    )
        return attribs

    @classmethod
    def schema(
        cls, by_alias: bool = True, ref_template: str = default_ref_template  # type: ignore
    ) -> 'DictStrAny':
        cached = cls.__schema_cache__.get((by_alias, ref_template))
        if cached is not None:
            return cached
        s = model_schema(cls, by_alias=by_alias, ref_template=ref_template)
        cls.__schema_cache__[(by_alias, ref_template)] = s
        return s

    @classmethod
    def from_bson(cls, bson_raw_data: RawBSONDocument) -> 'Document':
        data = bson_decode(bson_raw_data.raw)
        data = {
            cls.__mapping_from_fields__[field]: value for field, value in data.items()
        }
        obj = cls(**data)
        obj._id = data.get('_id')
        return obj

    @classmethod
    def to_db_ref(cls, object_id: Union[str, ObjectId]) -> DBRef:
        if isinstance(object_id, str):
            object_id = ObjectId(object_id)
        db_ref = DBRef(collection=cls.get_collection_name(), id=object_id)
        return db_ref

    @classmethod
    def to_relation(cls, object_id: Union[str, ObjectId]) -> Relation:
        db_ref = cls.to_db_ref(object_id=object_id)
        return Relation(db_ref, cls)

    @property
    def data(self) -> 'DictStrAny':
        return self.dict(with_props=True)

    @property
    def _query_data(self) -> 'DictStrAny':
        return self.dict(with_props=False)

    @property
    def _mongo_query_data(self) -> 'DictStrAny':
        return self._query_data

    @classmethod
    def get_collection_name(cls) -> str:
        """main method for set collection

        Returns:
            str: collection name
        """
        return cls.__collection_name__ or cls.__name__.lower()

    def serialize(self, fields: Union[Tuple, List]) -> 'DictStrAny':
        data: dict = self.dict(include=set(fields))
        return {f: data[f] for f in fields}

    def serialize_json(self, fields: Union[Tuple, List]) -> str:
        return json.dumps(self.serialize(fields))

    @property
    def pk(self):
        return self._id

    @root_validator
    def validate_all_fields(cls, values):
        for field, value in values.items():
            if isinstance(value, Document):
                raise ValueError(
                    f'{field} - cant be instance of Document without Relation'
                )
        return values


_is_document_class_defined = True
