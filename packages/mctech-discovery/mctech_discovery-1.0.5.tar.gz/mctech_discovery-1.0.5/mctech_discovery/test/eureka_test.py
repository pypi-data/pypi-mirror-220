from __future__ import absolute_import
from ..rpc import rpc
from ..rpc.request_context import PipeRpcInvoker, RpcServiceInfo, RpcInvoker
from ..discovery import discovery_client

discovery_client.start()
configure = discovery_client.load_config()
discovery_client.register()
configure.merge()
result = rpc.post(
    RpcInvoker(path='/nexts',
               query={'count': 5}, params={'id': 123456}),
    RpcServiceInfo(service_id='sequence-service')
)
print(result)
bind_rpc = rpc.bind(RpcServiceInfo(service_id='sequence-service'))
result = bind_rpc.stream(
    PipeRpcInvoker(path='/nexts', method='post',
                   query={'count': 5}, params={'id': 123456}),
)

# print(json.dumps(configure.get_config()))
print(result)
