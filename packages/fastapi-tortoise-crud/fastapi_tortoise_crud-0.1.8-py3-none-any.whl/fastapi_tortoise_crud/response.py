from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel, BaseModel

_T = TypeVar('_T')


class BaseApiOut(GenericModel, Generic[_T], BaseModel):
    message: str = '请求成功'
    data: Optional[_T] = None
    code: int = 200


__all__ = [
    'BaseApiOut',
]
