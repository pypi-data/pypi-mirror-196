"""
Type annotations for pipes service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pipes.client import EventBridgePipesClient
    from types_aiobotocore_pipes.paginator import (
        ListPipesPaginator,
    )

    session = get_session()
    with session.create_client("pipes") as client:
        client: EventBridgePipesClient

        list_pipes_paginator: ListPipesPaginator = client.get_paginator("list_pipes")
    ```
"""
import sys
from typing import Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import PipeStateType, RequestedPipeStateType
from .type_defs import ListPipesResponseTypeDef, PaginatorConfigTypeDef

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = ("ListPipesPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListPipesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Paginator.ListPipes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
    """

    def paginate(
        self,
        *,
        CurrentState: PipeStateType = ...,
        DesiredState: RequestedPipeStateType = ...,
        NamePrefix: str = ...,
        SourcePrefix: str = ...,
        TargetPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListPipesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pipes.html#EventBridgePipes.Paginator.ListPipes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pipes/paginators/#listpipespaginator)
        """
