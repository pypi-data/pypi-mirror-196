import dataclasses
import math
from typing import Iterable, Iterator, Optional, TypeVar

import torch

from ._utils import deprecated, is_namedtuple

T = TypeVar('T')
K = TypeVar('K')


def to(data: T, *args, **kwargs) -> T:
    """Like `torch.Tensor.to`, but for collections of tensors.

    The function takes a (nested) collection of tensors
    and creates its copy where all the tensors are transformed
    with `torch.Tensor.to`.

    Args:
        data: the tensor or the (nested) collection of tensors. Allowed collections
            include: (named)tuples, lists, dictionaries and dataclasses.
            For dataclasses, all their fields must be tensors.
        args: the positional arguments for `torch.Tensor.to`
        kwargs: the key-word arguments for `torch.Tensor.to`
    Returns:
        transformed data.

    Examples:
        .. testcode::

            # in practice, this can be 'cuda' or any other device
            device = torch.device('cpu')
            tensor = torch.tensor

            x = tensor(0)
            x = delu.to(x, dtype=torch.float, device=device)

            batch = {
                'x': tensor([0.0, 1.0]),
                'y': tensor([0, 1]),
            }
            batch = delu.to(batch, device)

            x = [
                tensor(0.0),
                {'a': tensor(1.0), 'b': tensor(2.0)},
                (tensor(3.0), tensor(4.0))
            ]
            x = delu.to(x, torch.half)
    """

    def TO_(x):
        return to(x, *args, **kwargs)

    # mypy does not understand what is going on here, hence a lot of "type: ignore"
    if isinstance(data, torch.Tensor):
        return data.to(*args, **kwargs)  # type: ignore
    elif isinstance(data, (tuple, list)):
        constructor = type(data)._make if is_namedtuple(data) else type(data)  # type: ignore  # noqa: E501
        return constructor(TO_(x) for x in data)  # type: ignore
    elif isinstance(data, dict):
        return type(data)((k, TO_(v)) for k, v in data.items())  # type: ignore
    elif dataclasses.is_dataclass(data):
        return type(data)(**{k: TO_(v) for k, v in vars(data).items()})  # type: ignore
    else:
        raise ValueError(
            f'the input contains an object of the unsupported type {type(data)}.'
            ' See the documentation for details'
        )


def cat(iterable: Iterable[T], dim: int = 0) -> T:
    """Like `torch.cat`, but for collections of tensors.

    The function is especially useful for concatenating outputs of a function or a model
    that returns not a single tensor, but a (named)tuple/dictionary/dataclass
    of tensors. For example::

        class Model(nn.Module):
            ...
            def forward(...) -> tuple[Tensor, Tensor]:
                ...
                return y_pred, embeddings

        model = Model(...)
        dataset = Dataset(...)
        dataloader = DataLoader(...)

        # prediction
        model.eval()
        with torch.inference_mode():
            # Concatenate a sequence of tuples into a single tuple.
            y_pred, embeddings = delu.cat(model(batch) for batch in dataloader)
        assert isinstance(y_pred, torch.Tensor) and len(y_pred) == len(dataset)
        assert isinstance(embeddings, torch.Tensor) and len(embeddings) == len(dataset)

    See other examples below.

    Note:
        Under the hood, roughly speaking, the function "transposes" the sequence of
        collections to a collection of sequences and applies `torch.cat` to those
        sequencies.

    Args:
        iterable: the iterable of (named)tuples/dictionaries/dataclasses of tensors.
            All items of the iterable must be of the same type and have the same
            structure (tuples must be of the same length, dictionaries must have the
            same keys, dataclasses must have the same fields). Dataclasses must have
            only tensor-valued fields.
        dim: the argument for `torch.cat`.
    Returns:
        Concatenated items of the iterable.
    Raises:
        ValueError: if the iterable is empty or contains unsupported collections.

    See also:
        `delu.iter_batches`

    Examples:
        Below, only one-dimensional data and dim=0 are considered for simplicity.

        .. testcode::

            tensor = torch.tensor

            batches = [
                # (batch0_x,         batch0_y)
                (tensor([0.0, 1.0]), tensor([[0], [1]])),

                # (batch1_x,         batch1_y)
                (tensor([2.0, 3.0]), tensor([[2], [3]])),

                # ...
            ]
            # result = (x, y)
            result = delu.cat(batches)
            assert isinstance(result, tuple) and len(result) == 2
            assert torch.equal(result[0], tensor([0.0, 1.0, 2.0, 3.0]))
            assert torch.equal(result[1], tensor([[0], [1], [2], [3]]))

            batches = [
                {'x': tensor([0.0, 1.0]), 'y': tensor([[0], [1]])},
                {'x': tensor([2.0, 3.0]), 'y': tensor([[2], [3]])},
            ]
            result = delu.cat(batches)
            assert isinstance(result, dict) and set(result) == {'x', 'y'}
            assert torch.equal(result['x'], tensor([0.0, 1.0, 2.0, 3.0]))
            assert torch.equal(result['y'], tensor([[0], [1], [2], [3]]))

            from dataclasses import dataclass
            @dataclass
            class Data:
                # all fields must be tensors
                x: torch.Tensor
                y: torch.Tensor

            batches = [
                Data(tensor([0.0, 1.0]), tensor([[0], [1]])),
                Data(tensor([2.0, 3.0]), tensor([[2], [3]])),
            ]
            result = delu.cat(batches)
            assert isinstance(result, Data)
            assert torch.equal(result.x, tensor([0.0, 1.0, 2.0, 3.0]))
            assert torch.equal(result.y, tensor([[0], [1], [2], [3]]))

            x = tensor([0.0, 1.0, 2.0, 3.0, 4.0])
            y = tensor([[0], [10], [20], [30], [40]])
            batch_size = 2
            ab = delu.cat(delu.iter_batches((x, y), batch_size))
            assert torch.equal(ab[0], x)
            assert torch.equal(ab[1], y)
    """
    data = iterable if isinstance(iterable, list) else list(iterable)
    if not data:
        raise ValueError('iterable must be non-empty.')

    def tcat(x):
        return torch.cat(x, dim=dim)

    first = data[0]
    if isinstance(first, torch.Tensor):
        raise ValueError(
            'Use torch.cat instead of delu.cat for concatenating a sequence of tensors.'
            ' Use delu.cat when concatenating a sequence of collections of tensors.'
        )
    elif isinstance(first, tuple):
        constructor = type(first)._make if is_namedtuple(first) else type(first)  # type: ignore  # noqa: E501
        return constructor(tcat([x[i] for x in data]) for i in range(len(first)))
    elif isinstance(first, dict):
        return type(first)((key, tcat([x[key] for x in data])) for key in first)  # type: ignore  # noqa: E501
    elif dataclasses.is_dataclass(first):
        fields = {}
        for field in dataclasses.fields(first):
            if field.type is not torch.Tensor:
                raise ValueError(
                    f'All dataclass fields must be PyTorch Tensors. Found {field.type}'
                )
            fields[field.name] = tcat([getattr(x, field.name) for x in data])
        return type(first)(**fields)
    else:
        raise ValueError(f'The collection type {type(first)} is not supported.')


@deprecated('Instead, use `delu.cat`')
def concat(*args, **kwargs):
    """"""
    return cat(*args, **kwargs)


def iter_batches(
    data: T,
    batch_size: int,
    shuffle: bool = False,
    *,
    generator: Optional[torch.Generator] = None,
    drop_last: bool = False,
) -> Iterator[T]:
    """Iterate over tensor or collection of tensors by (random) batches.

    The function makes batches over the first dimension of the tensors in ``data``
    and returns an iterator over collections of the same type as the input.

    Args:
        data: the tensor or the collection ((named)tuple/dict/dataclass) of tensors.
            If data is a collection, then the tensors must have the same first
            dimension. If data is a dataclass, then all its fields must be tensors.
        batch_size: the batch size. If ``drop_last`` is False, then the last batch can
            be smaller than ``batch_size``.
        shuffle: if True, iterate over random batches (without replacement),
            not sequentially.
        generator: the argument for `torch.randperm` when ``shuffle`` is True.
        drop_last: same as the ``drop_last`` argument for `torch.utils.data.DataLoader`.
            When True and the last batch is smaller then ``batch_size``, then this last
            batch is not returned.
    Returns:
        Iterator over batches.
    Raises:
        ValueError: if the data is empty.

    Note:
        The function lazily indexes to the provided input with batches of indices.
        This works faster than iterating over the tensors in ``data`` with
        `torch.utils.data.DataLoader`.

    See also:
        - `delu.cat`

    Examples:
        .. code-block::

            for epoch in range(n_epochs):
                for batch in delu.iter_batches(data, batch_size, shuffle=True)):
                    ...

        .. testcode::

            a = torch.tensor([0.0, 1.0, 2.0, 3.0, 4.0])
            b = torch.tensor([[0], [10], [20], [30], [40]])
            batch_size = 2

            for batch in delu.iter_batches(a, batch_size):
                assert isinstance(batch, torch.Tensor)
            for batch in delu.iter_batches((a, b), batch_size):
                assert isinstance(batch, tuple) and len(batch) == 2
            for batch in delu.iter_batches({'a': a, 'b': b}, batch_size):
                assert isinstance(batch, dict) and set(batch) == {'a', 'b'}

            from dataclasses import dataclass
            @dataclass
            class Data:
                a: torch.Tensor
                b: torch.Tensor

            for batch in delu.iter_batches(Data(a, b), batch_size):
                assert isinstance(batch, Data)

            ab = delu.cat(delu.iter_batches((a, b), batch_size))
            assert torch.equal(ab[0], a)
            assert torch.equal(ab[1], b)

            n_batches = len(list(delu.iter_batches((a, b), batch_size)))
            assert n_batches == 3
            n_batches = len(list(delu.iter_batches((a, b), batch_size, drop_last=True)))
            assert n_batches == 2
    """
    if not shuffle and generator is not None:
        raise ValueError('When shuffle is False, generator must be None.')

    if isinstance(data, torch.Tensor):
        if not len(data):
            raise ValueError('data must be non-empty')
        item = data
        get_batch = data.__getitem__
    elif isinstance(data, tuple):
        if not data:
            raise ValueError('data must be non-empty')
        item = data[0]
        if any(len(x) != len(item) for x in data):
            raise ValueError('All tensors must have the same first dimension.')
        constructor = type(data)._make if is_namedtuple(data) else type(data)  # type: ignore  # noqa: E501
        get_batch = lambda idx: constructor(x[idx] for x in data)  # type: ignore  # noqa: E731,E501
    elif isinstance(data, dict):
        if not data:
            raise ValueError('data must be non-empty')
        item = next(iter(data.values()))
        if any(len(x) != len(item) for x in data.values()):
            raise ValueError('All tensors must have the same first dimension.')
        get_batch = lambda idx: type(data)({k: v[idx] for k, v in data.items()})  # type: ignore # noqa: E731,E501
    elif dataclasses.is_dataclass(data):
        fields = list(dataclasses.fields(data))
        if not fields:
            raise ValueError('data must be non-empty')
        item = getattr(data, fields[0].name)
        for field in fields:
            if field.type is not torch.Tensor:
                raise ValueError('All dataclass fields must be tensors')
            if len(getattr(data, field.name)) != len(item):
                raise ValueError('All tensors must have the same first dimension.')
        get_batch = lambda idx: type(data)(  # type: ignore  # noqa: E731
            **{field.name: getattr(data, field.name)[idx] for field in fields}
        )
    else:
        raise ValueError(f'The collection {type(data)} is not supported.')

    size = len(item)
    device = item.device
    n_batches = math.ceil(size / batch_size)
    for i, idx in enumerate(
        (
            torch.randperm(size, generator=generator, device=device)
            if shuffle
            else torch.arange(size, device=device)
        ).split(batch_size)
    ):
        if i + 1 == n_batches and len(idx) < batch_size and drop_last:
            return
        yield get_batch(idx)  # type: ignore
