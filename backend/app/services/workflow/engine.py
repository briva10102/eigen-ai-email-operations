from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.workflow import Workflow


def workflow_matches(
    workflow: Workflow,
    classification: EmailClassificationRecord,
) -> bool:

    if not workflow.enabled:
        return False

    if workflow.trigger_category != classification.category.value:
        return False

    if classification.confidence < workflow.min_confidence:
        return False

    return True