from dataclasses import dataclass
from typing import Optional, List, Dict

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PolicyResource:
    values: List[str] = None
    is_excludes: bool = False


@dataclass_json
@dataclass
class PolicyItemAccess:
    type: str = None
    is_allowed: bool = True


@dataclass_json
@dataclass
class PolicyItem:
    users: List[str] = None
    groups: List[str] = None
    accesses: List[PolicyItemAccess] = None


@dataclass_json
@dataclass
class AccessPolicyView:
    id: Optional[int] = None
    is_enabled: bool = True
    name: str = ""
    description: Optional[str] = None
    resources: Dict[str, PolicyResource] = None
    additional_resources: List[Dict[str, PolicyResource]] = None
    policy_items: List[PolicyItem] = None
    deny_policy_items: List[PolicyItem] = None


@dataclass_json
@dataclass
class PolicyItemDataMaskInfo:
    # data_mask_type options: MASK, MASK_SHOW_LAST_4, MASK_SHOW_FIRST_4, MASK_HASH, MASK_NULL, MASK_NONE
    data_mask_type: Optional[str] = None,
    value_expr: Optional[str] = None


@dataclass_json
@dataclass
class DataMaskPolicyItem:
    accesses: List[PolicyItemAccess] = None
    data_mask_info: PolicyItemDataMaskInfo = None
    users: List[str] = None
    groups: List[str] = None


@dataclass_json
@dataclass
class DataMaskPolicyView:
    id: Optional[int] = None
    is_enabled: bool = True
    name: str = ""
    description: Optional[str] = None
    resources: Dict[str, PolicyResource] = None
    additional_resources: List[Dict[str, PolicyResource]] = None
    data_mask_policy_items: List[DataMaskPolicyItem] = None


@dataclass_json
@dataclass
class PolicyItemRowFilterInfo:
    filter_expr: str = None


@dataclass_json
@dataclass
class RowFilterPolicyItem:
    row_filter_info: PolicyItemRowFilterInfo = None
    accesses: List[PolicyItemAccess] = None
    users: List[str] = None
    groups: List[str] = None


@dataclass_json
@dataclass
class RowFilterPolicyView:
    id: Optional[int] = None
    is_enabled: bool = True
    name: str = ""
    description: Optional[str] = None
    resources: Dict[str, PolicyResource] = None
    additional_resources: List[Dict[str, PolicyResource]] = None
    row_filter_policy_items: List[RowFilterPolicyItem] = None
