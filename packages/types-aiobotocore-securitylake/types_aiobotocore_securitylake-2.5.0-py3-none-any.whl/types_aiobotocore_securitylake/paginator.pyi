"""
Type annotations for securitylake service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_securitylake.client import SecurityLakeClient
    from types_aiobotocore_securitylake.paginator import (
        GetDatalakeStatusPaginator,
        ListDatalakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
    )

    session = get_session()
    with session.create_client("securitylake") as client:
        client: SecurityLakeClient

        get_datalake_status_paginator: GetDatalakeStatusPaginator = client.get_paginator("get_datalake_status")
        list_datalake_exceptions_paginator: ListDatalakeExceptionsPaginator = client.get_paginator("list_datalake_exceptions")
        list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
        list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""
import sys
from typing import Generic, Iterator, Mapping, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import DimensionType, RegionType
from .type_defs import (
    GetDatalakeStatusResponseTypeDef,
    ListDatalakeExceptionsResponseTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import AsyncIterator
else:
    from typing_extensions import AsyncIterator

__all__ = (
    "GetDatalakeStatusPaginator",
    "ListDatalakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetDatalakeStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.GetDatalakeStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakestatuspaginator)
    """

    def paginate(
        self, *, accountSet: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[GetDatalakeStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.GetDatalakeStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#getdatalakestatuspaginator)
        """

class ListDatalakeExceptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListDatalakeExceptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
    """

    def paginate(
        self,
        *,
        regionSet: Sequence[RegionType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDatalakeExceptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListDatalakeExceptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listdatalakeexceptionspaginator)
        """

class ListLogSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListLogSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
    """

    def paginate(
        self,
        *,
        inputOrder: Sequence[DimensionType] = ...,
        listAllDimensions: Mapping[str, Mapping[str, Sequence[str]]] = ...,
        listSingleDimension: Sequence[str] = ...,
        listTwoDimensions: Mapping[str, Sequence[str]] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListLogSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListLogSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listlogsourcespaginator)
        """

class ListSubscribersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListSubscribers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListSubscribersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Paginator.ListSubscribers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_securitylake/paginators/#listsubscriberspaginator)
        """
