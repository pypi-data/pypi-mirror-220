# Generated by ariadne-codegen on 2023-07-18 13:55
# Source: operations.graphql

from pydantic import Field

from .base_model import BaseModel


class ReportEntitlementCheckRequested(BaseModel):
    report_entitlement_check_requested: bool = Field(
        alias="reportEntitlementCheckRequested"
    )


ReportEntitlementCheckRequested.update_forward_refs()
