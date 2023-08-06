"""
Main interface for securitylake service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_securitylake import (
        Client,
        GetDatalakeStatusPaginator,
        ListDatalakeExceptionsPaginator,
        ListLogSourcesPaginator,
        ListSubscribersPaginator,
        SecurityLakeClient,
    )

    session = get_session()
    async with session.create_client("securitylake") as client:
        client: SecurityLakeClient
        ...


    get_datalake_status_paginator: GetDatalakeStatusPaginator = client.get_paginator("get_datalake_status")
    list_datalake_exceptions_paginator: ListDatalakeExceptionsPaginator = client.get_paginator("list_datalake_exceptions")
    list_log_sources_paginator: ListLogSourcesPaginator = client.get_paginator("list_log_sources")
    list_subscribers_paginator: ListSubscribersPaginator = client.get_paginator("list_subscribers")
    ```
"""
from .client import SecurityLakeClient
from .paginator import (
    GetDatalakeStatusPaginator,
    ListDatalakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)

Client = SecurityLakeClient


__all__ = (
    "Client",
    "GetDatalakeStatusPaginator",
    "ListDatalakeExceptionsPaginator",
    "ListLogSourcesPaginator",
    "ListSubscribersPaginator",
    "SecurityLakeClient",
)
