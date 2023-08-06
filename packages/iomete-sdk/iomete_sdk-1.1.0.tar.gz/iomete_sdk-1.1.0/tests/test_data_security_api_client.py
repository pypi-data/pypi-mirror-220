import random
import string
import unittest

from iomete_sdk.api_utils import ClientError
from iomete_sdk.security import DataSecurityApiClient
from iomete_sdk.security.policy_models import AccessPolicyView, DataMaskPolicyView, RowFilterPolicyView, PolicyResource, \
    PolicyItem, PolicyItemAccess, DataMaskPolicyItem, PolicyItemDataMaskInfo, RowFilterPolicyItem, \
    PolicyItemRowFilterInfo

TEST_TOKEN = "FdVawCi9GZW0P8sWuWdx0Xl0r6rLVpqEiX2LB7KLB/I="
WORKSPACE_ID = "pw9if-p22"


class TestDataSecurityApiClient(unittest.TestCase):
    def setUp(self):
        self.client = DataSecurityApiClient(
            workspace_id=WORKSPACE_ID,
            api_key=TEST_TOKEN,
        )

    def test_access_policies(self):
        # Create a policy
        policy_name = "iomete-sdk-automated-access-policy"
        new_policy = AccessPolicyView(
            name=policy_name,
            description="iomete-sdk-automated-access-policy",
            resources={
                "database": PolicyResource(values=["test_db"]),
                "table": PolicyResource(values=["test_tbl"]),
                "column": PolicyResource(values=["*"])
            },
            policy_items=[
                PolicyItem(
                    accesses=[PolicyItemAccess(type='select'),
                              PolicyItemAccess(type='update'),
                              PolicyItemAccess(type='create'),
                              PolicyItemAccess(type='read'),
                              PolicyItemAccess(type='write')],
                    users=['fuad@iomete.com'])
            ]
        )
        created_policy = self.client.create_access_policy(new_policy)

        # Verify the created policy
        self.assertEqual(created_policy.name, policy_name)

        # Retrieve created policy
        existing_policy = self.client.get_access_policy_by_name(policy_name)

        # Update the policy
        updated_policy = existing_policy
        updated_policy.description = 'updated'
        updated_policy = self.client.update_access_policy_by_name(policy_name, updated_policy)

        # Verify the updated policy
        self.assertEqual(updated_policy.description, 'updated')

        # Delete the policy
        self.client.delete_access_policy_by_id(updated_policy.id)

        # Verify the policy is deleted
        with self.assertRaises(ClientError):
            self.client.get_access_policy_by_name(policy_name)

    def test_data_mask_policies(self):
        # Create a policy
        policy_name = "iomete-sdk-automated-masking-policy"
        new_policy = DataMaskPolicyView(
            name=policy_name,
            description="iomete-sdk-automated-masking-policy",
            resources={
                "database": PolicyResource(values=["test_db"]),
                "table": PolicyResource(values=["test_tbl"]),
                "column": PolicyResource(values=["sensitive_column"])
            },
            data_mask_policy_items=[
                DataMaskPolicyItem(
                    accesses=[PolicyItemAccess(type='select')],
                    data_mask_info=PolicyItemDataMaskInfo(data_mask_type="MASK_SHOW_LAST_4"),
                    users=["fuad@iomete.com"]
                )]
        )
        created_policy = self.client.create_masking_policy(new_policy)

        # Verify the created policy
        self.assertEqual(created_policy.name, policy_name)

        # Retrieve created policy
        existing_policy = self.client.get_masking_policy_by_name(policy_name)

        # Update the policy
        updated_policy = existing_policy
        updated_policy.description = 'updated'
        updated_policy = self.client.update_masking_policy_by_name(policy_name, updated_policy)

        # Verify the updated policy
        self.assertEqual(updated_policy.description, 'updated')

        # Delete the policy
        self.client.delete_masking_policy_by_id(updated_policy.id)

        # Verify the policy is deleted
        with self.assertRaises(ClientError):
            self.client.get_masking_policy_by_id(updated_policy.id)

    def test_row_filter_policies(self):
        # Create a policy
        policy_name = "iomete-sdk-automated-row-filter-policy"
        new_policy = RowFilterPolicyView(
            name=policy_name,
            description="iomete-sdk-automated-masking-policy",
            resources={
                "database": PolicyResource(values=["test_db"]),
                "table": PolicyResource(values=["test_tbl"])
            },
            row_filter_policy_items=[
                RowFilterPolicyItem(
                    row_filter_info=PolicyItemRowFilterInfo(filter_expr="1 == 1"),
                    accesses=[PolicyItemAccess(type='select')],
                    users=["fuad@iomete.com"],
                    groups=[]
                )]
        )
        created_policy = self.client.create_filter_policy(new_policy)

        # Verify the created policy
        self.assertEqual(created_policy.name, policy_name)

        # Retrieve created policy
        existing_policy = self.client.get_filter_policy_by_name(policy_name)

        # Update the policy
        updated_policy = existing_policy
        updated_policy.description = 'updated'
        updated_policy = self.client.update_filter_policy_by_name(policy_name, updated_policy)

        # Verify the updated policy
        self.assertEqual(updated_policy.description, 'updated')

        # Delete the policy
        self.client.delete_filter_policy_by_id(updated_policy.id)

        # Verify the policy is deleted
        with self.assertRaises(ClientError):
            self.client.get_filter_policy_by_id(updated_policy.id)
