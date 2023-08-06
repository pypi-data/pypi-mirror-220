from eth_account import Account  # noqa: E402,
import pkg_resources

from web3tool.main import (
    AsyncWeb3,
    Web3tool,
)
from web3tool.providers.async_rpc import (  # noqa: E402
    AsyncHTTPProvider,
)
from web3tool.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from web3tool.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from web3tool.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from web3tool.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

__version__ = pkg_resources.get_distribution("web3tool").version

__all__ = [
    "__version__",
    "AsyncWeb3",
    "Web3tool",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "EthereumTesterProvider",
    "Account",
    "AsyncHTTPProvider",
]
