from backend.app.services.email.gmail import (
    get_gmail_service,
    send_email,
)


def send_approved_email(email, draft):
    service = get_gmail_service()

    result = send_email(
        service=service,
        to=email.sender,
        subject=draft.subject,
        body=draft.body,
        thread_id=email.provider_thread_id,
    )

    return {
        "success": True,
        "provider_message_id": result.get("id"),
        "thread_id": result.get("threadId"),
    }