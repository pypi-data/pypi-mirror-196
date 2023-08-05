from importlib import metadata

CATWALK_CLIENT_VERSION = metadata.version("catwalk_client")

CATWALK_AUTH_HEADER = "Catwalk-Authorization"
CATWALK_USER_AGENT_HEADER_VALUE = f"Catwalk-Client/{CATWALK_CLIENT_VERSION}"
