# Example OpenCreator plugin component: GET /server/oc_hello
#
# This file may be distributed under the terms of the GNU GPLv3 license.
from __future__ import annotations

try:
    from ..common import RequestType
    GET = RequestType.GET
except ImportError:          # Moonraker before 2023
    GET = ["GET"]


class OCHello:
    def __init__(self, config):
        self.server = config.get_server()
        self.message = config.get("message", "Hello from an OpenCreator plugin")
        self.server.register_endpoint("/server/oc_hello", GET, self._handle_hello)

    async def _handle_hello(self, web_request):
        klippy = self.server.lookup_component("klippy_apis")
        try:
            status = await klippy.query_objects({"oc_hello": None})
        except Exception:
            status = {}
        return {"message": self.message, "klippy": status.get("oc_hello")}


def load_component(config):
    return OCHello(config)
