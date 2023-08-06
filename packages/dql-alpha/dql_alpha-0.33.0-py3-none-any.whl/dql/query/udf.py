from typing import TYPE_CHECKING, Any, Callable, Sequence, Tuple, Type, Union

from dql.catalog import Catalog

from .schema import Column, Object

if TYPE_CHECKING:
    from dql.dataset import DatasetRow

UDFType = Callable[["Catalog", "DatasetRow"], Any]

ColumnType = Any

# Specification for the output of a UDF, a sequence of tuples containing
# the column name and the type.
UDFOutputSpec = Sequence[Tuple[str, ColumnType]]


def udf(output: UDFOutputSpec, *parameters: Union["Column", "Object"]):
    """Decorate a function to be usable as a UDF."""

    def decorator(func: Callable):
        return UDFWrapper(func, output, *parameters)

    return decorator


class UDFWrapper:
    """A wrapper class for UDFs to be used in custom signal generation."""

    def __init__(
        self,
        func: Callable,
        output: UDFOutputSpec,
        *parameters: Union["Column", "Object"],
    ):
        self.func = func
        self.parameters = parameters
        self.output = output
        self.output_len = len(output)

    def __call__(self, catalog: "Catalog", row: "DatasetRow") -> Sequence[Any]:
        params = []
        for p in self.parameters:
            if isinstance(p, Column):
                params.append(row[p.name])
            elif isinstance(p, Object):
                with catalog.open_object(row) as f:
                    obj: Any = p.reader(f)
                params.append(obj)
            else:
                raise ValueError("unknown udf parameter")
        signals = self.func(*params)
        return signals


def generator(*parameters: Union["Column", "Object", Type["Catalog"]]):
    def decorator(func: Callable):
        return Generator(func, *parameters)

    return decorator


class Generator:
    """A wrapper class for UDFs used to generate new dataset rows."""

    def __init__(
        self, func: Callable, *parameters: Union["Column", "Object", Type["Catalog"]]
    ):
        self.func = func
        self.parameters = parameters

    def __call__(self, catalog: "Catalog", row: "DatasetRow"):
        params = []
        for p in self.parameters:
            if isinstance(p, Column):
                params.append(row[p.name])
            elif isinstance(p, Object):
                with catalog.open_object(row) as f:
                    obj: Any = p.reader(f)
                params.append(obj)
            elif p is Catalog:
                params.append(catalog)
            else:
                raise ValueError("unknown udf parameter")
        yield from self.func(row, *params)
