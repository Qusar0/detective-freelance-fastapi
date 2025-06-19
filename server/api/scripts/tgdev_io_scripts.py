import requests

from server.api.scripts.utils import renew_tgdev_balance


url = "https://api.tgdev.io/tgscan/v1/search"
balance_url = "https://api.tgdev.io/tgscan/v1/balance"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/117.0.0.0 Safari/537.36"
    ),
    "Api-Key": "f6d604279a644923940d7583df9fa3b2",
    "Content-Type": "application/json"
}


def get_tgdev_balance():
    resp = requests.post(balance_url, headers=headers)
    balance_info = resp.json()["result"]["num_credits"]
    return balance_info


async def get_groups_tgdev_method(telegram_id: str):
    response_user_groups = []
    data = {"query": telegram_id}
    resp = requests.post(url, headers=headers, data=data)
    info = resp.json()

    user_groups = info["result"]["groups"]

    for group in user_groups:
        response_user_groups.append("@" + group['username'] + " / " + group["title"] + ' | ' + group['date_updated'])

    tgdev_balance = get_tgdev_balance()
    await renew_tgdev_balance(tgdev_balance)

    return response_user_groups
