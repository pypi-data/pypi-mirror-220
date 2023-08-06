import logging
from dataclasses import dataclass
from typing import List

from iomete_sdk.api_utils import ClientError, APIUtils
from iomete_sdk.security.policy_models import AccessPolicyView, RowFilterPolicyView, DataMaskPolicyView

DATA_SECURITY_ENDPOINT = "/api/v1/workspaces/{workspace_id}/data-security"


@dataclass
class DataSecurityApiClient:
    logger = logging.getLogger('DataSecurityApiClient')

    workspace_id: str
    api_key: str
    base_url: str = None
    data_security_endpoint: str = None
    api_utils: APIUtils = None

    def __post_init__(self):
        self.api_utils = APIUtils(self.api_key)

        controller_host = self._get_controller_host()
        self.logger.debug(f"Controller host: {controller_host}")

        self.base_url = f"https://{self._get_controller_host()}"
        self.data_security_endpoint = self.base_url + DATA_SECURITY_ENDPOINT.format(workspace_id=self.workspace_id)

    def _get_controller_host(self):
        result = self.api_utils.call(
            method="GET", url=f"https://account.iomete.com/api/v1/workspaces/{self.workspace_id}/info")
        return result["controller_endpoint"]

    def create_access_policy(self, policy: AccessPolicyView) -> AccessPolicyView:
        data = self.api_utils.call(method="POST",
                                   url=f"{self.data_security_endpoint}/access/policy",
                                   payload=policy.to_dict())

        return AccessPolicyView(**data)

    def get_access_policies(self) -> List[AccessPolicyView]:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/access/policy")

        return [AccessPolicyView(**policy) for policy in data]

    def get_access_policy_by_name(self, policy_name: str) -> AccessPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/access/policy/name/{policy_name}")

        return AccessPolicyView(**data)

    def get_access_policy_by_id(self, policy_id: str) -> AccessPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/access/policy/{policy_id}")

        return AccessPolicyView(**data)

    def update_access_policy_by_name(self, policy_name: str, policy: AccessPolicyView) -> AccessPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/access/policy/name/{policy_name}",
                                   payload=policy.to_dict())

        return AccessPolicyView(**data)

    def update_access_policy_by_id(self, policy_id: str, policy: AccessPolicyView) -> AccessPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/access/policy/{policy_id}",
                                   payload=policy.to_dict())

        return AccessPolicyView(**data)

    def delete_access_policy_by_id(self, policy_id: str):
        self.api_utils.call(method="DELETE",
                            url=f"{self.data_security_endpoint}/access/policy/{policy_id}")

    def create_filter_policy(self, policy: RowFilterPolicyView) -> RowFilterPolicyView:
        data = self.api_utils.call(method="POST",
                                   url=f"{self.data_security_endpoint}/filter/policy",
                                   payload=policy.to_dict())

        return RowFilterPolicyView(**data)

    def get_filter_policies(self) -> List[RowFilterPolicyView]:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/filter/policy")

        return [RowFilterPolicyView(**policy) for policy in data]

    def get_filter_policy_by_name(self, policy_name: str) -> RowFilterPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/filter/policy/name/{policy_name}")

        return RowFilterPolicyView(**data)

    def get_filter_policy_by_id(self, policy_id: str) -> RowFilterPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/filter/policy/{policy_id}")

        return RowFilterPolicyView(**data)

    def update_filter_policy_by_name(self, policy_name: str, policy: RowFilterPolicyView) -> RowFilterPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/filter/policy/name/{policy_name}",
                                   payload=policy.to_dict())

        return RowFilterPolicyView(**data)

    def update_filter_policy_by_id(self, policy_id: str, policy: RowFilterPolicyView) -> RowFilterPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/filter/policy/{policy_id}",
                                   payload=policy.to_dict())

        return RowFilterPolicyView(**data)

    def delete_filter_policy_by_id(self, policy_id: str):
        self.api_utils.call(method="DELETE",
                            url=f"{self.data_security_endpoint}/filter/policy/{policy_id}")

    def create_masking_policy(self, policy: DataMaskPolicyView) -> DataMaskPolicyView:
        data = self.api_utils.call(method="POST",
                                   url=f"{self.data_security_endpoint}/mask/policy",
                                   payload=policy.to_dict())

        return DataMaskPolicyView(**data)

    def get_masking_policies(self) -> List[DataMaskPolicyView]:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/mask/policy")

        return [DataMaskPolicyView(**policy) for policy in data]

    def get_masking_policy_by_name(self, policy_name: str) -> DataMaskPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/mask/policy/name/{policy_name}")

        return DataMaskPolicyView(**data)

    def get_masking_policy_by_id(self, policy_id: str) -> DataMaskPolicyView:
        data = self.api_utils.call(method="GET",
                                   url=f"{self.data_security_endpoint}/mask/policy/{policy_id}")

        return DataMaskPolicyView(**data)

    def update_masking_policy_by_name(self, policy_name: str, policy: DataMaskPolicyView) -> DataMaskPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/mask/policy/name/{policy_name}",
                                   payload=policy.to_dict())

        return DataMaskPolicyView(**data)

    def update_masking_policy_by_id(self, policy_id: str, policy: DataMaskPolicyView) -> DataMaskPolicyView:
        data = self.api_utils.call(method="PUT",
                                   url=f"{self.data_security_endpoint}/mask/policy/{policy_id}",
                                   payload=policy.to_dict())

        return DataMaskPolicyView(**data)

    def delete_masking_policy_by_id(self, policy_id: str):
        self.api_utils.call(method="DELETE",
                            url=f"{self.data_security_endpoint}/mask/policy/{policy_id}")
