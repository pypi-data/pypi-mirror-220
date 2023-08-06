from typing import Any, Union, Optional, Tuple, TYPE_CHECKING

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from .types import ObjectIdStr, UUID
from .exceptions import MotordanticValidationError


__all__ = ('validate_field_value', 'sort_validation')

if TYPE_CHECKING:
    from .document import Document
    from .typing import DocumentType


def validate_field_value(
    document: Union['Document', 'DocumentType'], field_name: str, value: Any
) -> Any:
    """extra helper value validation

    Args:
        cls ('Document'): mongo document class
        field_name (str): name of field
        value (Any): value

    Raises:
        AttributeError: if not field in __fields__
        MongoValidationError: if invalid value type

    Returns:
        Any: value
    """
    if field_name == '_id':
        field = ObjectIdStr()  # type: ignore
    else:
        field = document.__fields__.get(field_name)  # type: ignore
    error_ = None
    if isinstance(field, ObjectIdStr):
        try:
            value = field.validate(value)
        except ValueError as e:
            error_ = ErrorWrapper(e, str(e))
    elif not field:
        raise AttributeError(f'invalid field - {field_name}')
    else:
        value, error_ = field.validate(value, {}, loc=field.alias, cls=document)  # type: ignore
    if error_:
        pydantic_validation_error = ValidationError([error_], document)  # type: ignore
        raise MotordanticValidationError(
            pydantic_validation_error.errors(), pydantic_validation_error
        )
    if field_name in document.__db_refs__:  # type: ignore
        if isinstance(value, list):
            s = [v.to_ref() for v in value]
            return s
        return value.to_ref() if value else None
    elif isinstance(value, UUID):
        return value.hex
    else:
        return value.dict() if isinstance(value, BaseModel) else value


def sort_validation(
    sort: Optional[int] = None, sort_fields: Union[list, tuple, None] = None
) -> Tuple[Any, ...]:
    if sort is not None:
        if sort not in (1, -1):
            raise ValueError(f'invalid sort value must be 1 or -1 not {sort}')
        if not sort_fields:
            sort_fields = ('_id',)
    return sort, sort_fields


def validate_object_id(document: 'Document', value: str) -> ObjectId:
    try:
        o_id = ObjectId(value)
    except InvalidId as e:
        error_ = ErrorWrapper(e, str(e))
        pydantic_validation_error = ValidationError([error_], document)  # type: ignore
        raise MotordanticValidationError(
            pydantic_validation_error.errors(), pydantic_validation_error
        )
    return o_id
