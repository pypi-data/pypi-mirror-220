from cegalprizm.hub import HubClient
from cegalprizm.hub.connection_parameters import ConnectionParameters
from .greeter_pb2 import GreeterRequest, GreeterResult
from google.protobuf.any_pb2 import Any
import threading
import time
import logging

logger = logging.getLogger("cegalprizm.hub")
logger.setLevel(logging.INFO)

connection_parameters = ConnectionParameters(
    use_auth=True
)

def task_fast_unary():
    for _ in range(5):
        hub_client = HubClient(connection_parameters)
        for _ in range(5):
            request = GreeterRequest(message="Tore") 
            payload = Any()
            payload.Pack(request)
            (ok, packed_response, connector_id)  = hub_client.do_unary_request(
                wellknown_connector_identifier="cegal.example_python_connector", 
                wellknown_payload_identifier="cegal.example_python_connector.demo_unary_task_ctx", 
                payload=payload
            )
            if ok:
                greeterResult = GreeterResult()
                packed_response.Unpack(greeterResult)
                print(f"unary with ctx response: {greeterResult.greeting_response}")
            else:
                print(f"error: {packed_response}")
            time.sleep(0.1)

def task_example_server_streaming():
    for _ in range(5):
        hub_client = HubClient(connection_parameters)
        request = GreeterRequest(message="Tore") 
        payload = Any()
        payload.Pack(request)
        for _ in range(5):
            responses = hub_client.do_server_streaming(
                wellknown_connector_identifier="cegal.example_python_connector", 
                wellknown_payload_identifier="cegal.example_python_connector.server_streaming_greeter_task_ctx", 
                payload=payload
            )

            for (ok, packed_response, _)  in responses:
                if ok:
                    greeterResult = GreeterResult()
                    packed_response.Unpack(greeterResult)
                    print(f"server streaming with ctx response: {greeterResult.greeting_response}")
                else:
                    print(f"error: {packed_response}")
            time.sleep(0.1)

def task_fast_unary_no_ctx():
    for _ in range(5):
        hub_client = HubClient(connection_parameters)
        for _ in range(5):
            request = GreeterRequest(message="Tore") 
            payload = Any()
            payload.Pack(request)
            (ok, packed_response, connector_id)  = hub_client.do_unary_request(
                wellknown_connector_identifier="cegal.example_python_connector", 
                wellknown_payload_identifier="cegal.example_python_connector.demo_unary_task", 
                payload=payload
            )
            if ok:
                greeterResult = GreeterResult()
                packed_response.Unpack(greeterResult)
                print(f"unary no ctx response: {greeterResult.greeting_response}")
            else:
                print(f"error: {packed_response}")
            time.sleep(0.1)

def task_example_server_streaming_no_ctx():
    for _ in range(5):
        hub_client = HubClient(connection_parameters)
        request = GreeterRequest(message="Tore") 
        payload = Any()
        payload.Pack(request)
        for _ in range(5):
            responses = hub_client.do_server_streaming(
                wellknown_connector_identifier="cegal.example_python_connector", 
                wellknown_payload_identifier="cegal.example_python_connector.server_streaming_greeter_task", 
                payload=payload
            )

            for (ok, packed_response, _)  in responses:
                if ok:
                    greeterResult = GreeterResult()
                    packed_response.Unpack(greeterResult)
                    print(f"server streaming no ctx response: {greeterResult.greeting_response}")
                else:
                    print(f"error: {packed_response}")
            time.sleep(0.1)

t1 = threading.Thread(target=task_fast_unary, daemon=True)
t2 = threading.Thread(target=task_example_server_streaming, daemon=True)
t3 = threading.Thread(target=task_fast_unary_no_ctx, daemon=True)
t4 = threading.Thread(target=task_example_server_streaming_no_ctx, daemon=True)
t1.start()
t2.start()
t3.start()
t4.start()
# t1.join()
# t2.join()
while True:
    time.sleep(1)
    # if not t2.is_alive():
    #     break
    if not t1.is_alive() and not t2.is_alive() and not t3.is_alive() and not t4.is_alive():
        break
print("Done!")