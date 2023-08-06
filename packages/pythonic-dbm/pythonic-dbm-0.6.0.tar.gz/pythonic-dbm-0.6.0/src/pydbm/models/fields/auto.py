from __future__ import annotations

import hashlib
import typing

from pydbm import contstant as C
from pydbm.models.fields.base import BaseField

if typing.TYPE_CHECKING:
    from pydbm.models.base import DbmModel
    from pydbm.typing_extra import SupportedClassT

__all__ = (
    "AutoField",
)

Self = typing.TypeVar("Self", bound="AutoField")  # unexport: not-public


class AutoField(BaseField):
    __slots__ = (
        "unique_together",
        "fields",
    )

    def __init__(self, field_name: str, field_type: SupportedClassT, *, unique_together: tuple[str, ...] | None = None, **kwargs) -> None:  # noqa: E501
        self.field_name = field_name
        self.field_type = field_type

        self.public_name = field_name
        self.private_name = "_" + field_name

        self.unique_together = unique_together if unique_together is not None else ()
        super().__init__(default_factory=self.generate_id, **kwargs)

    def __set__(self, instance: DbmModel, value: typing.Any) -> None:
        if (fields := getattr(instance, "fields", None)) is not None and C.PRIMARY_KEY not in fields:
            return super().__set__(instance, value)

    def __call__(self: Self, fields: dict[str, typing.Any] | None = None, *args, **kwargs) -> Self:  # type: ignore[valid-type, override]  # noqa: E501
        if fields is not None:
            _fields = fields.copy()
            _fields.pop(C.PRIMARY_KEY, None)
        else:
            _fields = None

        if self.unique_together and not _fields:
            raise ValueError("unique_together ise set, fields must be passed")

        self.fields = _fields
        return super().__call__(self.field_name, self.field_type, *args, **kwargs)  # type: ignore

    def generate_id(self) -> str:
        if self.unique_together and self._is_call_run:
            text = "*".join(map(str, (attr for name in self.unique_together if (attr := self.fields.get(name, None)))))
            return hashlib.md5(bytes(text, "utf-8")).hexdigest()
        else:  # TODO: disable all behaviors
            return __import__("uuid").uuid4().hex
