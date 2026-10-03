from backend.app.db.session import SessionLocal
from backend.app.services.workflow.storage import create_workflow


db = SessionLocal()

try:
    workflow = create_workflow(
        db=db,
        name="Quotation Lead Workflow",
        description="Handle customer quotation requests",
        trigger_category="QUOTATION",
        min_confidence=0.80,
    )

    print("\n--- WORKFLOW CREATED ---")
    print("ID:", workflow.id)
    print("Name:", workflow.name)
    print("Category:", workflow.trigger_category)
    print("Minimum confidence:", workflow.min_confidence)
    print("Enabled:", workflow.enabled)

finally:
    db.close()