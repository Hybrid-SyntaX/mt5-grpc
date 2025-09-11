import json
import os

import MetaTrader5 as mt5
import grpc
import pytest
from mt5_grpc.core.enums import GRPCMetaTrader5ReturnType
from mt5_grpc.mt5_grpc_client import GRPCMetaTrader5

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="class")
def mt5_test_env(request):
    # Load configs and initialize original MT5
    with open(os.path.join(CURRENT_DIR, 'configs.json')) as configs_file:
        configs = json.load(configs_file)

    assert mt5.initialize(**configs["metatrader"]), "Failed to initialize original MT5 client"
    channel = grpc.insecure_channel(configs["grpc_channel"])
    mt5_client = GRPCMetaTrader5(channel, return_type=GRPCMetaTrader5ReturnType.VALUE_OR_ERROR)

    # Provide objects to the test class
    request.cls.mt5 = mt5
    request.cls.mt5_client = mt5_client
    request.cls.grpc_channel = channel
    request.cls.mt5_configs = configs["metatrader"]

    yield  # Run the tests

    # Teardown
    mt5.shutdown()
    channel.close()
