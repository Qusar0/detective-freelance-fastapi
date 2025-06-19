import requests
import json
import base64

from datetime import datetime

from server.api.conf.config import settings


account_search_methods = [
    "email_haveibeenpwned_v1",
    "email_leakcheck_v1",
    "email_skype_v1",
    "email_yandex_search_v1",
    "email_linkedin_v1",
    "email_icq_v1",
    "email_foursquare_v1",
    "email_tumblr_v1",
    "email_flickr_v1",
    "email_github_v1",
    "email_duolingo_v1",
    "email_deezer_v1",
    "email_bitbucket_v1",
    "email_aboutme_v1",
    "email_yandex_services_v1",
    "email_mailru_avatar_v1",
    "email_thatsthem_v1",
    "email_advancedbackgroundchecks_v1",
    "email_searchcode_v1",
    "email_whoxy_v1",
    "email_openpeoplesearch_v1",
    "email_aihitdata_v1",
    "email_findpenguins_v1",
    "email_tapatalk_v1",
    "email_yandex_check_v1",
    "email_askfm_v1",
    "email_fb_restore_v1",
    "email_iforgot_apple_v1",
    "email_notion_v1",
    "email_trello_v1"
]

fitness_methods = [
    "email_runkeeper_v1",
    "email_nikeplus_v1",
    "email_sporttracks_v1",
    "email_adidas_v1",
    "email_fitbit_v1",
    "email_myfitnesspal_v1",
    "email_mapmyfitness_v1",
    "email_garminconnect_v1",
    "email_pulsstory_v1",
]

account_check_methods = [
    "email_instagram_restore_v1",
    "email_samsung_v1",
    "email_aeroflot_v1",
    "email_blablacar_checker_v1",
    "email_aliexpress_checker_v1",
    "email_github_checker_v1",
    "email_7cups_checker_v1",
    "email_amazon_checker_v1",
    "email_lastfm_checker_v1",
    "email_evernote_checker_v1",
    "email_vrbo_checker_v1",
    "email_pornhub_checker_v1",
    "email_eventbrite_checker_v1",
    "email_adobe_checker_v1",
    "email_microsoft_checker_v1",
    "email_codecademy_checker_v1",
    "email_freelancer_checker_v1",
    "email_lastpass_checker_v1",
    "email_xing_checker_v1",
    "email_wattpad_checker_v1",
    "email_seoclerks_checker_v1",
    "email_smule_checker_v1",
    "email_replit_checker_v1",
    "email_quora_checker_v1",
    "email_protonmail_v1",
    "email_sporcle_checker_v1",
    "email_spotify_checker_v1",
    "email_xvideos_checker_v1",
    "email_firefox_checker_v1",
    "email_anydo_checker_v1",
    "email_archiveorg_checker_v1",
    "email_wordpress_com_checker_v1",
    "email_snapchat_bitmoji_checker_v1",
    "email_rambler_restore_v1",
    "email_twitter_checker_v1",
    "email_ivi_checker_v1",
    "email_airbnb_checker_v1"

]

test_account_search_methods = ["email_github_v1"]

test_fitness_methods = ["email_fitbit_v1"]

test_account_check_methods = ["email_twitter_checker_v1"]


class LampyreMail:
    def __init__(self):
        self.token = settings.utils_token
        self.lampyre_handler = LampyreResultsHandler()
        self.tasks = []
        self.no_results_html = ""

    def main(self, email, methods_name):
        methods = self.define_methods_type(methods_name)

        for method in methods:
            task_info = self.start_task(method, email)
            if task_info is None:
                continue
            task_name = task_info[0]
            task_id = task_info[1]
            self.tasks.append({"task_name": task_name, "task_id": task_id, "iterated_times": 0})

        task_results = self.iterate_tasks()
        lampyre_html = ''
        for task in task_results:
            task_name = task['task_name']
            task_result = task['result']

            handled_result = self.lampyre_handler.distribute_task(task_name, task_result)
            print(handled_result)
            lampyre_html += self.form_lampyre_html(handled_result)
        lampyre_html += self.no_results_html
        print(lampyre_html)
        return lampyre_html

    def start_task(self, task_name: str, email: str):
        response = requests.post(
            url=f"https://api.lighthouse.lampyre.io/api/1.0/tasks/{task_name}",
            json={
                "token": self.token,
                "task_info": {
                    "email": email
                }
            }
        )
        if response.status_code == 404:
            return
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
                        output = {"task_name": task_name, "result": task_result['result']['result'][0]['output'][0]}
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
                    print("ERROR", task_result)

                task_iterated_times += 1
        return results

    @staticmethod
    def define_methods_type(methods_name: list[str]):
        methods = []

        if "acc search" in methods_name:
            methods.extend(account_search_methods)
        if "fitness tracker" in methods_name:
            methods.extend(fitness_methods)
        if "acc checker" in methods_name:
            methods.extend(account_check_methods)

        return methods

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
                result_str += f'<span class="account-dont-exist">Аккаунт не зарегистрирован</span>' + '<br>'
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
                        result_str += f'<tr> <td class="td-key">Аккаунт</td> <td class="account-exist">зарегистрирован</td></tr>'
                    else:
                        result_str += f'<tr> <td class="td-key">Аккаунт</td> <td class="account-dont-exist">зарегистрирован</td></tr>'
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
    def distribute_task(self, task_name, task_result):
        res = None
        if task_name in account_check_methods:
            res = self.checker_handler(task_result, task_name)
            return res

        match task_name:
            case "email_reputation_v1":
                res = self.reputation_handler(task_result)
            case "email_haveibeenpwned_v1":
                res = self.haveibeenpwned_handler(task_result)
            case "email_leakcheck_v1":
                res = self.leakcheck_handler(task_result)
            case "email_skype_v1":
                res = self.skype_handler(task_result)
            case "email_yandex_search_v1":
                res = self.yandex_search_handler(task_result)
            case "email_linkedin_v1":
                res = self.linkedin_handler(task_result)
            case "email_icq_v1":
                res = self.icq_handler(task_result)
            case "email_foursquare_v1":
                res = self.foursquare_handler(task_result)
            case "email_tumblr_v1":
                res = self.tumblr_handler(task_result)
            case "email_flickr_v1":
                res = self.flickr_handler(task_result)
            case "email_github_v1":
                res = self.github_handler(task_result)
            case "email_duolingo_v1":
                res = self.duolingo_handler(task_result)
            case "email_deezer_v1":
                res = self.deezer_handler(task_result)
            case "email_bitbucket_v1":
                res = self.bitbucket_handler(task_result)
            case "email_aboutme_v1":
                res = self.aboutme_handler(task_result)
            case "email_google_contacts_api_v1":
                res = self.google_contacts_api_handler(task_result)
            case "email_pinterest_v1":
                res = self.pinterest_handler(task_result)
            case "email_yandex_services_v1":
                res = self.yandex_services_handler(task_result)
            case "email_mailru_avatar_v1":
                res = self.mailru_avatar_handler(task_result)
            case "email_thatsthem_v1":
                res = self.thatsthem_handler(task_result)
            case "email_advancedbackgroundchecks_v1":
                res = self.advancedbackgroundchecks_handler(task_result)
            case "email_searchcode_v1":
                res = self.searchcode_handler(task_result)
            case "email_whoxy_v1":
                res = self.whoxy_handler(task_result)
            case "email_openpeoplesearch_v1":
                res = self.openpeoplesearch_handler(task_result)
            case "email_aihitdata_v1":
                res = self.aihitdata_handler(task_result)
            case "email_findpenguins_v1":
                res = self.findpenguins_handler(task_result)
            case "email_tapatalk_v1":
                res = self.tapatalk_handler(task_result)
            case "email_yandex_check_v1":
                res = self.yandex_check_handler(task_result)
            case "email_askfm_v1":
                res = self.askfm_handler(task_result)
            case "email_fb_restore_v1":
                res = self.fb_restore_handler(task_result)
            case "email_iforgot_apple_v1":
                res = self.iforgot_apple_handler(task_result)
            case "email_runkeeper_v1":
                res = self.runkeeper_handle(task_result)
            case "email_nikeplus_v1":
                res = self.nikeplus_handler(task_result)
            case "email_sporttracks_v1":
                res = self.sporttracks_hander(task_result)
            case "email_adidas_v1":
                res = self.adidas_handler(task_result)
            case "email_fitbit_v1":
                res = self.fitbit_handler(task_result)
            case "email_myfitnesspal_v1":
                res = self.myfitnesspal_hanler(task_result)
            case "email_mapmyfitness_v1":
                res = self.mapmyfitness_hanler(task_result)
            case "email_garminconnect_v1":
                res = self.garminconnect_hadler(task_result)
            case "email_pulsstory_v1":
                res = self.pulsstory_handle(task_result)
        return res

    @staticmethod
    def handler(data, result_vars, result_vars_into_list=None, verbose_name=None):
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

        if result == {}:
            result['результат'] = 'результат отсутствует'
        result['verbose_name'] = verbose_name
        return result

    def reputation_handler(self, data):
        verbose_name = 'Reputation'
        result_vars = ["is_suspicious", "references", "reputation", "first_seen", "lastseen", "list_of_services"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def haveibeenpwned_handler(self, data):
        verbose_name = 'HaveIBeenpwned'
        result_vars = ["title", "created"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def leakcheck_handler(self, data):
        verbose_name = 'Leakcheck'
        result_vars = ['password', 'last_modified_date', 'domain']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def skype_handler(self, data):
        verbose_name = 'Skype'
        result_vars = ["skype_profile_uid", "skype_profile_deep_link", "skype_contact_type", "avatar_url",
                       "avatar_fileid", "latitude", "longitude", "location", "fullname"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def yandex_search_handler(self, data):
        verbose_name = 'Яндекс'
        result_vars = ["url", "title", "description", "found_emails"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def linkedin_handler(self, data):
        verbose_name = "Linkedin"
        result_vars = ["firstname", "lastname", "linkedin_profile_uid", "avatar_fileid", "avatar_url", "fullname",
                       "occupation",
                       "linkedin_profile_url", "email"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def icq_handler(self, data):
        verbose_name = 'Icq'
        result_vars = ['icq_profile_uid', 'icq_profile_url', 'avatar_url', 'avatar_fileid', 'username', 'fullname',
                       'lastname', 'firstname', 'latitude', 'longitude', 'location', 'birthday']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def foursquare_handler(self, data):
        verbose_name = 'Foursquare'
        result_vars = ['foursquare_profile_uid', 'foursquare_profile_url', 'avatar_url', 'avatar_fileid', 'city',
                       'longitude', 'latitude', 'firstname', 'lastname', 'fullname', 'gender', 'bio', 'twitter',
                       'instagram', 'facebook']
        result_vars_into_list = ["twitter_profile_url", "twitter_profile_uid", "instagram_profile_url",
                                 "instagram_profile_uid", "facebook_profile_uid", "facebook_profile_url"]

        handled_info = self.handler(data, result_vars, result_vars_into_list, verbose_name=verbose_name)
        return handled_info

    def tumblr_handler(self, data):
        verbose_name = 'Tumblr'
        result_vars = ['username', 'tumblr_profile_url', 'avatar_url', 'avatar_fileid']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def flickr_handler(self, data):
        verbose_name = 'Flickr'
        result_vars = ['flickr_profile_url', 'flickr_profile_uid', 'posts_count', 'following_count', 'followers_count',
                       'location', 'latitude', 'longitude', 'bio', 'avatar_url', 'avatar_fileid', 'occupation',
                       'facebook_profile_url', 'twitter_profile_url', 'instagram_profile_url', 'pinterest_profile_url',
                       'tumblr_profile_url', 'url', 'fullname']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def github_handler(self, data):
        verbose_name = 'Github'
        result_vars = ['company_name', 'location', 'latitude', 'longitude', 'username', 'github_profile_url', 'bio',
                       'url', 'fullname', 'avatar_url', 'avatar_fileid', 'organizations']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def duolingo_handler(self, data):
        verbose_name = 'Duolingo'
        result_vars = ['duolingo_profile_uid', 'fullname', 'username', 'learning_language', 'url', 'avatar_url',
                       'avatar_fileid']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def deezer_handler(self, data):
        verbose_name = 'Deezer'
        result_vars = ['deezer_profile_uid', 'deezer_profile_url', 'screen_name', 'birthday', 'country_code', 'gender',
                       'avatar_url', 'avatar_fileid']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def bitbucket_handler(self, data):
        verbose_name = 'Bitbucket'
        result_vars = ['username', 'created', 'url', 'fullname', 'avatar_url', 'avatar_fileid', 'is_bitbucket_team',
                       'bitbucket_profile_url']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def aboutme_handler(self, data):
        verbose_name = "Aboutme"
        result_vars = ['aboutme_profile_uid', 'aboutme_profile_url', 'username', 'firstname', 'lastname',
                       'paid_account', 'fullname', 'avatar_url', 'avatar_fileid', 'occupation', 'employment',
                       'education', 'feedback', 'location', 'latitude', 'longitude', 'text', 'interests', 'tag', 'url',
                       'twitter', 'instagram', 'facebook', 'linkedin']
        result_vars_into_list = ['twitter_profile_url', 'twitter_profile_uid', 'username', 'fullname', 'avatar_url',
                                 'avatar_fileid', 'instagram_profile_url', 'instagram_profile_uid',
                                 'facebook_profile_uid', 'facebook_profile_url', 'linkedin_profile_url',
                                 'linkedin_profile_uid', 'linkedin_company_url', 'linkedin_company_uid', 'company_name']
        handled_info = self.handler(data, result_vars, result_vars_into_list, verbose_name=verbose_name)
        return handled_info

    def google_contacts_api_handler(self, data):
        verbose_name = "Google Contacts"
        result_vars = ['google_profile_uid', 'avatar_url', 'avatar_fileid', 'fullname',
                       'google_album_archive_profile_url', 'google_maps_profile_url', 'google_calendar_profile_url']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def pinterest_handler(self, data):
        verbose_name = "Pinterest"
        result_vars = ['pinterest_profile_uid', 'pinterest_profile_url', 'username', 'firstname', 'lastname',
                       'fullname', 'gender', 'age', 'pins_count', 'boards_count', 'followers_count', 'following_count',
                       'views_count', 'location', 'latitude', 'longitude', 'created', 'avatar_url', 'avatar_fileid',
                       'is_verified', 'is_business_account', 'is_owner_website', 'url', 'text', 'boards']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def yandex_services_handler(self, data):
        verbose_name = 'Yandex сервисы'
        result_vars = ['yandex_profile_uid', 'fullname', 'username', 'gender', 'avatar_url', 'avatar_fileid',
                       'yandex_music_url', 'yandex_profile_digital_uid', 'vk', 'url']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def mailru_avatar_handler(self, data):
        verbose_name = "Mailru avatar"
        result_vars = ["avatar_fileid"]
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def thatsthem_handler(self, data):
        verbose_name = "Thatsthem"
        result_vars = ['fullname', 'gender', 'birthday', 'address', 'longitude', 'latitude', 'zip_code', 'state',
                       'city', 'street', 'relationship_status', 'facebook', 'linkedin', 'url', 'ip', 'phone',
                       'phone_part', 'email', 'email_part']
        result_vars_into_list = ['facebook_profile_uid', 'facebook_profile_url', 'username', 'fullname', 'avatar_url',
                                 'avatar_fileid', 'linkedin_profile_url', 'linkedin_profile_uid',
                                 'linkedin_company_url', 'linkedin_company_uid', 'company_name']

        handled_info = self.handler(data, result_vars, result_vars_into_list, verbose_name=verbose_name)
        return handled_info

    def advancedbackgroundchecks_handler(self, data):
        verbose_name = "Advancedbackgroundchecks"
        result_vars = ['fullname', 'age', 'city', 'state', 'phone', 'phone_part', 'addresses', 'relatives']
        result_vars_into_list = ["address", "latitude", "longitude", "fullname"]

        handled_info = self.handler(data, result_vars, result_vars_into_list, verbose_name=verbose_name)
        return handled_info

    def searchcode_handler(self, data):
        verbose_name = "Searchcode"
        result_vars = ['count', 'url', 'language', 'file_name', 'file_path', 'text']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def whoxy_handler(self, data):
        verbose_name = "Whoxy"
        result_vars = ['domain', 'registrar', 'created', 'updated', 'expires']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def openpeoplesearch_handler(self, data):
        verbose_name = 'Openpeoplesearch'
        result_vars = ['firstname', 'middlename', 'lastname', 'address', 'city', 'state', 'street', 'zip_code', 'phone',
                       'phone_part', 'email', 'email_part', 'birthday_string', 'domain', 'occupation', 'employer',
                       'phone_line_type', 'latitude', 'longitude']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def aihitdata_handler(self, data):
        verbose_name = "aihitdata"
        result_vars = ['description', 'company_name', 'domain', 'person', 'email', 'address', 'phone', 'fax',
                       'email_part', 'phone_part']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def findpenguins_handler(self, data):
        verbose_name = "Findpenguins"
        result_vars = ['findpenguins_profile_uid', 'findpenguins_profile_url', 'username', 'fullname', 'bio',
                       'is_verified', 'url', 'created', 'location', 'latitude', 'longitude', 'avatar_url',
                       'avatar_fileid', 'stats']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def tapatalk_handler(self, data):
        verbose_name = "Tapatalk"
        result_vars = ["avatar_fileid", "username"]
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def yandex_check_handler(self, data):
        verbose_name = "Yandex"
        result_vars = ["exist"]
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def allegro_handler(self, data):
        verbose_name = []
        result_vars = []
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def askfm_handler(self, data):
        verbose_name = "Askfm"
        result_vars = ['avatar_url', 'address', 'bio', 'posts_count', 'likes_count', 'interests', 'url', 'is_disabled',
                       'username', 'askfm_profile_url', 'avatar_fileid', 'lastname', 'longitude', 'latitude',
                       'firstname', 'fullname']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def fb_restore_handler(self, data):
        verbose_name = "Facebook"
        result_vars = ['email_part', 'phone_part', 'fullname', 'avatar_url', 'avatar_fileid', 'exists']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def iforgot_apple_handler(self, data):
        verbose_name = "Iforgot apple"
        result_vars = ['exists', 'email_part', 'phone_part']
        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def runkeeper_handle(self, data):
        verbose_name = "Runkeeper"
        result_vars = ['exists', 'runkeeper_profile_url', 'runkeeper_profile_uid', 'fullname', 'username', 'location',
                       'latitude', 'longitude', 'facebook_profile_url', 'facebook_profile_uid', 'avatar_url',
                       'avatar_fileid', 'runkeeper_activity_uid']
        result_vars_into_list = ['runkeeper_activity_uid', 'created', 'points', 'latitude', 'longitude', 'created']

        handled_info = self.handler(data, result_vars, result_vars_into_list, verbose_name=verbose_name)
        return handled_info

    def nikeplus_handler(self, data):
        verbose_name = "Nikeplus"
        result_vars = ['username', 'firstname', 'lastname', 'avatar_url', 'avatar_fileid', 'nike_plus_profile_uid',
                       'nike_plus_profile_url']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def sporttracks_hander(self, data):
        verbose_name = "Sporttrack"
        result_vars = ['email', 'photo_fileid', 'country_code', 'sporttracks_profile_url', 'sporttracks_profile_uid',
                       'fullname', 'latitude', 'longitude']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def adidas_handler(self, data):
        verbose_name = "Adidas"
        result_vars = ['email', 'adidas_running_profile_uid', 'adidas_running_profile_url', 'created', 'avatar_url',
                       'avatar_fileid', 'fullname', 'exists']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def fitbit_handler(self, data):
        verbose_name = "Fitbit"
        result_vars = ['email', 'fitbit_profile_url', 'fitbit_profile_uid', 'photo_fileid', 'fullname']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def myfitnesspal_hanler(self, data):
        verbose_name = "Myfitnesspal"
        result_vars = ['username', 'myfitnesspal_profile_uid', 'myfitnesspal_profile_url', 'gender', 'age', 'city',
                       'latitude', 'longitude', 'bio', 'is_closed_profile', 'status', 'interests', 'motivation',
                       'created', 'avatar_url', 'avatar_fileid', 'photos_count', 'friends_count', 'postal_code',
                       'birthday']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def mapmyfitness_hanler(self, data):
        verbose_name = "mapmyfitness"
        result_vars = ['avatar_url', 'avatar_fileid', 'exists', 'username', 'fullname', 'lastname', 'firstname',
                       'latitude', 'longitude', 'location', 'mapmyfitness_profile_id', 'mapmyfitness_profile_url']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def garminconnect_hadler(self, data):
        verbose_name = "Garminconnect"
        result_vars = ['email', 'exists', 'fullname', 'garmin_connect_profile_url', 'garmin_connect_profile_uid',
                       'username', 'url', 'location', 'longitude', 'latitude', 'avatar_url', 'avatar_fileid',
                       'facebook_profile_url', 'facebook_profile_uid', 'twitter_profile_url', 'twitter_profile_uid',
                       'bio']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def pulsstory_handle(self, data):
        verbose_name = "Pulsstory"
        result_vars = ['avatar_url', 'avatar_fileid', 'birthday', 'username', 'fullname', 'lastname', 'firstname',
                       'pulsstory_profile_id']

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info

    def checker_handler(self, data, checker_name: str):
        verbose_name = checker_name.replace("_checker_v1", "").replace("email_", "").capitalize()
        result_vars = ["exists", "is_disabled", "created"]

        handled_info = self.handler(data, result_vars, verbose_name=verbose_name)
        return handled_info


def get_files(file_ids):
    images_data = ""
    if isinstance(file_ids, str):
        file_ids = [file_ids]

    for file_id in file_ids:
        url = f"https://api.lighthouse.lampyre.io/api/1.0/files/{file_id}"

        resp = requests.get(url, params={"token": settings.utils_token})

        image_data = "data:image;base64," + base64.b64encode(resp.content).decode()
        images_data += f'<img width="150" src="{image_data}" alt="Фото">'
    return images_data


if __name__ == "__main__":
    test_obj = LampyreMail()
    methods = ["acc search", "acc checker"]
    email = 'darhanuva@gmail.com'
    k = test_obj.main(methods, email)
    print("[RESULT]", k)
