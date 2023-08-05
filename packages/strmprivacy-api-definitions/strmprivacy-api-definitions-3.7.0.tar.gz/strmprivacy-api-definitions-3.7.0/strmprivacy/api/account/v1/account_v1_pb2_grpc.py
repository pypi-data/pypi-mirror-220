# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from strmprivacy.api.account.v1 import account_v1_pb2 as strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2


class AccountServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAccountDetails = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/GetAccountDetails',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsResponse.FromString,
                )
        self.GetLegacyBillingId = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/GetLegacyBillingId',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdResponse.FromString,
                )
        self.CreateAccountHandle = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/CreateAccountHandle',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleResponse.FromString,
                )
        self.InitializeCheckout = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/InitializeCheckout',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutResponse.FromString,
                )
        self.GetCheckoutStatus = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/GetCheckoutStatus',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusResponse.FromString,
                )
        self.InitializeCustomerPortal = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/InitializeCustomerPortal',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalResponse.FromString,
                )
        self.SetCheckoutCancelled = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/SetCheckoutCancelled',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledResponse.FromString,
                )
        self.UpdateOnboarding = channel.unary_unary(
                '/strmprivacy.api.account.v1.AccountService/UpdateOnboarding',
                request_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingRequest.SerializeToString,
                response_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingResponse.FromString,
                )


class AccountServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAccountDetails(self, request, context):
        """Retrieve information regarding quotas, and the user context
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLegacyBillingId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccountHandle(self, request, context):
        """Claim and create a handle for your user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitializeCheckout(self, request, context):
        """Start a checkout to subscribe to a specific subscription
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCheckoutStatus(self, request, context):
        """Get the Stripe Checkout Status for an ongoing checkout
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InitializeCustomerPortal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetCheckoutCancelled(self, request, context):
        """(-- api-linter: core::0134::synonyms=disabled
        aip.dev/not-precedent: We're not updating a Checkout here. --)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateOnboarding(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AccountServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAccountDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAccountDetails,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsResponse.SerializeToString,
            ),
            'GetLegacyBillingId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLegacyBillingId,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdResponse.SerializeToString,
            ),
            'CreateAccountHandle': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccountHandle,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleResponse.SerializeToString,
            ),
            'InitializeCheckout': grpc.unary_unary_rpc_method_handler(
                    servicer.InitializeCheckout,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutResponse.SerializeToString,
            ),
            'GetCheckoutStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCheckoutStatus,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusResponse.SerializeToString,
            ),
            'InitializeCustomerPortal': grpc.unary_unary_rpc_method_handler(
                    servicer.InitializeCustomerPortal,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalResponse.SerializeToString,
            ),
            'SetCheckoutCancelled': grpc.unary_unary_rpc_method_handler(
                    servicer.SetCheckoutCancelled,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledResponse.SerializeToString,
            ),
            'UpdateOnboarding': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateOnboarding,
                    request_deserializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingRequest.FromString,
                    response_serializer=strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'strmprivacy.api.account.v1.AccountService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AccountService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAccountDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/GetAccountDetails',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetAccountDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLegacyBillingId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/GetLegacyBillingId',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetLegacyBillingIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccountHandle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/CreateAccountHandle',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.CreateAccountHandleResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InitializeCheckout(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/InitializeCheckout',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCheckoutResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCheckoutStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/GetCheckoutStatus',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.GetCheckoutStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InitializeCustomerPortal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/InitializeCustomerPortal',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.InitializeCustomerPortalResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetCheckoutCancelled(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/SetCheckoutCancelled',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.SetCheckoutCancelledResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateOnboarding(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/strmprivacy.api.account.v1.AccountService/UpdateOnboarding',
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingRequest.SerializeToString,
            strmprivacy_dot_api_dot_account_dot_v1_dot_account__v1__pb2.UpdateOnboardingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
