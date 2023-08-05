# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from strmprivacy.api.monitoring.v1 import monitoring_pb2 as strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2


class MonitoringServiceStub(object):
    """
    The monitoring service
    1. holds a semi-persistent store of entity states that can be queried by end users to show entity state
    2. has an endpoint that agents can call to store entity states
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetEntityState = channel.unary_stream(
                '/strmprivacy.api.monitoring.v1.MonitoringService/GetEntityState',
                request_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateResponse.FromString,
                )
        self.GetLatestEntityStates = channel.unary_unary(
                '/strmprivacy.api.monitoring.v1.MonitoringService/GetLatestEntityStates',
                request_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesResponse.FromString,
                )
        self.UpdateEntityStates = channel.stream_unary(
                '/strmprivacy.api.monitoring.v1.MonitoringService/UpdateEntityStates',
                request_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesResponse.FromString,
                )


class MonitoringServiceServicer(object):
    """
    The monitoring service
    1. holds a semi-persistent store of entity states that can be queried by end users to show entity state
    2. has an endpoint that agents can call to store entity states
    """

    def GetEntityState(self, request, context):
        """
        will be called by end users from the cli or console, to retrieve entity states
        and indicate them to users.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestEntityStates(self, request, context):
        """
        can be called via the CLI and the Console, to get the latest entity state for all entities included
        in this request
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntityStates(self, request_iterator, context):
        """
        will be called from entity agents so that they can send the entity states
        of items they're responsible for to the monitoring service.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MonitoringServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetEntityState': grpc.unary_stream_rpc_method_handler(
                    servicer.GetEntityState,
                    request_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateResponse.SerializeToString,
            ),
            'GetLatestEntityStates': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLatestEntityStates,
                    request_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesResponse.SerializeToString,
            ),
            'UpdateEntityStates': grpc.stream_unary_rpc_method_handler(
                    servicer.UpdateEntityStates,
                    request_deserializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'strmprivacy.api.monitoring.v1.MonitoringService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MonitoringService(object):
    """
    The monitoring service
    1. holds a semi-persistent store of entity states that can be queried by end users to show entity state
    2. has an endpoint that agents can call to store entity states
    """

    @staticmethod
    def GetEntityState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/strmprivacy.api.monitoring.v1.MonitoringService/GetEntityState',
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateRequest.SerializeToString,
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetEntityStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLatestEntityStates(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.monitoring.v1.MonitoringService/GetLatestEntityStates',
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesRequest.SerializeToString,
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.GetLatestEntityStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEntityStates(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/strmprivacy.api.monitoring.v1.MonitoringService/UpdateEntityStates',
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesRequest.SerializeToString,
            strmprivacy_dot_api_dot_monitoring_dot_v1_dot_monitoring__pb2.UpdateEntityStatesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
