from pathlib import Path


class PathConst:
    BASE_DIR = Path(__file__).parent.parent.absolute()

    PROTO_FILE = BASE_DIR.joinpath('asx_bridge.proto')

    LOG_DIR = BASE_DIR.joinpath('logs')

    ASX_BRIDGE_LOCK = LOG_DIR.joinpath('asx_bridge.lock')
