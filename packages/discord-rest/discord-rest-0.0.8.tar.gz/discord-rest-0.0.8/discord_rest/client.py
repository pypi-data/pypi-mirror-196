from __future__ import annotations

import asyncio

from typing import Any, Set
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from discord import Client, utils
from logging import getLogger
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from json import loads

import uvicorn
log = getLogger("REST")


__all__ = ("RestClient",)


class RestClient(FastAPI):
    def __init__(
        self,
        client: Client,
        *,
        route: str = "/interactions",
        **kwargs
    ):
        super().__init__(**kwargs)
        self._client = client
        self._app = FastAPI
        self._route = route
        self._verify_key: VerifyKey = utils.MISSING
        self.add_route(path=route, route=self.handle_interactions, methods=["POST"])
    def get_latest_task(
        self, before_tasks: Set[asyncio.Task[Any]]
    ) -> asyncio.Task[None]:
        return (asyncio.all_tasks() - before_tasks).pop()

    async def verify_request(self, request: Request):
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")

        if not signature or not timestamp:
            return False
        try:
            message = timestamp.encode() + await request.body()
            self._verify_key.verify(
                message, bytes.fromhex(signature)
            )
        except BadSignatureError as e:
            return False

        return True

    async def handle_interactions(self, request: Request):
        if not await self.verify_request(request):
            response = await utils.maybe_coroutine(lambda r: None, request)
            return JSONResponse(content="Bad Signature", status_code=401)

        data = await request.json()
        if data["type"] == 1:
            return JSONResponse(
                status_code=200,
                content={"type": 1}
            )

        tasks = asyncio.all_tasks()
        self._client._connection.parse_interaction_create(data)
        if len(tasks):
            await self.get_latest_task(tasks)
        response = await utils.maybe_coroutine(lambda r: None, request)
        return JSONResponse(response)

    async def start(self, token: str, **kwargs):
        utils.setup_logging()
        await self._client.login(token)

        assert self._client.application is not None
        self._verify_key = VerifyKey(bytes.fromhex(self._client.application.verify_key))
        log.info(
            f"Running on https://{kwargs.get('host', 'localhost')}:{kwargs.get('port', 8080)}{self._route}"
        )
        self._client.dispatch("ready")

        
