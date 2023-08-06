import os
from typing import Final, Optional
from urllib import parse

import jwt
from sqlalchemy.orm import Session

from switcore.auth.repository import AppRepository
from switcore.auth.schemas import SwitToken, Payload
from switcore.auth.utils import get_swit_openapi_base_url


def get_oauth2_url(
        scopes: str,
        redirect_url: str
) -> str:
    client_id: str = os.getenv("SWIT_CLIENT_ID", None)
    base_url: str = os.getenv('BASE_URL', None)

    assert client_id is not None, "SWIT_CLIENT_ID is not set check .env file"
    assert base_url is not None, "BASE_URL is not set check .env file"

    params: Final[dict] = {
        "client_id": client_id,
        "redirect_uri": base_url + redirect_url,
        "response_type": "code",
        "scope": scopes
    }

    return f"{get_swit_openapi_base_url()}/oauth/authorize?{parse.urlencode(params)}"


async def save_swit_app(
        session: Session,
        token: SwitToken,
        state: str | None = None  # noqa
):
    repository = AppRepository(session)
    payload = Payload(**jwt.decode(token.access_token, options={"verify_signature": False}))

    return repository.create(
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        apps_id=payload.apps_id,
        cmp_id=payload.cmp_id,
        iss=payload.iss
    )
