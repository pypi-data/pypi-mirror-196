import json
from typing import Callable

from flask import Request, make_response, Response


class Router:
    def __init__(self, prefix=''):
        self.__route_prefix = self._strip_path(prefix)
        self.routes = {}

    @staticmethod
    def _strip_path(path: str):
        return path.strip().strip('/').strip()

    def _format_path(self, path: str):
        if self.__route_prefix != '':
            return f'/{self.__route_prefix}/{self._strip_path(path)}'
        else:
            return f'/{self._strip_path(path)}'

    def register(self, handler: Callable, path: str, method: str = 'GET'):
        if method not in self.routes:
            self.routes.update({method: {self._format_path(path): handler}})
        else:
            self.routes[method].update({self._format_path(path): handler})

    def _list_routes(self):
        print(json.dumps(self.routes, indent=2, default=str))

    def response(self, request: Request) -> Response:
        if request.method not in self.routes.keys():
            return make_response("Method not allowed", 405)

        if request.path not in self.routes[request.method]:
            return make_response("Not found", 404)

        return self.routes[request.method][request.path](request)





