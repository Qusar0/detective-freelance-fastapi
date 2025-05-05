import requests


def get_tags_in_getcontact(number):
    headers = {
        'x-bot-id': '234343072',
        'x-bot-token': 'RQjogf9Sh1k/V/evxNGoa5PtTWuy5ODz0kdH6crzomg=',
        'x-api-key': 'iKKjHjnPOr9QoL93PtAIZ7gHhSpyxA2a24qN4Xrt',
        'Content-Type': 'application/json',
    }

    r = requests.post(
        'https://r0cyk3wpdg.execute-api.us-east-2.amazonaws.com/default/apiv2',
        headers=headers,
        json={"phone": number}
    )

    contacs_json = r.json()
    requests_left = contacs_json['data']['subscription']['remainingRequestCount']
    sources = contacs_json['data']['responce']

    list_tags = []
    for source in sources:
        if source['source'] == 'getcontact':
            response = source['results']['response']
            if 'tagCount' in response and response['tagCount'] > 0:
                tags = response.get('tags', [])
                list_tags.extend([tag['tag'] for tag in tags if 'tag' in tag])
            else:
                print(f"Для номера {number} теги не найдены.")

    return list_tags, requests_left


if __name__ == "__main__":
    leaks, requests = get_tags_in_getcontact('+79276030425')
    print(leaks)
    test = []
    i = 0
    for item in leaks:
        if item in test:
            print(item)
            i += 1
        test.append(item)
    print('\n')
    print(requests)
