from datetime import datetime, timezone
from email.utils import parseaddr
from typing import Any


def normalize_gmail_message(message: dict[str, Any]) -> dict[str, Any]:
    headers = message.get("payload", {}).get("headers", [])

    header_map = {
        header["name"].lower(): header["value"]
        for header in headers
    }

    sender_name, sender_email = parseaddr(
        header_map.get("from", "")
    )

    return {
        "provider_message_id": message["id"],
        "provider_thread_id": message.get("threadId"),
        "sender_name": sender_name,
        "sender_email": sender_email,
        "recipients": header_map.get("to", ""),
        "subject": header_map.get("subject", ""),
        "body": extract_body(message.get("payload", {})),
        "received_at": datetime.fromtimestamp(
            int(message.get("internalDate", "0")) / 1000,
            tz=timezone.utc
        ),
    }


import base64
def decode_body(data: str) -> str:
    decoded = base64.urlsafe_b64decode(data + "===")
    return decoded.decode("utf-8", errors="replace")


def extract_body(payload: dict[str, Any]) -> str:
    body = payload.get("body", {})

    if body.get("data"):
        return decode_body(body["data"])

    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain":
            part_body = part.get("body", {})

            if part_body.get("data"):
                return decode_body(part_body["data"])

    return ""