import argparse
import asyncio
import logging

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

    return parser.parse_args()


async def main(args):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    configs_manager = ConfigsManager('configs.json', args)
    # server = await create_grpc_server(configs_manager.get_node_configs())
    # await server.serve()
    configs = configs_manager.get_node_configs()
    await asyncio.gather(create_grpc_server(configs),
                         create_mt5_keepalive(configs, configs_manager.configs['keep_alive_interval']))


if __name__ == '__main__':
    input_args = parse_arguments()
    asyncio.run(main(input_args))
