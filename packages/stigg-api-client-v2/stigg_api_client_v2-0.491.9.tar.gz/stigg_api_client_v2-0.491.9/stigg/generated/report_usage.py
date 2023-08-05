# Generated by ariadne-codegen on 2023-07-18 13:55
# Source: operations.graphql

from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class ReportUsage(BaseModel):
    create_usage_measurement: "ReportUsageCreateUsageMeasurement" = Field(
        alias="createUsageMeasurement"
    )


class ReportUsageCreateUsageMeasurement(BaseModel):
    id: str
    current_usage: Optional[float] = Field(alias="currentUsage")
    next_reset_date: Optional[Any] = Field(alias="nextResetDate")
    timestamp: Any


ReportUsage.update_forward_refs()
ReportUsageCreateUsageMeasurement.update_forward_refs()
