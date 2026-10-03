from enum import Enum

from pydantic import BaseModel


class WorkflowActionType(str, Enum):
    CREATE_LEAD = "CREATE_LEAD"
    CREATE_TICKET = "CREATE_TICKET"
    SEND_NOTIFICATION = "SEND_NOTIFICATION"
    GENERATE_DRAFT = "GENERATE_DRAFT"


class WorkflowCondition(BaseModel):
    category: str | None = None
    min_confidence: float | None = None


class WorkflowAction(BaseModel):
    type: WorkflowActionType


class WorkflowDefinition(BaseModel):
    name: str
    description: str | None = None
    enabled: bool = True
    condition: WorkflowCondition
    actions: list[WorkflowAction]