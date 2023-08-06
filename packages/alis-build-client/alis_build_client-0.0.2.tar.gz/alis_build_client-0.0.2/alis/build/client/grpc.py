import grpc
import re
import time
from google.auth.transport.grpc import AuthMetadataPlugin
from google.auth.transport.requests import Request
from google.auth.exceptions import DefaultCredentialsError
from google.oauth2 import id_token

class InvalidArgumentError(Exception):
    print(f"Argument validation failed: {Exception}")

def validate_argument(name: str, value: str, pattern: str) -> None:
    if not re.match(pattern, value):
        raise InvalidArgumentError(f"Invalid {name}. Expected format is {pattern}")

def new_conn(host: str, insecure: bool) -> grpc.Channel:
    """
    Create a new gRPC channel to a server.

    :param host: (str) The host to connect to.
    :param insecure: (bool) If set to True, creates an insecure channel. Otherwise a secure channel will be created.
    :return: A grpc.Channel.
    """    
    class GrpcAuth(grpc.AuthMetadataPlugin):
        def __init__(self, request, target_audience):
            """
            :type target_audience: str
            :type request: google.auth.transport.Response
            """
            self.target_audience = target_audience
            self._set_id_token(request)
            
        def __call__(self, context, callback):
            if self._token_expiry <= time.time():
                self._set_id_token(Request())
            callback(self._metadata, None)
            
        def _set_id_token(self, request):
            """
            retrieves an OAuth2 ID token for a given audience
            """
            token = id_token.fetch_id_token(request, self.target_audience)
            self._metadata = (('authorization', 'Bearer ' + token),)
            self._token_expiry = id_token.verify_oauth2_token(token, request)['exp']
    
    validate_argument("host", host, r"^[a-zA-Z0-9.-]+:\d+$")

    if insecure:
        # Create an insecure Channel
        channel = grpc.insecure_channel(host)
    else:
        # Make a secure Channel
        # The following URL will be used as the audience field in the JWT token authentication with the server.
        audience = f"https://{host.split(':')[0]}"
        try:
            # Create an AuthMetadataPlugin instance using the ID token credentials and the request
            auth = GrpcAuth(Request(), audience)

            # Create a set of grpc.CallCredentials using the AuthMetadataPlugin instance
            call_creds = grpc.metadata_call_credentials(auth)

            # Create a secure Channel using the call credentials
            channel = grpc.secure_channel(host, grpc.composite_channel_credentials(grpc.ssl_channel_credentials(), call_creds))

        except DefaultCredentialsError as e:
            print(f"Failed to fetch identity token credentials: {e}")
            return None

    return channel