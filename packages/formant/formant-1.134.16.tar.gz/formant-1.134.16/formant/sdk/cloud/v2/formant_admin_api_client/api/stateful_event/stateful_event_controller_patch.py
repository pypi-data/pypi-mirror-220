from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ...client import AuthenticatedClient
from ...models.partial_stateful_event import PartialStatefulEvent
from ...models.stateful_event import StatefulEvent
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    json_body: PartialStatefulEvent,
) -> Dict[str, Any]:
    url = "{}/stateful-events".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "patch",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[StatefulEvent]:
    if response.status_code == HTTPStatus.CREATED:
        response_201 = StatefulEvent.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[StatefulEvent]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PartialStatefulEvent,
) -> Response[StatefulEvent]:
    """Patch

     Create or update a stateful event
    Resource: events
    Authorized roles: device

    Args:
        json_body (PartialStatefulEvent):

    Returns:
        Response[StatefulEvent]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    json_body: PartialStatefulEvent,
) -> Optional[StatefulEvent]:
    """Patch

     Create or update a stateful event
    Resource: events
    Authorized roles: device

    Args:
        json_body (PartialStatefulEvent):

    Returns:
        Response[StatefulEvent]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    json_body: PartialStatefulEvent,
) -> Response[StatefulEvent]:
    """Patch

     Create or update a stateful event
    Resource: events
    Authorized roles: device

    Args:
        json_body (PartialStatefulEvent):

    Returns:
        Response[StatefulEvent]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    json_body: PartialStatefulEvent,
) -> Optional[StatefulEvent]:
    """Patch

     Create or update a stateful event
    Resource: events
    Authorized roles: device

    Args:
        json_body (PartialStatefulEvent):

    Returns:
        Response[StatefulEvent]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
