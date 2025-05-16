from abc import ABC

import MetaTrader5
from grpc import Channel

from mt5_grpc.core.abstracts import AbstractMetaTrader5


class AbstractMT5TestEnv(ABC):
    mt5: MetaTrader5
    mt5_client: AbstractMetaTrader5
    grpc_channel: Channel
    mt5_configs: dict