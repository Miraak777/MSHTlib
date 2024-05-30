from dataclasses import dataclass


@dataclass(frozen=True)
class PayloadConstants:
    APP_JSON: str = "application/json"
    X_ACCESS_TOKEN: str = "x-access-token"
    POST: str = "POST"
    GET: str = "GET"
