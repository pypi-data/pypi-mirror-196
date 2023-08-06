import requests, json
from typing import Optional
from ddd_interface.objects.lib import serialize, deserialize
from redis_ao.infrastructure.ao import RedisAccessOperator
from api_gateway_ao.infrastructure.ao import APIGatewayAccessOperator
from .do import TaskRequestDO, APIGatewayRequestDO, TaskItemDO, TaskDeleteRequestDO

class TaskControlAccessOperator:
    def __init__(
        self, 
        ip: str, 
        port: int, 
        token: str, 
        with_gateway: str=False,
        gateway_ip: Optional[str]=None,
        gateway_port: Optional[str]=None,
        gateway_token: Optional[str]=None
    ) -> None:
        self.url = f"http://{ip}:{port}"
        self.header = {"api-token":token}
        self.with_gateway = with_gateway
        if with_gateway:
            assert gateway_ip and gateway_port and gateway_token
            self.gateway = APIGatewayAccessOperator(gateway_ip, gateway_port, gateway_token)
        else:
            self.redis = RedisAccessOperator(ip, port, token)
        self.ip = ip
        self.port = port
        self.token = token


    def send_request(self, request: TaskRequestDO, timeout=3)->str:
        request_str = serialize(request)
        domain, key = 'k3s-app', 'task-request'
        if self.gateway:
            gateway_request = APIGatewayRequestDO(
                service_name='redis',
                method = 'send_request',
                auth = {'token': self.token},
                data = {
                    'domain': domain,
                    'key': key,
                    'request': request_str
                }
            )
            task_id = self.gateway.send_request(gateway_request, timeout)
        else:
            task_id = self.redis.send_request(domain=domain, key=key, request=request_str)
        return task_id
            

    def find_task(self, task_id:str, timeout=3):
        domain = 'k3s-app'
        if self.gateway:
            gateway_request = APIGatewayRequestDO(
                service_name='redis',
                method = 'get_response',
                auth = {'token': self.token},
                data = {
                    'domain': domain,
                    'request_id': task_id
                }
            )
            task_str = self.gateway.send_request(gateway_request, timeout)
        else:
            task_str = self.redis.get_response(domain=domain, request_id=task_id)
        if task_str:
            return deserialize(task_str, TaskItemDO)
        return None

        
    def delete_task(self, request:TaskDeleteRequestDO, timeout=3):
        request_str = serialize(request)
        domain, key = 'k3s-app', 'task-delete-request'
        if self.gateway:
            gateway_request = APIGatewayRequestDO(
                service_name='redis',
                method = 'send_request',
                auth = {'token': self.token},
                data = {
                    'domain': domain,
                    'key': key,
                    'request': request_str
                }
            )
            self.gateway.send_request(gateway_request, timeout)
        else:
            self.redis.send_request(domain=domain, key=key, request=request_str)
        return True