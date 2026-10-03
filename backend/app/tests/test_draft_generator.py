from backend.app.services.ai.draft_generator import generate_email_draft


result = generate_email_draft(
    sender="customer@example.com",
    subject="Solar Installation Quotation Request",
    body="""
Hi,

I am interested in installing solar panels for my house.
Could you please provide a quotation?

Thanks,
Rahul
""",
)

print("\n--- GENERATED DRAFT ---")
print("Subject:", result["subject"])
print("Body:")
print(result["body"])