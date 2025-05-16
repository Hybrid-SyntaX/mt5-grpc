import logging
from concurrent import futures
import grpc
from src.mt5_grpc.generated_proto import services_pb2_grpc
from src.mt5_grpc.mt5_grpc_server.services import GRPCMetaTrader5Service


def create_grpc_server(_configs):
    port = str(_configs['server']['port']) if _configs['server']['port'] is not None else "50051"
    host = _configs['server']['host'] if _configs['server']['host'] is not None else "[::]"
    max_workers = _configs['server']['max_workers'] if _configs.get('server').get('max_workers') is not None else 30
    logging.info(f'Max workers: {max_workers}')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers))

    services_pb2_grpc.add_MetaTrader5ServiceServicer_to_server(GRPCMetaTrader5Service(_configs['metatrader']), server)

    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()
