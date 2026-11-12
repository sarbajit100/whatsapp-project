from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from .config import settings


_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        _client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    return _client


def send_whatsapp_message(to: str, message: str) -> str:
    """Send a WhatsApp message and return the Twilio message SID."""
    client = get_client()
    try:
        msg = client.messages.create(
            from_=settings.twilio_whatsapp_from,
            to=to,
            body=message,
        )
        return msg.sid
    except TwilioRestException as exc:
        raise RuntimeError(f"Twilio error {exc.code}: {exc.msg}") from exc
