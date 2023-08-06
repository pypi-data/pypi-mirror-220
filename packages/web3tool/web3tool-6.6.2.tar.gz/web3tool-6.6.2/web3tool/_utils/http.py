def construct_user_agent(class_name: str) -> str:
    from web3tool import (
        __version__ as web3_version,
    )

    user_agent = f"web3tool.py/{web3_version}/{class_name}"
    return user_agent
