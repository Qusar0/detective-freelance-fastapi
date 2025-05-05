from server.api.scripts.utils import renew_ibhldr_balance
import requests


url = "https://api.ibhldr.com:48480/v2/get-interests/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
           "Authorization": "Bearer 9220308ca1fcef03d76d16af52770598cf989a59",
           "Content-Type": "application/json"}


async def get_interests(telegram_id):
    data = {"uid": telegram_id, "interests": "true"}

    resp = requests.post(url, headers=headers, json=data)
    info = resp.json()
    interests = info['interests']
    balance = info['balance']
    await renew_ibhldr_balance(balance)

    interests_html = ""
    for i in interests:
        block_name = i['b']

        try:
            categories = i['cs']
            for category in categories:
                all_tags = []
                try:
                    tags = category['ts']
                    for tag in tags:
                        all_tags.append(tag['t'])
                    interests_html += f"""<tr>
                                                    <td>{block_name}</td>
                                                    <td>{category['c']}</td>
                                                    <td>{", ".join(all_tags)}</td>
                                                </tr>"""
                except KeyError:
                    interests_html += f"""<tr>
                                              <td>{block_name}</td>
                                              <td>{category['c']}</td>
                                              <td></td>
                                          </tr>
                                       """
        except KeyError:
            interests_html += f"""<tr>
                                          <td>{block_name}</td>
                                          <td></td>
                                          <td></td>
                                      </tr>
                                   """

    return interests_html


async def get_groups_ibhldr_method(telegram_id):
    data = {"uid": telegram_id, "groups": "true"}

    resp = requests.post(url, headers=headers, json=data)

    info = resp.json()

    groups = info['groups']
    balance = info['balance']
    await renew_ibhldr_balance(balance)

    separated_groups = groups.split("\n")

    return separated_groups


async def get_profiles(telegram_id):
    data = {"uid": telegram_id, "profiles": "true"}

    resp = requests.post(url, headers=headers, json=data)

    info = resp.json()
    profiles = info['profiles']
    balance = info['balance']
    await renew_ibhldr_balance(balance)

    separated_profiles = profiles.split("\n")

    return separated_profiles


async def get_phones(telegram_id):
    data = {"uid": telegram_id, "phones": "true"}

    resp = requests.post(url, headers=headers, json=data)

    info = resp.json()
    phones = info['phones']
    balance = info['balance']
    await renew_ibhldr_balance(balance)

    return phones
