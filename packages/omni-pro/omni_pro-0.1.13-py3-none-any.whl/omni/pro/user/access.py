# create a decorator to check if the user has permission to access the resource
from enum import Enum

from omni.pro.config import Config
from omni.pro.logger import LoggerTraceback, configure_logger
from omni.pro.protos.grpc_connector import Event, GRPClient
from omni.pro.protos.v1.users import user_pb2

logger = configure_logger(name=__name__)


class Permission(Enum):
    CAN_CREATE_ACCESS = "CAN_CREATE_ACCESS"
    CAN_UPDATE_ACCESS = "CAN_UPDATE_ACCESS"
    CAN_READ_ACCESS = "CAN_READ_ACCESS"
    CAN_DELETE_ACCESS = "CAN_DELETE_ACCESS"
    CAN_CREATE_ACTION = "CAN_CREATE_ACTION"
    CAN_READ_ACTION = "CAN_READ_ACTION"
    CAN_UPDATE_ACTION = "CAN_UPDATE_ACTION"
    CAN_DELETE_ACTION = "CAN_DELETE_ACTION"
    CAN_CREATE_GROUP = "CAN_CREATE_GROUP"
    CAN_READ_GROUP = "CAN_READ_GROUP"
    CAN_UPDATE_GROUP = "CAN_UPDATE_GROUP"
    CAN_DELETE_GROUP = "CAN_DELETE_GROUP"
    CAN_CREATE_USER = "CAN_CREATE_USER"
    CAN_UPDATE_USER = "CAN_UPDATE_USER"
    CAN_READ_USER = "CAN_READ_USER"
    CAN_DELETE_USER = "CAN_DELETE_USER"
    CAN_CHANGE_PASSWORD_USER = "CAN_CHAMGE_PASSWORD_USER"
    CAN_CHANGE_EMAIL_USER = "CAN_CHANGE_EMAIL_USER"


def permission_required(permission_name: Permission) -> callable:
    def decorador_func(funcion: callable) -> callable:
        def inner(instance, request, context):
            event = Event(
                module_grpc="v1.users.user_pb2_grpc",
                module_pb2="v1.users.user_pb2",
                stub_classname="UsersServiceStub",
                rpc_method="HasPermission",
                request_class="HasPermissionRequest",
                params={
                    "username": request.context.user,
                    "permission": permission_name.value,
                    "context": {"tenant": request.context.tenant},
                },
            )
            response: user_pb2.HasPermissionResponse = None
            response, success = GRPClient(Config.SAAS_MS_USER).call_rpc_fuction(event)
            if not success or not response.has_permission:
                raise Exception("User has no permission")
            c = funcion(instance, request, context)
            return c

        return inner

    return decorador_func


def sync_cognito_access(sync_allow_access):
    def decorador(funcion):
        def wrapper(*args, **kwargs):
            result = funcion(*args, **kwargs)
            sync_allow_access(result)
            return result

        return wrapper

    return decorador


# Definimos la función que queremos ejecutar al final
def sync_allow_access(result):
    try:
        logger.info("sync_allow_access")
        if isinstance(result, user_pb2.GroupCreateResponse):
            pass
    except Exception as e:
        LoggerTraceback.error("Resource Decorator exception", e, logger)
    return True
