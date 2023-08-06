import re
import typing
import traceback
import dataclasses
from quart import Quart
from quart_schema import QuartSchema, validate_request, validate_response, RequestSchemaValidationError
from . import loader


@dataclasses.dataclass
class FunctionContext:
    node_id: str
    # 右面板参数
    params: typing.Optional[dict]
    # 输入桩参数
    args: dict


@dataclasses.dataclass
class FunctionParams:
    id: str
    file: str
    working_dir: typing.Optional[str]
    context: FunctionContext
    function: typing.Optional[str] = "main"


@dataclasses.dataclass
class FunctionResponse:
    id: str
    success: bool
    error: typing.Optional[str] = None
    data: typing.Optional[dict] = None


def create_app(working_dir='.'):
    app = Quart(__name__)
    QuartSchema(app)

    @app.post("/")
    @validate_request(FunctionParams)
    @validate_response(FunctionResponse)
    async def handle_post(data: FunctionParams) -> FunctionResponse:
        app.logger.debug('request %s', data)
        try:
            function = load(data, working_dir)
            ret = await function.call_func(data.context.args, data.context.params)
            out_data = {key: value for key, value in ret.items() if re.match(r"out\d+", key)}
            resp = FunctionResponse(id=data.id, success=True, data=out_data)
        except Exception as e:
            traceback.print_exc()
            resp = FunctionResponse(id=data.id, success=False, error=str(e))

        app.logger.debug('response %s', resp)
        return resp

    @app.errorhandler(RequestSchemaValidationError)
    async def handle_request_validation_error(error):
        if isinstance(error.validation_error, TypeError):
            err = str(error.validation_error)
        else:
            err = error.validation_error.json()

        return {"errors": err}, 400

    @app.get("/health/liveness")
    async def liveness():
        return "OK"

    @app.get("/health/readiness")
    async def readiness():
        return "OK"

    return app


module_imported = {}


def load(data: FunctionParams, default_dir):
    node_id = data.context.node_id
    working_dir = data.working_dir if data.working_dir else default_dir
    filename = data.file
    function = data.function

    node_function = module_imported.get(data.context.node_id)
    if not node_function:
        node_function = loader.NodeFunction(working_dir, filename, function)
        module_imported[node_id] = node_function

    return node_function
