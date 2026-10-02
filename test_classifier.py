from backend.app.services.ai.classifier import classify_email


result = classify_email(
    sender="customer@example.com",
    subject="Interested in installing solar panels",
    body="""
Hi,

I am interested in installing solar panels for my house.
Could you please provide a quotation?

My location is Mumbai and I would like to get this done next month.

Thanks
""",
)

print("\n--- CLASSIFICATION ---")
print("Category:", result.category)
print("Confidence:", result.confidence)
print("Urgency:", result.urgency)
print("Intent:", result.intent)
print("Reason:", result.reason)