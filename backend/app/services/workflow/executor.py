import json

from sqlalchemy.orm import Session

from backend.app.models.classification import EmailClassificationRecord
from backend.app.models.email import Email
from backend.app.models.extraction import SalesLeadExtractionRecord
from backend.app.models.workflow import Workflow

from backend.app.services.actions.dispatcher import dispatch_action
from backend.app.services.workflow.action_definition_storage import (
    get_workflow_actions,
)
from backend.app.services.workflow.action_storage import save_workflow_action
from backend.app.services.workflow.engine import workflow_matches
from backend.app.services.workflow.run_storage import (
    start_workflow_run,
    complete_workflow_run,
    fail_workflow_run,
)


def execute_workflow(
    db: Session,
    workflow: Workflow,
    email: Email,
    classification: EmailClassificationRecord,
    extraction: SalesLeadExtractionRecord | None = None,
) -> list[dict]:

    if not workflow_matches(
        workflow=workflow,
        classification=classification,
    ):
        return []

    run = start_workflow_run(
        db=db,
        workflow_id=workflow.id,
        email_id=email.id,
    )

    actions = []

    try:
        workflow_actions = get_workflow_actions(
            db=db,
            workflow_id=workflow.id,
        )

        for action_definition in workflow_actions:

            action_type = action_definition.action_type

            try:
                result = dispatch_action(
                    db=db,
                    action_type=action_type,
                    email=email,
                    classification=classification,
                    extraction=extraction,
                    workflow_run=run,
                )

                save_workflow_action(
                    db=db,
                    workflow_run_id=run.id,
                    action_type=action_type,
                    status="SUCCESS",
                    result=json.dumps(result),
                )

                actions.append(result)

            except Exception as action_error:

                save_workflow_action(
                    db=db,
                    workflow_run_id=run.id,
                    action_type=action_type,
                    status="FAILED",
                    error=str(action_error),
                )

                raise

        complete_workflow_run(
            db=db,
            run=run,
        )

        return actions

    except Exception as error:

        fail_workflow_run(
            db=db,
            run=run,
            error=str(error),
        )

        raise