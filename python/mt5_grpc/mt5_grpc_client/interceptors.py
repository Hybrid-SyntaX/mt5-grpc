import grpc
import logging

class SingleLineLoggingClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self,log_methods=[]):
        super().__init__()
        self._log_methods = log_methods

    def _proto_to_single_line(self, message):
        if hasattr(message, 'result'):
            message = message.result

        try:
            s = str(message).replace('\n', ' ').replace('\r', ' ')
            if not s.strip():
                return "{}"
            return " ".join(s.split())
        except Exception as e:
            return f"<Serialization Error: {e}>"

    def intercept_unary_unary(self, continuation, client_call_details, request):
        method = client_call_details.method.replace('/MetaTrader5Service/','')

        result = continuation(client_call_details, request)
        actual_response = result
        if hasattr(result, 'result'):
            actual_response = result.result()

        if self._log_methods == ['*'] or method in self._log_methods:
            req_str = self._proto_to_single_line(request)
            res_str = self._proto_to_single_line(actual_response)
            logging.info(f"[SYNC-CLIENT] {method} | REQ: {req_str} | RES: {res_str}")

        return result

    # Pass-through methods for other RPC types
    def intercept_unary_stream(self, continuation, client_call_details, request):
        return continuation(client_call_details, request)

    def intercept_stream_unary(self, continuation, client_call_details):
        return continuation(client_call_details)

    def intercept_stream_stream(self, continuation, client_call_details, request_iterator):
        return continuation(client_call_details, request_iterator)