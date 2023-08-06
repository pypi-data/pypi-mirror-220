import logging
import uuid
from dataclasses import dataclass

from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    ClientPodComputeResources,
    PodComputeResourceTemplateSpec,
)
from _qwak_proto.qwak.workspace.workspace_pb2 import Workspace
from _qwak_proto.qwak.workspace.workspace_service_pb2 import (
    CreateWorkspaceResponse,
    DeleteWorkspaceResponse,
    GetWorkspaceByIdResponse,
    ListWorkspacesResponse,
    UpdateWorkspaceResponse,
)
from _qwak_proto.qwak.workspace.workspace_service_pb2_grpc import (
    WorkspaceManagementServiceServicer,
)

logger = logging.getLogger(__name__)


@dataclass
class WorkspaceData:
    workspace_name: str
    image_type: str
    template_id: str


class WorkspaceManagerServiceMock(WorkspaceManagementServiceServicer):
    def __init__(self):
        super(WorkspaceManagerServiceMock, self).__init__()
        self.workspaces = dict()

    def CreateWorkspace(self, request, context):
        logger.info(f"Creating workspace {request}")
        workspace_id = self._get_workspace_id()
        self.workspaces[workspace_id] = WorkspaceData(
            workspace_name=request.workspace_creation_spec.workspace_name,
            image_type=request.workspace_creation_spec.image_type,
            template_id=request.workspace_creation_spec.client_pod_compute_resources.template_spec.template_id,
        )
        return CreateWorkspaceResponse(workspace_id=workspace_id)

    def UpdateWorkspace(self, request, context):
        logger.info(f"Updating workspace {request}")
        self.workspaces[request.workspace_id] = WorkspaceData(
            workspace_name=request.workspace.workspace_name,
            image_type=request.workspace.image_type,
            template_id=request.workspace.client_pod_compute_resources.template_spec.template_id,
        )
        return UpdateWorkspaceResponse()

    def DeleteWorkspace(self, request, context):
        logger.info(f"delete workspace request: {request}")
        del self.workspaces[request.workspace_id]
        return DeleteWorkspaceResponse()

    def GetWorkspaceById(self, request, context):
        logger.info(f"get workspace by id request: {request}")
        return GetWorkspaceByIdResponse(
            workspace=Workspace(
                workspace_name=self.workspaces[request.workspace_id].workspace_name,
                image_type=self.workspaces[request.workspace_id].image_type,
                client_pod_compute_resources=ClientPodComputeResources(
                    template_spec=PodComputeResourceTemplateSpec(
                        template_id=self.workspaces[request.workspace_id].template_id
                    )
                ),
            )
        )

    def ListWorkspaces(self, request, context):
        logger.info(f"list workspaces: {request}")
        return ListWorkspacesResponse(
            workspaces=[
                Workspace(
                    workspace_name=workspace.workspace_name,
                )
                for workspace_id, workspace in self.workspaces.items()
            ]
        )

    def DeployWorkspace(self, request, context):
        pass

    def UndeployWorkspace(self, request, context):
        pass

    @staticmethod
    def _get_workspace_id():
        return str(uuid.uuid4())
