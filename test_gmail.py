from backend.app.services.email.ingestion import (
    fetch_latest_emails,
)


emails = fetch_latest_emails(limit=5)

print(f"Fetched {len(emails)} emails")

for email in emails:
    print("\n--- EMAIL ---")
    print("From:", email["sender_email"])
    print("Subject:", email["subject"])
    print("Thread:", email["provider_thread_id"])
    print("Body:", email["body"][:300])