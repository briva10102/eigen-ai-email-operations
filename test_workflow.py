from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.workflow import Workflow
from backend.app.schemas.classification import EmailCategory
from backend.app.services.workflow.engine import workflow_matches


workflow = Workflow(
    name="Sales Lead Workflow",
    description="Handle incoming sales leads",
    enabled=True,
    trigger_category="QUOTATION",
    min_confidence=0.80,
)

classification = EmailClassificationRecord(
    email_id=1,
    category=EmailCategory.QUOTATION,
    confidence=0.90,
    urgency="Medium",
    intent="Customer wants a solar quotation",
    reason="The customer explicitly requested a quotation.",
    model="gemini-2.5-flash-lite",
)

result = workflow_matches(
    workflow=workflow,
    classification=classification,
)

print("Workflow matches:", result)