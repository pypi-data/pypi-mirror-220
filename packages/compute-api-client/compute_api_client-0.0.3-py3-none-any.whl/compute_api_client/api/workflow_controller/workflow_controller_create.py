from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.new_workflow import NewWorkflow
from ...models.workflow import Workflow
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: NewWorkflow,
) -> Dict[str, Any]:
    url = "{}/compute/workflows".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Workflow]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Workflow.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Workflow]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: NewWorkflow,
) -> Response[Workflow]:
    """
    Args:
        json_body (NewWorkflow): (tsType: Omit<Workflow, 'id' | 'status' | 'dateCreated'>,
            schemaOptions: { title: 'NewWorkflow', exclude: [ 'id', 'status', 'dateCreated' ] })

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workflow]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: NewWorkflow,
) -> Optional[Workflow]:
    """
    Args:
        json_body (NewWorkflow): (tsType: Omit<Workflow, 'id' | 'status' | 'dateCreated'>,
            schemaOptions: { title: 'NewWorkflow', exclude: [ 'id', 'status', 'dateCreated' ] })

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workflow]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: NewWorkflow,
) -> Response[Workflow]:
    """
    Args:
        json_body (NewWorkflow): (tsType: Omit<Workflow, 'id' | 'status' | 'dateCreated'>,
            schemaOptions: { title: 'NewWorkflow', exclude: [ 'id', 'status', 'dateCreated' ] })

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workflow]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: NewWorkflow,
) -> Optional[Workflow]:
    """
    Args:
        json_body (NewWorkflow): (tsType: Omit<Workflow, 'id' | 'status' | 'dateCreated'>,
            schemaOptions: { title: 'NewWorkflow', exclude: [ 'id', 'status', 'dateCreated' ] })

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Workflow]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
