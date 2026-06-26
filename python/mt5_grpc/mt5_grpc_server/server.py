import asyncio
import logging
from concurrent import futures
import grpc
from ..mt5_grpc_server.interceptors import SingleLineLoggingServerInterceptor
from ..generated_proto import services_pb2_grpc
from ..mt5_grpc_server.services import GRPCMetaTrader5Service

async def create_mt5_keepalive(configs, mt5, interval_seconds=2.0):
    await asyncio.sleep(interval_seconds)
    while True:
        if mt5.terminal_info() == None:
            logging.error('MetaTrader 5 Terminal was closed,')
            logging.info('Reopening MetaTrader 5 Terminal.')

            mt5.initialize(**configs['metatrader'])

            logging.info('MetaTrader 5 Terminal was reopened.')

        await asyncio.sleep(interval_seconds)

async def create_grpc_server(_configs, mt5):
    port = str(_configs['server']['port']) if _configs['server']['port'] is not None else "50051"
    host = _configs['server']['host'] if _configs['server']['host'] is not None else "[::]"
    max_workers = _configs['server']['max_workers'] if _configs.get('server').get('max_workers') is not None else 30
    logging.info(f'Max workers: {max_workers}')
    SingleLineLoggingServerInterceptor
    log_methods = _configs.get("log_methods")
    interceptors_list = [SingleLineLoggingServerInterceptor(log_methods=log_methods)] if log_methods else None
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers),
                             compression=grpc.Compression.Gzip,
                             interceptors=interceptors_list)

    services_pb2_grpc.add_MetaTrader5ServiceServicer_to_server(GRPCMetaTrader5Service(mt5), server)

    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    logging.info("Server started, listening on " + port)


    await server.wait_for_termination()
