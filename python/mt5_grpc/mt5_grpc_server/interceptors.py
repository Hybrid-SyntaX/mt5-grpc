import grpc
import logging
import inspect




class SingleLineLoggingServerInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self, log_methods = []):
        super().__init__()
        self._log_methods = log_methods

    def _proto_to_single_line(self,message):
        """Helper to convert proto to a single line string."""
        try:
            s = str(message).replace('\n', ' ').replace('\r', ' ')
            return " ".join(s.split())
        except Exception as e:
            return f"<Serialization Error: {e}>"


    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method.replace('/MetaTrader5Service/','')
        handler = await continuation(handler_call_details)

        if handler.unary_unary:
            original_func = handler.unary_unary

            async def wrapped_unary_unary(request, context):
                if inspect.iscoroutinefunction(original_func):
                    response = await original_func(request, context)
                else:
                    response = original_func(request, context)

                if self._log_methods == ['*'] or method in self._log_methods:
                    req_str = self._proto_to_single_line(request)
                    res_str = self._proto_to_single_line(response)

                    logging.info(f"[{method}] REQ: {req_str} | RES: {res_str}")

                return response

            return grpc.unary_unary_rpc_method_handler(
                wrapped_unary_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler

