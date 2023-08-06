import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Optional,
    ParamSpecKwargs,
    Union,
    cast,
)

from pydantic import BaseModel
from pydantic.main import _missing
from pydantic.utils import ROOT_KEY, ValueItems

if TYPE_CHECKING:
    from pydantic.typing import (
        AbstractSetIntStr,
        DictStrAny,
        MappingIntStrAny,
        TupleGenerator,
    )


__all__ = ("ExpandableExportBaseModel",)


class ExpandableExportBaseModel(BaseModel):
    def dict(
        self,
        *,
        include: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        exclude: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        **kwags: ParamSpecKwargs,
    ) -> "DictStrAny":
        """
        Generate a dictionary representation of the model, optionally
        specifying which fields to include or exclude and custom encoding
        like json.

        *Copied from pydantic BaseModel.dict for extend export model to dict*
        """
        if skip_defaults is not None:
            warnings.warn(
                (
                    f'{self.__class__.__name__}.dict(): "skip_defaults"'
                    f'is deprecated and replaced by "exclude_unset"'
                ),
                DeprecationWarning,
            )
            exclude_unset = skip_defaults

        return dict(
            self._iter(
                to_dict=True,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                **kwags,
            )
        )

    def json(
        self,
        *,
        include: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        exclude: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        encoder: Optional[Callable[[Any], Any]] = None,
        models_as_dict: bool = True,
        **dumps_kwargs: Any,
    ) -> str:
        """
        Generate a JSON representation of the model,
        `include` and `exclude` arguments as per `dict()`.

        `encoder` is an optional function to supply as `default`
        to json.dumps(), other arguments as per `json.dumps()`.

        *Copied from pydantic BaseModel.json for extend export model to json*
        """
        if skip_defaults is not None:
            warnings.warn(
                (
                    f'{self.__class__.__name__}.json():'
                    f' "skip_defaults" is deprecated and replaced'
                    f' by "exclude_unset"'
                ),
                DeprecationWarning,
            )
            exclude_unset = skip_defaults
        encoder = cast(Callable[[Any], Any], encoder or self.__json_encoder__)

        # We don't directly call `self.dict()`, which does exactly this with `to_dict=True`  # noqa: E501
        # because we want to be able to keep raw `BaseModel` instances and not as `dict`.  # noqa: E501
        # This allows users to write custom JSON encoders for given `BaseModel` classes.  # noqa: E501
        data = dict(
            self._iter(
                to_dict=models_as_dict,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                **dumps_kwargs,
            )
        )
        if self.__custom_root_type__:
            data = data[ROOT_KEY]
        return self.__config__.json_dumps(
            data, default=encoder, **dumps_kwargs
        )

    def _iter(
        self,
        to_dict: bool = False,
        by_alias: bool = False,
        include: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        exclude: Optional[
            Union["AbstractSetIntStr", "MappingIntStrAny"]
        ] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        **kwags: ParamSpecKwargs,
    ) -> "TupleGenerator":
        """
        Copied from pydantic BaseModel._iter
        for forward kwargs to _get_value method
        """

        # Merge field set excludes with explicit exclude parameter with explicit overriding field set options.  # noqa: E501
        # The extra "is not None" guards are not logically necessary but optimizes performance for the simple case.  # noqa: E501
        if exclude is not None or self.__exclude_fields__ is not None:
            exclude = ValueItems.merge(self.__exclude_fields__, exclude)

        if include is not None or self.__include_fields__ is not None:
            include = ValueItems.merge(
                self.__include_fields__, include, intersect=True
            )

        allowed_keys = self._calculate_keys(
            include=include, exclude=exclude, exclude_unset=exclude_unset  # type: ignore  # noqa: E501
        )
        if allowed_keys is None and not (
            to_dict
            or by_alias
            or exclude_unset
            or exclude_defaults
            or exclude_none
        ):
            # huge boost for plain _iter()
            yield from self.__dict__.items()
            return

        value_exclude = (
            ValueItems(self, exclude) if exclude is not None else None
        )
        value_include = (
            ValueItems(self, include) if include is not None else None
        )

        for field_key, v in self.__dict__.items():
            if (
                allowed_keys is not None and field_key not in allowed_keys
            ) or (exclude_none and v is None):
                continue

            if exclude_defaults:
                model_field = self.__fields__.get(field_key)
                if (
                    not getattr(model_field, "required", True)
                    and getattr(model_field, "default", _missing) == v
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
                    include=value_include and value_include.for_element(field_key),  # type: ignore  # noqa: E501
                    exclude=value_exclude and value_exclude.for_element(field_key),  # type: ignore  # noqa: E501
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    **kwags,
                )
            yield dict_key, v

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
        **kwags: ParamSpecKwargs,
    ) -> Any:
        return super()._get_value(
            v,
            to_dict,
            by_alias,
            include,
            exclude,
            exclude_unset,
            exclude_defaults,
            exclude_none,
        )
