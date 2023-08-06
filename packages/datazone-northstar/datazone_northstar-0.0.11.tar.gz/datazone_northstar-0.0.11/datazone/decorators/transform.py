from typing import Optional, List, Callable, Any

from datazone.core.transform import _Transform


def transform(
    compute_fn: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    input_mapping: Optional[dict] = None,
    output_mapping: Optional[dict] = None,
    materialized: Optional[bool] = False,
    tags: Optional[List] = None
):
    def create_transform():
        return _Transform(
            name=name or compute_fn.__name__,
            description=description,
            input_mapping=input_mapping,
            output_mapping=output_mapping,
            materialized=materialized,
            tags=tags,
        )

    if compute_fn is not None:
        return create_transform()(compute_fn)

    def inner(fn: Callable[..., Any]):
        if fn is not None:
            return create_transform()(fn)

    return inner
