from typing import Optional, TypeVar, Generic, Union, TYPE_CHECKING
from enum import Enum
from uuid import UUID

from bson import ObjectId, DBRef
from bson.errors import InvalidId
from pydantic import parse_obj_as, BaseModel
from pydantic.fields import ModelField
from pydantic.json import ENCODERS_BY_TYPE

from .typing import DocumentType

__all__ = (
    'ObjectIdStr',
    'UUIDField',
    'Relation',
    'RelationInfo',
    'RelationTypes',
)

if TYPE_CHECKING:
    from .document import Document

T = TypeVar("T")


class ObjectIdStr(str):
    """Field for validate string like ObjectId"""

    type_ = ObjectId
    required = False
    default = None
    validate_always = False
    alias = ''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError(f"invalid ObjectId - {v}")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UUIDField(str):
    """Field for validate string like UUID"""

    type_ = UUID
    required = False
    default = None
    validate_always = False
    alias = ''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str) -> UUID:
        if isinstance(v, UUID):
            return v
        try:
            return UUID(str(v))
        except ValueError:
            raise ValueError(f"invalid UUID - {v}")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class RelationTypes(str, Enum):
    SINGLE = "SINGLE"
    OPTIONAL_SINGLE = "OPTIONAL_SINGLE"
    ARRAY = "ARRAY"


class RelationInfo(BaseModel):
    field: str
    document_class: DocumentType
    relation_type: RelationTypes


class Relation(Generic[T]):
    def __init__(self, db_ref: DBRef, document_class: DocumentType):
        self.db_ref = db_ref
        self.document_class = document_class

    async def get(self) -> Optional["Document"]:
        result = await self.document_class.Q.find_one(_id=self.db_ref.id, with_relations_objects=True)  # type: ignore
        return result

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def _validate_for_model(
        cls, v: Union[dict, BaseModel], document_class: DocumentType
    ) -> 'Relation':
        parsed = (
            document_class.parse_obj(v)
            if isinstance(v, dict)
            else document_class.validate(v)
        )
        new_id = (
            parsed._id
            if isinstance(parsed._id, ObjectId)
            else parse_obj_as(
                ObjectIdStr,
                parsed._id,  # type: ignore
            )
        )
        db_ref = DBRef(collection=document_class.get_collection_name(), id=new_id)
        return cls(db_ref=db_ref, document_class=document_class)

    @classmethod
    def validate(cls, v: Union[DBRef, T], field: ModelField) -> 'Relation':
        document_class = field.sub_fields[0].type_  # type: ignore
        if isinstance(v, DBRef):
            return cls(db_ref=v, document_class=document_class)
        if isinstance(v, Relation):
            return v
        if isinstance(v, dict):
            try:
                return cls(db_ref=DBRef(**v), document_class=document_class)
            except TypeError:
                return cls._validate_for_model(v, document_class)
        if isinstance(v, BaseModel):
            return cls._validate_for_model(v, document_class)
        raise ValueError(f'invalod type - {v}')

    def to_ref(self) -> DBRef:
        return self.db_ref

    def to_dict(self) -> dict:
        return {"id": str(self.db_ref.id), "collection": self.db_ref.collection}

    @property
    def data(self) -> dict:
        return self.to_dict()


ENCODERS_BY_TYPE[Relation] = lambda r: r.to_dict()
ENCODERS_BY_TYPE[ObjectIdStr] = lambda o: str(o)
