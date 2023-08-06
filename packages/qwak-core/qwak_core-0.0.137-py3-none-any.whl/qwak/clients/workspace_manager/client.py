import grpc
from _qwak_proto.qwak.user_application.common.v0.resources_pb2 import (
    ClientPodComputeResources,
    PodComputeResourceTemplateSpec,
)
from _qwak_proto.qwak.workspace.workspace_pb2 import Workspace, WorkspaceCreationSpec
from _qwak_proto.qwak.workspace.workspace_service_pb2 import (
    CreateWorkspaceRequest,
    CreateWorkspaceResponse,
    DeleteWorkspaceRequest,
    DeployWorkspaceRequest,
    DeployWorkspaceResponse,
    GetWorkspaceByIdRequest,
    GetWorkspaceByIdResponse,
    ListWorkspacesRequest,
    ListWorkspacesResponse,
    UpdateWorkspaceRequest,
)
from _qwak_proto.qwak.workspace.workspace_service_pb2_grpc import (
    WorkspaceManagementServiceStub,
)
from dependency_injector.wiring import Provide
from qwak.exceptions import QwakException
from qwak.inner.di_configuration import QwakContainer


class WorkspaceManagerClient:
    """
    Used for interacting with Workspace Manager endpoints
    """

    def __init__(self, grpc_channel=Provide[QwakContainer.core_grpc_channel]):
        self._workspace_manager = WorkspaceManagementServiceStub(grpc_channel)

    def create_workspace(
        self, workspace_name: str, image_type: str, template_id: str
    ) -> CreateWorkspaceResponse:
        """
        Args:
            workspace_name: The name of the workspace
            image_type: The image type of the workspace deployment
            template_id: The id of the template to use for the workspace deployment

        Returns:
            The response of the created workspace
        """
        try:
            create_workspace_request = CreateWorkspaceRequest(
                workspace_creation_spec=WorkspaceCreationSpec(
                    workspace_name=workspace_name,
                    image_type=image_type,
                    client_pod_compute_resources=ClientPodComputeResources(
                        template_spec=PodComputeResourceTemplateSpec(
                            template_id=template_id
                        )
                    ),
                )
            )
            return self._workspace_manager.CreateWorkspace(create_workspace_request)
        except grpc.RpcError as e:
            raise QwakException(f"Failed to create workspace, error is {repr(e)}")

    def update_workspace(
        self, workspace_id: str, workspace_name: str, image_type: str, template_id: str
    ) -> CreateWorkspaceResponse:
        """
        Args:
            workspace_id: The id of the workspace
            workspace_name: The name of the workspace
            image_type: The image type of the workspace deployment
            template_id: The id of the template to use for the workspace deployment
        Returns:
            The response of the updated workspace
        """
        try:
            update_workspace_request = UpdateWorkspaceRequest(
                workspace_id=workspace_id,
                workspace=Workspace(
                    workspace_name=workspace_name,
                    image_type=image_type,
                    client_pod_compute_resources=ClientPodComputeResources(
                        template_spec=PodComputeResourceTemplateSpec(
                            template_id=template_id
                        )
                    ),
                ),
            )
            return self._workspace_manager.UpdateWorkspace(update_workspace_request)
        except grpc.RpcError as e:
            raise QwakException(f"Failed to update workspace, error is {repr(e)}")

    def deploy_workspace(self, workspace_id: str) -> DeployWorkspaceResponse:
        """
        Args:
            workspace_id: The id of the workspace
        Returns:
            The response of the deployed workspace
        """
        try:
            deploy_workspace_request = DeployWorkspaceRequest(workspace_id=workspace_id)
            return self._workspace_manager.DeployWorkspace(deploy_workspace_request)
        except grpc.RpcError as e:
            raise QwakException(f"Failed to deploy workspace, error is {repr(e)}")

    def get_workspaces(self) -> ListWorkspacesResponse:
        """
        Returns:
            The response of the list workspaces
        """
        try:
            return self._workspace_manager.ListWorkspaces(ListWorkspacesRequest())
        except grpc.RpcError as e:
            raise QwakException(f"Failed to list workspaces, error is {repr(e)}")

    def get_workspace_by_id(self, workspace_id: str) -> GetWorkspaceByIdResponse:
        """
        Args:
            workspace_id: The id of the workspace
        Returns:
            The response of the workspace
        """
        try:
            return self._workspace_manager.GetWorkspaceById(
                GetWorkspaceByIdRequest(workspace_id=workspace_id)
            )
        except grpc.RpcError as e:
            raise QwakException(f"Failed to get workspace by id, error is {repr(e)}")

    def delete_workspace(self, workspace_id: str) -> DeployWorkspaceResponse:
        """
        Args:
            workspace_id: The id of the workspace
        Returns:
            The response of the deleted workspace
        """
        try:
            delete_workspace_request = DeleteWorkspaceRequest(workspace_id=workspace_id)
            return self._workspace_manager.DeleteWorkspace(delete_workspace_request)
        except grpc.RpcError as e:
            raise QwakException(f"Failed to delete workspace, error is {repr(e)}")
