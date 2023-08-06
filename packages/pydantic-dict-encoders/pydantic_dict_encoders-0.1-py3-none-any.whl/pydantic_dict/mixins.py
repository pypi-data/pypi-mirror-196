from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    ForwardRef,
    Optional,
    ParamSpecKwargs,
    Type,
    Union,
    cast,
)

from pydantic import BaseConfig, BaseModel

from pydantic_dict.pydantic import ExpandableExportBaseModel

if TYPE_CHECKING:
    from pydantic.typing import (
        AbstractSetIntStr,
        AnyCallable,
        MappingIntStrAny,
    )


__all__ = ("PydanticDictEncoderMixin",)


class PydanticDictEncoderMixin(ExpandableExportBaseModel):
    class Config(BaseConfig):
        # Dict encoders like json_encoders
        dict_encoders: Dict[
            Union[Type[Any], str, ForwardRef], "AnyCallable"
        ] = {}
        # To dict encoding value like json value
        jsonify_dict_encode: bool = False

    if TYPE_CHECKING:
        __config__: ClassVar[Type["Config"]] = Config

    @classmethod
    def _get_value_like_json(
        cls,
        v: Any,
        encoder: Optional[Callable[[Any], Any]] = None,
    ) -> Any:
        encoder = encoder or cls.__json_encoder__
        v = cls.__config__.json_dumps(v, default=encoder)
        if v.startswith('"'):
            return v[1:-1]
        return v

    @classmethod
    def _get_value_custom_encoder(cls, v: Any) -> Callable[[Any], Any] | None:
        for _type, encoder in cls.__config__.dict_encoders.items():
            if isinstance(v, _type):  # type: ignore
                return encoder
        return None

    @classmethod
    def _get_value_encoder_like_json(
        cls,
        v: Any,
        encoder: Optional[Callable[[Any], Any]] = None,
    ) -> Any:
        return partial(cls._get_value_like_json, encoder=encoder)

    @classmethod
    def _get_value(
        cls,
        v: Any,
        to_dict: bool,
        by_alias: bool,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]],
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]],
        exclude_unset: bool,
        exclude_defaults: bool,
        exclude_none: bool,
        **kwargs: ParamSpecKwargs,
    ) -> Any:
        encoder = None
        if cls.__config__.dict_encoders:
            encoder = cls._get_value_custom_encoder(v)
        if (
            not encoder
            and cls.__config__.jsonify_dict_encode
            and not isinstance(v, (dict, BaseModel))
        ):
            user_json_encoder = cast(
                Callable[[Any], Any] | None, kwargs.get("encoder")
            )
            encoder = cls._get_value_encoder_like_json(v, user_json_encoder)
        if cls.__config__.jsonify_dict_encode and isinstance(
            v, (PydanticDictEncoderMixin)
        ):
            v.__config__.jsonify_dict_encode = True
        if encoder:
            v = encoder(v)
        v = super()._get_value(
            v,
            to_dict,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_none,
            **kwargs,
        )
        return v
