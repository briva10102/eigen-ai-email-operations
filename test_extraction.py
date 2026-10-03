from backend.app.services.ai.extractor import extract_sales_lead


result = extract_sales_lead(
    sender="customer@example.com",
    subject="Solar installation quotation",
    body="""
Hi,

My name is Rahul Sharma.

I am interested in installing a 5kW solar system
for my house in Mumbai.

My budget is around ₹3 lakh.

I would like to install it next month.

You can contact me at 9876543210.

Please send me a quotation.

Thanks,
Rahul
""",
)

print("\n--- SALES LEAD EXTRACTION ---")

print("Name:", result.name)
print("Email:", result.email)
print("Phone:", result.phone)
print("Company:", result.company)
print("Location:", result.location)
print("Product:", result.product_interest)
print("Budget:", result.budget)
print("Timeline:", result.timeline)
print("Requirements:", result.requirements)
print("Urgency:", result.urgency)