# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import encryption_pb2 as encryption__pb2


class EncryptionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Encrypt = channel.unary_unary(
                '/bloock.EncryptionService/Encrypt',
                request_serializer=encryption__pb2.EncryptRequest.SerializeToString,
                response_deserializer=encryption__pb2.EncryptResponse.FromString,
                )
        self.Decrypt = channel.unary_unary(
                '/bloock.EncryptionService/Decrypt',
                request_serializer=encryption__pb2.DecryptRequest.SerializeToString,
                response_deserializer=encryption__pb2.DecryptResponse.FromString,
                )
        self.GetEncryptionAlg = channel.unary_unary(
                '/bloock.EncryptionService/GetEncryptionAlg',
                request_serializer=encryption__pb2.EncryptionAlgRequest.SerializeToString,
                response_deserializer=encryption__pb2.EncryptionAlgResponse.FromString,
                )


class EncryptionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Encrypt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Decrypt(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEncryptionAlg(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EncryptionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Encrypt': grpc.unary_unary_rpc_method_handler(
                    servicer.Encrypt,
                    request_deserializer=encryption__pb2.EncryptRequest.FromString,
                    response_serializer=encryption__pb2.EncryptResponse.SerializeToString,
            ),
            'Decrypt': grpc.unary_unary_rpc_method_handler(
                    servicer.Decrypt,
                    request_deserializer=encryption__pb2.DecryptRequest.FromString,
                    response_serializer=encryption__pb2.DecryptResponse.SerializeToString,
            ),
            'GetEncryptionAlg': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEncryptionAlg,
                    request_deserializer=encryption__pb2.EncryptionAlgRequest.FromString,
                    response_serializer=encryption__pb2.EncryptionAlgResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bloock.EncryptionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EncryptionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Encrypt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bloock.EncryptionService/Encrypt',
            encryption__pb2.EncryptRequest.SerializeToString,
            encryption__pb2.EncryptResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Decrypt(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bloock.EncryptionService/Decrypt',
            encryption__pb2.DecryptRequest.SerializeToString,
            encryption__pb2.DecryptResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEncryptionAlg(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bloock.EncryptionService/GetEncryptionAlg',
            encryption__pb2.EncryptionAlgRequest.SerializeToString,
            encryption__pb2.EncryptionAlgResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
