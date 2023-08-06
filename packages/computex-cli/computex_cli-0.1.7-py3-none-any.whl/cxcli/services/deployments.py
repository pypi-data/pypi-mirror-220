from typing import List

from pydantic import BaseModel

from .service import CoreApiService


class DeployRequest(BaseModel):
    app_name: str
    container_image: str
    num_cpu_cores: int
    num_gpu: int
    # TODO: Share SKU enums from main repo.
    gpu: str
    # cpu: str
    memory: int
    replicas: int


class DeployServerlessRequest(BaseModel):
    app_name: str
    container_image: str
    num_cpu_cores: int
    num_gpu: int
    # TODO: Share SKU enums from main repo.
    gpu: str
    # cpu: str
    memory: int
    concurrency: int = 1
    min_scale: int = 0
    max_scale: int = 10


class DeployResponse(BaseModel):
    app_name: str


class DeleteResponse(BaseModel):
    # TODO: Needs better definition once the spec starts to settle.
    status: dict


class ListDeploymentsResponse(BaseModel):
    deployments: List[str]


class LogsResponse(BaseModel):
    logs: dict


class PredictResponse(BaseModel):
    result: dict


class DeploymentServiceV1(CoreApiService):
    base_path: str = "/api/v1/deployments"

    def deploy(self, deploy_request: DeployRequest) -> DeployResponse:
        r = self._post("/deploy", json=deploy_request.dict())
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return DeployResponse(app_name=j["app_name"])

    def deploy_serverless(
        self,
        deploy_serverless_request: DeployServerlessRequest,
        is_public: bool = False,
    ) -> DeployResponse:
        path = (
            is_public and "/deploy_serverless_public_endpoint" or "/deploy_serverless"
        )
        r = self._post(path, json=deploy_serverless_request.dict())
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return DeployResponse(app_name=j["app_name"])

    def list(self) -> ListDeploymentsResponse:
        r = self._get("/deployments")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return ListDeploymentsResponse(deployments=j["deployments"])

    def delete(self, app_name: str):
        r = self._delete(f"/{app_name}")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return DeleteResponse(status=j["status"])

    def logs(self, app_name: str):
        r = self._get(f"/{app_name}/logs")
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        j = r.json()
        return LogsResponse(logs=j["logs"])

    def predict(
        self,
        app_name: str,
        data: dict,
        is_serverless: bool = False,
        is_public: bool = False,
    ):
        params = dict(is_serverless=is_serverless, is_public=is_public)
        r = self._post(f"/{app_name}/predict", json=data, params=params)
        # TODO: Add better status checks and failed login reporting.
        r.raise_for_status()
        return PredictResponse(result=r.json())
