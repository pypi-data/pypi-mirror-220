from cegalprizm.hub import HubTaskRegistry
from google.protobuf.any_pb2 import Any
from typing import Iterable, Tuple
from cegalprizm.hub.connector import HubConnector, TaskContext
from example_connector.greeter_pb2 import GreeterRequest, GreeterResult
import time
import logging

logger = logging.getLogger("cegalprizm.hub")
logger.setLevel(logging.DEBUG)

def DemoUnaryCtxTask(ctx: TaskContext, payload: Any) -> Tuple[bool, Any, str]:
    print(f"metadata: {ctx.metadata}")
    greeterRequest = GreeterRequest()
    payload.Unpack(greeterRequest)
    # print(f"DemoUnaryTask received request: {greeterRequest.message}")
    time.sleep(0.1)
    return (True, GreeterResult(greeting_response=f"DemoUnaryTask greets {greeterRequest.message}!"), "")
    
def ServerStreamingGreeterCtxTask(ctx: TaskContext, payload) -> Iterable[Tuple[bool, bool, Any, str]]:
    print(f"metadata: {ctx.metadata}")
    greeterRequest = GreeterRequest()
    payload.Unpack(greeterRequest)
    # print(f"ServerStreamingGreeterTask received request: {greeterRequest.message}")
    greetings = ["Hello", "Hola", "Bonjour", "Hallo", "Hej", "Ahoj", "Konnichiwa", "Ni hao", "Namaste", "Salaam", "Sawubona"]*10
    for greeting in greetings:
        time.sleep(0.1)
        response = GreeterResult(greeting_response=f"{greeting} {greeterRequest.message}!")
        yield (True, False, response, None)
        # print(f"ServerStreamingGreeterTask sent response: {response.greeting_response}")
    
    response = GreeterResult(greeting_response=f"Ciao {greeterRequest.message}!")
    yield (True, True, response, None)

def DemoUnaryTask(payload: Any) -> Tuple[bool, Any, str]:
    greeterRequest = GreeterRequest()
    payload.Unpack(greeterRequest)
    # print(f"DemoUnaryTask received request: {greeterRequest.message}")
    time.sleep(0.1)
    return (True, GreeterResult(greeting_response=f"DemoUnaryTask greets {greeterRequest.message}!"), "")
    
def ServerStreamingGreeterTask(payload) -> Iterable[Tuple[bool, bool, Any, str]]:
    greeterRequest = GreeterRequest()
    payload.Unpack(greeterRequest)
    # print(f"ServerStreamingGreeterTask received request: {greeterRequest.message}")
    greetings = ["Hello", "Hola", "Bonjour", "Hallo", "Hej", "Ahoj", "Konnichiwa", "Ni hao", "Namaste", "Salaam", "Sawubona"]*10
    for greeting in greetings:
        time.sleep(0.1)
        response = GreeterResult(greeting_response=f"{greeting} {greeterRequest.message}!")
        yield (True, False, response, None)
        # print(f"ServerStreamingGreeterTask sent response: {response.greeting_response}")
    
    response = GreeterResult(greeting_response=f"Ciao {greeterRequest.message}!")
    yield (True, True, response, None)

def get_task_registry() -> HubTaskRegistry:
    registry = HubTaskRegistry()

    registry.register_unary_task(wellknown_payload_identifier="cegal.example_python_connector.demo_unary_task_ctx",
                                 task=DemoUnaryCtxTask,
                                 friendly_name="An example of a unary task with context with in a python connector",
                                 description="No description yet, sorry!",
                                 payload_auth=None)

    registry.register_server_streaming_task(wellknown_payload_identifier="cegal.example_python_connector.server_streaming_greeter_task_ctx",
                                            task=ServerStreamingGreeterCtxTask,
                                            friendly_name="An example of a server streaming task with context in a python connector",
                                            description="No description yet, sorry!",
                                            payload_auth=None)
    
    registry.register_unary_task(wellknown_payload_identifier="cegal.example_python_connector.demo_unary_task",
                                 task=DemoUnaryTask,
                                 friendly_name="An example of a unary task without context in a python connector",
                                 description="No description yet, sorry!",
                                 payload_auth=None)

    registry.register_server_streaming_task(wellknown_payload_identifier="cegal.example_python_connector.server_streaming_greeter_task",
                                            task=ServerStreamingGreeterTask,
                                            friendly_name="An example of a server streaming task without context in a python connector",
                                            description="No description yet, sorry!",
                                            payload_auth=None)
    
    
    return registry


connector = HubConnector(wellknown_identifier="cegal.example_python_connector",
                         friendly_name="Cegal example python connector",
                         description="No description yet, sorry!",
                         version="0.0.1",
                         build_version="local")

connector.start(get_task_registry())