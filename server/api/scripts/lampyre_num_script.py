from datetime import datetime

import requests
import json

import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code
)

import base64

default_methods = [
    'phone_viber_v1',
    'phone_truecaller_v1',
    'phone_twitter_restore_v1',
    'phone_leakcheck_v1',
    'phone_instagram_restore_v1',
    'phone_yandex_search_v1',
    'phone_fb_restore_v1',
    'phone_foursquare_v1',
    'phone_skype_v1',
    'phone_telegram_v1',
    'phone_icq_v1',
    'phone_allcon_v1',
    'phone_whatsapp_v1',
    'phone_aeroflot_v1',
    'phone_amazon_checker_v1',
    'phone_microsoft_checker_v1',
    'phone_google_checker_v1',
]

usa_methods = [
    'phone_thatsthem_v1',
    "phone_openpeoplesearch_v1",
    "phone_whitepages_v1",
    "phone_aihitdata_v1",
]

other_country_methods = [
    'phone_advancedbackgroundchecks_v1',
    'phone_syncme_v1',
]

# нужно затестить
test = [
    'phone_whatsapp_v1'
]

# практически всегда долго работают
too_long = [
    "phone_google_search_v1",
    "phone_google_id_v1",
]

test2 = ['phone_telegram_v1']


class Lampyre:
    def __init__(self):
        self.token = "a05b0f96-008d-4e81-b5ea-b0792c764a1d"
        self.lampyre_handler = LampyreResultsHandler()
        self.tasks = []
        self.no_results_html = ''

    def main(self, number):
        methods = self.define_methods_type_by_num(number)

        for method in methods:
            task_info = self.start_task(method, number)
            task_name = task_info[0]
            task_id = task_info[1]
            self.tasks.append({
                "task_name": task_name,
                "task_id": task_id,
                "iterated_times": 0,
            })

        task_results = self.iterate_tasks()
        lampyre_html = ''
        for task in task_results:
            task_name = task['task_name']
            task_result = task['result']

            handled_result = self.lampyre_handler.distribute_task(
                task_name,
                task_result,
            )
            lampyre_html += self.form_lampyre_html(handled_result)
        lampyre_html += self.no_results_html
        return lampyre_html

    def start_task(self, task_name: str, number: str):
        response = requests.post(
            url=f"https://api.lighthouse.lampyre.io/api/1.0/tasks/{task_name}",
            json={
                "token": self.token,
                "task_info": {
                    "phone": number,
                },
            }
        )
        resp_json = json.loads(response.text)
        task_id = resp_json['task_id']
        return task_name, task_id

    def get_result(self, task_name, task_id) -> dict:
        response = requests.get(
            url=f"https://api.lighthouse.lampyre.io/api/1.0/tasks/{task_name}/{task_id}?token={self.token}")

        return response.json()

    def iterate_tasks(self):
        # 2 - the task hasn't been started
        # 3 - the task is in process
        # 0 - the task has been completed succesfully
        # 1 - the task has been completed with errors
        results = []

        while self.tasks:
            for task_info in self.tasks:
                task_name = task_info["task_name"]
                task_id = task_info["task_id"]
                task_iterated_times = task_info["iterated_times"]

                task_result = self.get_result(task_name, task_id)
                task_status = task_result['task_status']

                if task_iterated_times > 100 and task_status != 0:
                    task_status = 3

                if task_status == 0:
                    print("OK", task_result)
                    try:
                        result = task_result['result']['result'][0]['output'][0]
                        output = {
                            "task_name": task_name,
                            "result": result,
                        }
                    except IndexError:
                        output = {"task_name": task_name, "result": {}}
                    results.append(output)
                    self.tasks.remove(task_info)
                elif task_status == 3:
                    continue
                elif task_status == 1:
                    output = {"task_name": task_name, "result": "ERROR"}
                    results.append(output)
                    self.tasks.remove(task_info)

                task_iterated_times += 1
        return results

    @staticmethod
    def define_methods_type_by_num(number):
        phonenum = phonenumbers.parse(number)
        region_code = region_code_for_country_code(phonenum.country_code)

        if region_code == "US":
            default_methods.extend(usa_methods)
            default_methods.extend(other_country_methods)

        elif region_code != "RU":
            default_methods.extend(other_country_methods)

        return default_methods

    def form_lampyre_html(self, results):
        if isinstance(results, str) or results == 'ERROR' or results == {}:
            return ''

        html = ''
        result_str = ''
        verbose_name = results['verbose_name']

        try:
            if results['результат']:
                result_str = results['результат']
                self.no_results_html += f"""<tr>\n    <td>{verbose_name}</td>\n    <td class="empty-result">{result_str}</td>\n</tr>"""
                return ''
        except KeyError:
            pass

        if len(results.items()) == 2 and 'exists' in results:
            if results['exists'] is False:
                result_str += '<span class="account-dont-exist">Аккаунт не зарегистрирован</span><br>'
                self.no_results_html += f"""<tr>\n    <td>{verbose_name}</td>\n    <td>{result_str}</td>\n</tr>"""
                return ''
            else:
                pass

        try:
            photo_str = ''
            for key, value in results.items():
                if key == 'verbose_name':
                    continue
                elif key == 'lastseen':
                    result_str += f'''<tr> <td class="td-key">Последний раз в сети</td> <td>{datetime.fromtimestamp(value)}</td></tr>'''
                elif key == 'exists':
                    if value:
                        result_str += '<tr> <td class="td-key">Аккаунт</td> <td class="account-exist">зарегистрирован</td></tr>'
                    else:
                        result_str += '<tr> <td class="td-key">Аккаунт</td> <td class="account-dont-exist">зарегистрирован</td></tr>'
                elif key == 'avatar_fileid' or key == 'photo_fileid':
                    image_data = get_files(value)
                    photo_str += f'<tr><td class="td-key">Фото аккаунта</td>  <td>{image_data}</td></tr>'
                elif isinstance(value, list):
                    result_str += f'<tr><td class="td-key">{key}</td> <td>{", ".join(value)}</td></tr>'
                else:
                    if 'http' in value:
                        result_str += f'<tr><td class="td-key">{key}</td> <td><a class="td-link" href="{value}">{value}</a></td></tr>'
                    else:
                        result_str += f'<tr><td class="td-key">{key}</td> <td>{value}</td></tr>'
            result_str += photo_str
            if result_str != '':
                html += f"""<tr>\n    <td>{verbose_name}</td>\n    <td><table cellspacing="0"><tbody>{result_str}</tbody></table></td>\n</tr>"""
        except Exception as e:
            print("ОШИБКА ПРИ task_result.items()", e, '\n', results)
        return html


class LampyreResultsHandler:

    def distribute_task(self, task_name, result):
        res = None
        match task_name:
            case "phone_viber_v1":
                res = self.viber_handler(result)
            case "phone_truecaller_v1":
                res = self.truecaller_handler(result)
            case "phone_google_search_v1":
                res = self.google_search_handler(result)
            case "phone_twitter_restore_v1":
                res = self.twitter_restore_handler(result)
            case "phone_leakcheck_v1":
                res = self.leakcheck_handler(result)
            case "phone_instagram_restore_v1":
                res = self.instagram_restore_handler(result)
            case "phone_yandex_search_v1":
                res = self.yandex_search_handler(result)
            case "phone_fb_restore_v1":
                res = self.fb_restore_handler(result)
            case "phone_foursquare_v1":
                res = self.foursquare_handler(result)
            case "phone_skype_v1":
                res = self.skype_handler(result)
            case "phone_telegram_v1":
                res = self.telegram_handler(result)
            case "phone_icq_v1":
                res = self.icq_handler(result)
            case "phone_allcon_v1":
                res = self.allcon_handler(result)
            case "phone_google_id_v1":
                res = self.google_id_handler(result)
            case "phone_thatsthem_v1":
                res = self.thatsthem_handler(result)
            case "phone_advancedbackgroundchecks_v1":
                res = self.advancedbackgroundchecks_handler(result)
            case "phone_syncme_v1":
                res = self.syncme_handler(result)
        return res

    @staticmethod
    def handler(
        data,
        result_vars,
        result_vars_into_list=None,
        verbose_name=None,
    ):
        result = {}
        if data is [] or data == "ERROR":
            return result

        for var in result_vars:
            res = data.get(var)

            if res is not None:
                if isinstance(res, list) and isinstance(res[0], dict):
                    result[var] = {}
                    list_res = res[0]
                    for list_var in result_vars_into_list:
                        res = list_res.get(list_var)

                        if res is not None:
                            result[var][list_var] = res
                else:
                    result[var] = res
        result['verbose_name'] = verbose_name
        return result

    def viber_handler(self, data):
        verbose_name = 'Viber'
        result_vars = ["fullname", "lastseen", "photo_fileid"]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def truecaller_handler(self, data):
        verbose_name = 'TrueCaller'
        result_vars = [
            "fullname",
            "firstname",
            "lastname",
            "email",
            "facebook_profile_uid",
            "facebook_profile_url",
            "avatar_url",
            "avatar_fileid",
            "latitude",
            "longitude",
            "city",
            "gender",
            "carrier",
            "country_code",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def google_search_handler(self, data):
        verbose_name = 'Google'
        result_vars = ["url", "title", "description"]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def twitter_restore_handler(self, data):
        verbose_name = 'Twitter'
        result_vars = [
            "exists",
            "has_many_accounts",
            "email_part",
            "phone_part",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def leakcheck_handler(self, data):
        verbose_name = 'Пароли, обнаруженные в утечках'
        result_vars = [
            "password",
            "last_modified_date",
            "domain",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def instagram_restore_handler(self, data):
        verbose_name = 'Instagram'
        result_vars = ["exists"]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def yandex_search_handler(self, data):
        verbose_name = 'Яндекс'
        result_vars = ["url", "title", "description"]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def fb_restore_handler(self, data):
        verbose_name = 'Facebook'
        result_vars = [
            "email_part",
            "phone_part",
            "fullname",
            "avatar_url",
            "avatar_fileid",
            "exists",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def foursquare_handler(self, data):
        verbose_name = 'Foursquare'
        result_vars = [
            "foursquare_profile_uid",
            "foursquare_profile_url",
            "avatar_url",
            "avatar_fileid",
            "city",
            "longitude",
            "latitude",
            "firstname",
            "lastname",
            "fullname",
            "gender",
            "bio",
            "twitter",
            "instagram",
            "facebook",
        ]
        result_vars_into_list = [
            "twitter_profile_url",
            "twitter_profile_uid",
            "instagram_profile_url",
            "instagram_profile_uid",
            "facebook_profile_uid",
            "facebook_profile_url",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            result_vars_into_list,
            verbose_name=verbose_name,
        )
        return handled_info

    def skype_handler(self, data):
        verbose_name = 'Skype'
        result_vars = [
            "skype_profile_uid",
            "skype_profile_deep_link",
            "skype_contact_type",
            "avatar_url",
            "avatar_fileid",
            "latitude",
            "longitude",
            "location",
            "fullname",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def telegram_handler(self, data):
        verbose_name = 'Telegram'
        result_vars = [
            "firstname",
            "lastname",
            "username",
            "lastseen",
            "bio",
            "telegram_profile_uid",
            "avatar_fileid",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def icq_handler(self, data):
        verbose_name = 'ICQ'
        result_vars = [
            "icq_profile_uid",
            "icq_profile_url",
            "avatar_url",
            "avatar_fileid",
            "username",
            "fullname",
            "lastname",
            "firstname",
            "latitude",
            "longitude",
            "location",
            "birthday",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def allcon_handler(self, data):
        verbose_name = 'Allcon'
        result_vars = [
            "fullname",
            "carrier",
            "category",
            "company_name",
            "description",
            "rating",
            "spam_count",
            "location",
        ]
        result_vars_into_list = [
            "location",
            "latitude",
            "longitude",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            result_vars_into_list,
            verbose_name=verbose_name,
        )
        return handled_info

    def google_id_handler(self, data):
        verbose_name = 'Google id'
        result_vars = [
            "google_profile_uid",
            "avatar_url",
            "avatar_fileid",
            "fullname",
            "google_album_archive_profile_url",
            "google_maps_profile_url",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            verbose_name=verbose_name,
        )
        return handled_info

    def thatsthem_handler(self, data):
        verbose_name = 'Thatsthem'
        result_vars = [
            "fullname",
            "gender",
            "birthday",
            "address",
            "longitude",
            "latitude",
            "zip_code",
            "state",
            "city",
            "street",
            "relationship_status",
            "facebook",
            "linkedin",
            "url",
            "ip",
            "phone",
            "phone_part",
            "email",
            "email_part",
        ]
        result_vars_into_list = [
            "facebook_profile_uid", "facebook_profile_url", "username", "fullname", "avatar_url",
            "avatar_fileid",
            "linkedin_profile_url",
            "linkedin_profile_uid",
            "username",
            "fullname",
            "avatar_url",
            "avatar_fileid",
            "linkedin_company_url",
            "linkedin_company_uid",
            "company_name",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            result_vars_into_list,
            verbose_name=verbose_name,
        )
        return handled_info

    def advancedbackgroundchecks_handler(self, data):
        verbose_name = 'Advanced Background Checks'
        result_vars = [
            "fullname",
            "age",
            "city",
            "state",
            "phone",
            "phone_part",
            "addresses",
            "relatives",
        ]
        result_vars_into_list = [
            "address",
            "latitude",
            "longitude",
            "fullname",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            result_vars_into_list,
            verbose_name=verbose_name,
        )
        return handled_info

    def syncme_handler(self, data):
        verbose_name = 'Syncme'
        result_vars = [
            "fullname",
            "age",
            "phone",
            "twitter_profile_uid",
            "twitter_profile_url",
            "googleplus_profile_uid",
            "googleplus_profile_url",
            "linkedin_profile_uid",
            "linkedin_profile_url",
            "work",
            "school",
            "address",
        ]
        result_vars_into_list = [
            "company_name",
            "occupation",
            "year_from",
            "year_to",
            "school_name",
            "year_from",
            "year_to",
            "address",
            "latitude",
            "longitude",
        ]

        handled_info = self.handler(
            data,
            result_vars,
            result_vars_into_list,
            verbose_name=verbose_name,
        )
        return handled_info


def get_files(file_ids):
    images_data = ""
    if isinstance(file_ids, str):
        file_ids = [file_ids]

    for file_id in file_ids:
        url = f"https://api.lighthouse.lampyre.io/api/1.0/files/{file_id}"

        resp = requests.get(url, params={"token": "a05b0f96-008d-4e81-b5ea-b0792c764a1d"})

        image_data = "data:image;base64," + base64.b64encode(resp.content).decode()
        images_data += f'<img width="150" src="{image_data}" alt="Фото">'
    return images_data


if __name__ == "__main__":
    # +79506779955 - рос
    # +18004699269 - амер
    # +420604199473 чешский
    test_obj = Lampyre()
    k = test_obj.main("+79506779955")
    print("[RESULT]", k)
    # print(get_files("882e5e711eddf3ad9b693fa94f87c409"))

# phone_telegram_v1 {'firstname': 'Алексей', 'username': 'a79506779955', 'telegram_profile_uid': '234343072', 'avatar_fileid': ['882e5e711eddf3ad9b693fa94f87c409']}
# phone_telegram_v1 {'firstname': 'Dmitry', 'lastname': 'Ovchinnikov', 'lastseen': 1687420917, 'telegram_profile_uid': '349330686', 'avatar_fileid': ['39c7adae05abf5989af040b311977092']}
