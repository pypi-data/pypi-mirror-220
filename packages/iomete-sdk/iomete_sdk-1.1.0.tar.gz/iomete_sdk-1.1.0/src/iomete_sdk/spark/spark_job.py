import logging
from dataclasses import dataclass

from iomete_sdk.api_utils import APIUtils

SPARK_JOB_ENDPOINT = "/api/v1/workspaces/{workspace_id}/spark-jobs"


@dataclass
class SparkJobApiClient:
    logger = logging.getLogger('SparkJobApiClient')

    workspace_id: str
    api_key: str
    base_url: str = None
    spark_job_endpoint: str = None
    api_utils: APIUtils = None

    def __post_init__(self):
        self.api_utils = APIUtils(api_key=self.api_key)

        controller_host = self._get_controller_host()
        self.logger.debug(f"Controller host: {controller_host}")

        self.base_url = f"https://{self._get_controller_host()}"
        self.spark_job_endpoint = self.base_url + SPARK_JOB_ENDPOINT.format(workspace_id=self.workspace_id)

    def _get_controller_host(self):
        result = self.api_utils.call(
            method="GET", url=f"https://account.iomete.com/api/v1/workspaces/{self.workspace_id}/info")
        return result["controller_endpoint"]

    def create_job(self, payload: dict):
        return self.api_utils.call(method="POST", url=self.spark_job_endpoint, payload=payload)

    def update_job(self, job_id: str, payload: dict):
        return self.api_utils.call(method="PUT", url=f"{self.spark_job_endpoint}/{job_id}", payload=payload)

    def get_jobs(self):
        return self.api_utils.call(method="GET", url=self.spark_job_endpoint)

    def get_job_by_id(self, job_id: str):
        return self.api_utils.call(method="GET", url=f"{self.spark_job_endpoint}/{job_id}")

    def delete_job_by_id(self, job_id: str):
        return self.api_utils.call(method="DELETE", url=f"{self.spark_job_endpoint}/{job_id}")

    def get_job_runs(self, job_id: str):
        return self.api_utils.call(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs")

    def submit_job_run(self, job_id: str, payload: dict):
        return self.api_utils.call(method="POST", url=f"{self.spark_job_endpoint}/{job_id}/runs", payload=payload)

    def cancel_job_run(self, job_id: str, run_id: str):
        return self.api_utils.call(method="DELETE", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}")

    def get_job_run_by_id(self, job_id: str, run_id: str):
        return self.api_utils.call(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}")

    def get_job_run_logs(self, job_id: str, run_id: str):
        return self.api_utils.call(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}/logs")

    def get_job_run_metrics(self, job_id: str, run_id: str):
        return self.api_utils.call(method="GET", url=f"{self.spark_job_endpoint}/{job_id}/runs/{run_id}/metrics")
