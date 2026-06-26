import argparse
import asyncio
import os
import sys
from datetime import datetime
import importlib
import logging
from logging.handlers import RotatingFileHandler

from mt5_grpc.mocks.fake_mt5 import FakeMT5
from mt5_grpc.mt5_grpc_server.configs_manager import ConfigsManager
from mt5_grpc.mt5_grpc_server.server import create_grpc_server, create_mt5_keepalive

def parse_arguments():
    parser = argparse.ArgumentParser(prog='MetaTrader Service')
    parser.add_argument('-d', '--debug', action='store_true')

    cmd_group = parser.add_argument_group("Configuration via command line")
    cmd_group.add_argument('-c', '--host', type=str)
    cmd_group.add_argument('-p', '--port', type=int)

    cmd_group.add_argument('--mt-login', type=int)
    cmd_group.add_argument('--mt-password', type=str)
    cmd_group.add_argument('--mt-server', type=str)
    cmd_group.add_argument('--mt-path', type=str)

    configs_group = parser.add_mutually_exclusive_group(required=False)
    configs_group.add_argument('-n', '--node-name', type=str, help='Node name')
    configs_group.add_argument('-i', '--node-index', type=int, help='Node index')
    configs_group.add_argument('-f', '--fake', action='store_true',help='Fake server')

    return parser.parse_args()



def setup_logging(name):
    if not os.path.exists('logs'):
        os.makedirs('logs')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'logs/{timestamp}-{name}.log'

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=
        [
            RotatingFileHandler(log_filename,
                                mode='a',
                                maxBytes=50 * 1024 * 1024,
                                backupCount=1),
            logging.StreamHandler(stream=sys.stdout)
        ]
    )

async def main(args):

    configs_manager = ConfigsManager('configs.json', args)
    # server = await create_grpc_server(configs_manager.get_node_configs())
    # await server.serve()
    configs = configs_manager.get_node_configs()
    mt5 = importlib.import_module('MetaTrader5') if not args.fake else FakeMT5()
    mt5.initialize(**configs['metatrader'])
    await asyncio.gather(create_grpc_server(configs,mt5),
                         create_mt5_keepalive(configs, mt5,configs_manager.configs['keep_alive_interval']))


if __name__ == '__main__':
    input_args = parse_arguments()
    setup_logging(input_args.node_name)
    asyncio.run(main(input_args))
