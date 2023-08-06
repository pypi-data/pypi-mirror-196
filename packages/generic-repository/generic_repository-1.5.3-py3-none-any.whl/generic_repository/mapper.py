# pylint: disable=import-error
"""
Data mappers.

These constructs are used to apply data transformations in various places.
"""
import abc
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import ParamSpec

_MapperParams = ParamSpec("_MapperParams")
_In = TypeVar("_In")
_Out = TypeVar("_Out")
_New = TypeVar("_New")
_Left = TypeVar("_Left")
_Right = TypeVar("_Right")
_FuncParams = ParamSpec("_FuncParams")


class Mapper(Generic[_In, _Out], abc.ABC):
    """A mapper abstract class.

    Example:
    >>> class MultiplyMapper(Mapper):
    ...     def map_item(self, num, **kwargs):
    ...         return num*2
    ...
    >>> mapper=MultiplyMapper()
    >>> mapper(2)
    4
    >>> mapper(5)
    10
    >>> mapper.reverse_map(4)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NotImplementedError: ...
    """

    def __call__(self, value: _In) -> _Out:
        """Process the input argument.

        Args:
            input: The object being processed.

        Returns:
            _Out: The resulting object.
        """
        return self.map_item(value)

    @abc.abstractmethod
    def map_item(self, item: _In) -> _Out:
        """Maps an item to it's output representation.

        Args:
            item (_In): The item to map.

        Returns:
            _Out: The output representation.
        """

    def reverse_map(self, out: _Out) -> _In:
        """Reverse the mapping process.

        Args:
            out (_Out): The output to reverse map.

        Returns:
            _In: The input representation.
        """
        raise NotImplementedError("Not implemented.")

    def chain(self, mapper: "Mapper[_Out, _New]") -> "Mapper[_In,_New]":
        """Chain another mapper to this.

        >>> mapper=(
        ...     LambdaMapper(lambda x: x*2, lambda x: x/2)
        ...     .chain(LambdaMapper(lambda x: x*2, lambda x: x/2))
        ... )
        >>> mapper(3)
        12
        >>> mapper.reverse_map(12)
        3.0

        You can also chain a mapper instance:
        >>> mapper2=mapper.chain(LambdaMapper(lambda x: x*2, lambda x: x/2))
        >>> mapper2(3)
        24
        >>> mapper2.reverse_map(24)
        3.0

        Raises if any other type is provided.
        >>> mapper.chain('x')
        Traceback (most recent call last):
          ...
        TypeError: ...
        >>>
        """
        return DecoratedMapper(self, mapper)

    def chain_lambda(
        self,
        func: Callable[[_Out], _New],
        reverse_func: Optional[Callable[[_New], _Out]] = None,
    ) -> "Mapper[_In, _New]":
        """Chain a lambda function and a reverse function.

        Args:
            func (Callable[[_Out], _New]): The function to chain
            reverse_func (Optional[Callable[[_New], _Out]], optional): The reverse
                function. Defaults to None.

        Returns:
            Mapper[_In, _New]: The resulting mapper

        Example:
        >>> mapper = LambdaMapper(lambda x: x*2, lambda x: x/2)
        >>> mapper2 = mapper.chain_lambda(lambda x: x*3, lambda x: x/3)
        >>> mapper2(3)
        18
        """
        return self.chain(LambdaMapper(func, reverse_func))

    def __invert__(self) -> "Mapper[_Out, _In]":
        """Return the inverse mapper.

        Returns:
            Mapper[_Out, _In]: A mapper doing the reverse operation.

        For example, this inverts the lambda operation.
        >>> mapper = ~LambdaMapper(lambda x: x*2, lambda x: x/2)
        >>> mapper(4)
        2.0
        >>> reversed_mapper = ~mapper # (Reverse the mapper)
        >>> reversed_mapper(4)
        8
        >>>
        """
        return InverseMapper(self)

    def __rshift__(
        self, other: "Mapper[_Left, _In]"
    ) -> "Mapper[_Left, _Out]":  # pragma nocover
        """Chain this mapper to the right of the other.

        Args:
            other (Mapper[_New, _In]): The mapper to chain to the left.

        Returns:
            Mapper[_New, _Out]: The mapper chain.
        """
        return other.chain(self)  # type: ignore

    def __lshift__(
        self, other: "Mapper[_Out, _Right]"
    ) -> "Mapper[_In, _Right]":  # pragma nocover
        """Chain this mapper to the left of the other.

        Args:
            other: The mapper to prepend.

        Returns:
            Mapper[_New, _Out]: The mapper chain.
        """
        return self.chain(other)  # type: ignore

    @staticmethod
    def identity() -> "Mapper[_In, _In]":  # pragma nocover
        """The identity mapper."""
        return LambdaMapper[_In, _In](lambda x: x, lambda x: x)


class LambdaMapper(Mapper[_In, _Out]):
    """A lambda-powered mapper.

    A multiply mapper can be defined as follows:
    >>> mapper=LambdaMapper(lambda x: x*3, lambda x: x/3)

    Example call:
    >>> mapper(4)
    12
    >>> mapper.reverse_map(15)
    5.0

    If the `reverse_func` param is not provided, a `NotImplementedError` is raised.
    >>> mapper2 = LambdaMapper(lambda x: x*3)
    >>> mapper2.reverse_map(3)
    Traceback (most recent call last):
      ...
    NotImplementedError: ...

    A multiply x*n mapper can be defined as follows:
    >>> mapper3 = LambdaMapper(
    ...     lambda x, *, n: x*n,
    ...     lambda x, *, n: x/n,
    ...     n=5,
    ... )
    >>> mapper3(4)
    20
    >>> mapper3.reverse_map(20)
    4.0
    """

    def __init__(
        self,
        func: Callable[[_In], _Out],
        reverse_func: Optional[Callable[[_Out], _In]] = None,
        **kwargs: Any
    ) -> None:
        super().__init__()
        self.func = func
        self.reverse_func = reverse_func
        self.mapper_kwargs = kwargs

    def map_item(self, item: _In) -> _Out:
        return self.func(item, **self.mapper_kwargs)

    def reverse_map(self, out: _Out) -> _In:
        if self.reverse_func is not None:
            return self.reverse_func(out, **self.mapper_kwargs)
        return super().reverse_map(out)


_Obj = TypeVar("_Obj")


class _Arguments(NamedTuple):
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]


class ToFunctionArgsMapper(Mapper[Union[Dict[str, Any], Sequence[Any]], _Arguments]):
    """Maps a dict to kwargs part of a function call.

    Example:
    >>> mapper=ToFunctionArgsMapper()

    >>> mapper({'x':3})
    _Arguments(args=(), kwargs={'x': 3})
    >>> mapper([3])
    _Arguments(args=(3,), kwargs={})
    >>> mapper({3})
    _Arguments(args=(3,), kwargs={})
    >>> mapper((3,))
    _Arguments(args=(3,), kwargs={})
    >>> mapper('x')
    Traceback (most recent call last):
      ...
    TypeError: ...
    >>>
    """

    def __init__(self, **default_kwargs: Any) -> None:
        super().__init__()
        self.default_kwargs = default_kwargs

    def map_item(self, item: Union[Dict[str, Any], Sequence[Any]]) -> _Arguments:
        args: List[Any] = []
        kwargs: Dict[str, Any] = {}
        kwargs.update(self.default_kwargs)
        if isinstance(item, dict):
            kwargs.update(item)
        elif isinstance(item, (tuple, list, set)):
            args.extend(item)
        else:
            raise TypeError("Type not supported.")

        return _Arguments(tuple(args), kwargs)

    def reverse_map(self, out: _Arguments) -> Union[Tuple[Any, ...], Dict[str, Any]]:
        """Perform the reverse map of the arguments.

        Args:
            out (_Arguments): The arguments to be reversed

        Returns:
            Union[tuple, Dict[str, Any]]: The resulting arguments.

        >>> mapper= ~ToFunctionArgsMapper()
        >>> mapper(_Arguments((5, 3), {}))
        (5, 3)

        >>> mapper(_Arguments((), {'x': 3}))
        {'x': 3}
        """
        if len(out.args) > 0:
            return out.args
        return out.kwargs


class ConstructorMapper(Mapper[_Arguments, _Obj], Generic[_Obj]):
    """A from-args to object mapper.

    Example:
    >>> from dataclasses import dataclass

    >>> @dataclass()
    ... class Point:
    ...     x: int
    ...     y: int
    ...
    >>> mapper=ConstructorMapper(Point)

    >>> mapper(((4, 5),{}))
    Point(x=4, y=5)
    >>> mapper(((4,),{'y': 5}))
    Point(x=4, y=5)
    >>> mapper(((),{'y': 5,'x':4}))
    Point(x=4, y=5)

    Non-clas objects are not accepted:
    >>> mapper2 = ConstructorMapper(lambda x, y: (x, y))
    Traceback (most recent call last):
      ...
    AssertionError: ...
    """

    def __init__(self, cls: Type[_Obj], **default_kwargs: Any) -> None:
        super().__init__()
        if not isinstance(cls, type):
            raise AssertionError("The provided object is not a valid class.")
        self.cls = cls
        self._default_kw = default_kwargs

    def map_item(self, item: _Arguments) -> _Obj:
        args, kwargs = item
        kwargs = {**self._default_kw, **kwargs}
        return self.cls(*args, **kwargs)  # type: ignore


_Intermediate = TypeVar("_Intermediate")


class DecoratedMapper(Mapper[_In, _Out]):
    """Wraps two other mappers, effectively producing a binaary tree of mappers.

    Example:
    >>> left = LambdaMapper(lambda x: x*2, lambda x: x/2)
    >>> right = LambdaMapper(lambda x: x*3, lambda x: x/3)
    >>> decorated = DecoratedMapper(left, right)
    >>> decorated(2)
    12
    >>> decorated.reverse_map(12)
    2.0

    But non-mapper instances are not accepted:
    >>> class FakeMapper:
    ...     pass
    ...
    >>> decorated2=DecoratedMapper(left, FakeMapper())
    Traceback (most recent call last):
      ...
    TypeError: ...
    >>> decorated2=DecoratedMapper(FakeMapper(), right)
    Traceback (most recent call last):
      ...
    TypeError: ...
    >>>
    """

    def __init__(
        self, first: Mapper[_In, _Intermediate], second: Mapper[_Intermediate, _Out]
    ) -> None:
        super().__init__()
        if not isinstance(first, Mapper):  # type: ignore
            raise TypeError("`first` parameter is not a mapper instance.")

        if not isinstance(second, Mapper):  # type: ignore
            raise TypeError("`second` is not a mapper instance.")

        self.first, self.second = first, second

    def map_item(self, item: _In) -> _Out:
        return self.second.map_item(self.first.map_item(item))

    def reverse_map(self, out: _Out) -> _In:
        return self.first.reverse_map(self.second.reverse_map(out))


class InverseMapper(Mapper[_Out, _In], Generic[_In, _Out]):
    """A reverse mapper.

    This performs the inverse operation from the given mapper by calling the
    `reverse_map` method.

    Normally, this is not instantiated directly. Insthead, use the `inverse` operator.
    """

    def __init__(self, mapper: Mapper[_In, _Out]) -> None:
        super().__init__()
        self.mapper = mapper

    def map_item(self, item: _Out) -> _In:
        return self.mapper.reverse_map(item)

    def reverse_map(self, out: _In) -> _Out:
        return self.mapper.map_item(out)
