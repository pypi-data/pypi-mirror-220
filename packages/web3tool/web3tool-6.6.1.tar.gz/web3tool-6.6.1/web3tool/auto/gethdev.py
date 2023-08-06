from web3tool import (
    IPCProvider,
    Web3tool,
)
from web3tool.middleware import (
    geth_poa_middleware,
)
from web3tool.providers.ipc import (
    get_dev_ipc_path,
)

w3 = Web3tool(IPCProvider(get_dev_ipc_path()))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
