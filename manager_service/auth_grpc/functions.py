import uuid

import auth_pb2
import auth_pb2_grpc
import grpc
from django.conf import settings

auth_channel = grpc.insecure_channel(
    f"{settings.AUTH_GRPC_HOST}:{settings.AUTH_GRPC_PORT}"
)
auth_client = auth_pb2_grpc.AuthStub(auth_channel)


def set_auth_role(id_: uuid.UUID, role: str):
    set_role_request = auth_pb2.SetRoleRequest(
        uuid=id_, role=role
    )
    auth_response = auth_client.SetRole(
        set_role_request
    )
    return auth_response.result


def check_user_exits(id_: uuid.UUID):
    return auth_client.CheckUserExists(uuid=id_).result
