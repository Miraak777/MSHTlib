from functools import wraps
from http import HTTPStatus
from typing import Any, Callable

from flask import Response, abort, json, jsonify, request
from mshtlib.kedro_shell.context import Context
from mshtlib.kedro_shell.predicates.exceptions import PredicateError

from src.core.component_builder import ServiceComponentBuilder
from src.server.app import create_app
from src.server.const import PayloadConstants

from . import PARAMS_PATH

app = create_app()


def predicate_error_catcher(f) -> Callable:
    @wraps(f)
    def decorator(*args, **kwargs) -> Any:
        try:
            result = f(*args, **kwargs)
        except PredicateError:
            abort(
                HTTPStatus.BAD_REQUEST,
                description="Predicate Error: wrong module input parameters",
            )
        return result

    return decorator


@app.route("/")
def index() -> Any:
    return app.response_class(status=HTTPStatus.NOT_FOUND)


@app.errorhandler(HTTPStatus.BAD_REQUEST)
def resource_not_found(e) -> Any:
    return jsonify(error=str(e)), HTTPStatus.BAD_REQUEST


@app.route("/api/example_endpoint", methods=[PayloadConstants.GET])
@predicate_error_catcher
def example_endpoint() -> Response:
    data = request.form.get("example_data_name")
    result = Context.run(
        params=PARAMS_PATH.joinpath("template_context_params.yaml"),
        user_data={"data_name_1": data},
        component_builder=ServiceComponentBuilder(),
    )
    response = app.response_class(
        response=json.dumps(result),
        status=HTTPStatus.OK,
        mimetype=PayloadConstants.APP_JSON,
    )
    return response
