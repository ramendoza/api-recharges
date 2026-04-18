import requests
from django.conf import settings


def _build_url(path: str) -> str:
    return f"{settings.BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def fetch_send_recharges() -> list:
    response = requests.get(_build_url("send-recharges"), timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_recharge_prices(user) -> list:
    try:
        read_key = user.userprofile.read_key
    except AttributeError as exc:
        raise ValueError("Authenticated user does not have a profile with read_key.") from exc
    print(_build_url("recharge"))
    response = requests.get(
        _build_url("recharge"),
        headers={"X-Authorization": read_key, 'content-type': 'application/json'},
        timeout=30,
        verify=False
    )
    response.raise_for_status()
    return response.json()


def send_recharge(payload: dict, user) -> dict:
    try:
        write_key = user.userprofile.write_key
    except AttributeError as exc:
        raise ValueError("Authenticated user does not have a profile with write_key.") from exc
    response = requests.post(_build_url("recharge"),
                             json=payload,
                             timeout=30,
                             headers={"X-Authorization": write_key, 'content-type': 'application/json'},
                             verify=False
                             )
    response.raise_for_status()
    return response.json()


def send_telegram_recharge_notification(username: str, recipient: str) -> None:
    if not settings.TELEGRAM_BOT_KEY or not settings.TELEGRAM_GROUP_ID:
        return

    message = (
        "Recharge sent\n"
        f"User: {username}\n"
        f"Recipient: {recipient}"
    )

    requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_KEY}/sendMessage",
        json={"chat_id": settings.TELEGRAM_GROUP_ID, "text": message},
        timeout=10,
    ).raise_for_status()
