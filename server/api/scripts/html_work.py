from server.api.templates.html_styles import FIO_STYLE, NUM_STYLE, COMPANY_STYLE, TG_STYLE
from server.api.templates.js_scripts import HIGHCHARTS


def response_template(titles, items, filters, fullname_counters, extra_titles="") -> str:
    report_html = f"""<!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titles[0]}</title>
            {FIO_STYLE}
        </head>

        <body>
            <div class="tab-head" onclick="closeModal(event)">
                <div id="head-info" style="margin-bottom: 6px;transition: .15s;overflow:hidden;width: 100%;height:105px">
            <h2 style="display: inline;cursor:pointer;" class="object-full_name" onclick="$('#head-info').style.height = ($('#head-info').style.height == '105px' ? '28px' : '105px');$('#head-info h2 svg').style.transform = ($('#head-info').style.height == '105px' ? 'rotateX(180deg)' : 'rotateX(0deg)')">Объект: <span style="white-space:nowrap; text-transform: capitalize;">{titles[0]}</span>
                <svg xmlns="http://www.w3.org/2000/svg" style="width:15px;margin-bottom: -2px;transition: .15s;transform:rotateX(180deg);" viewBox="0 0 448 512"><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>
                    </h2>
                <div class="flex justify-center" style="flex-direction:column;width: 100%;">
                    <span class="max-text-length" title="Категории поиска: {titles[1]}"><b>Категории поиска:</b>{titles[1]}</span>
                    <span class="max-text-length" title="Произвольные ключевые слова: {titles[2]}"><b>Произвольные ключевые слова: </b> {titles[2]}</span>
                    <span class="max-text-length" title="Минус-слова: {titles[3]}"><b>Минус-слова:</b> {titles[3]}</span>
                    <span class="max-text-length" title="Плюс-слова: {titles[4]}"><b>Плюс-слова:</b> {titles[4]}</span>
                    {extra_titles}
                </div>

                </div>

                <div class=" tabs flex flex-wrap items-center">
                    <div class="tab-1 selected" onclick="select_tab(1)">
                        Главное
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-2" onclick="select_tab(2)">
                        Произвольные
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-3" onclick="select_tab(3)">
                        Негатив
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-4" onclick="select_tab(4)">
                        Репутация
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-5" onclick="select_tab(5)">
                        Связи
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-6" onclick="select_tab(6)">
                        Соц.сети
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-7" onclick="select_tab(7)">Документы
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-8" onclick="select_tab(8)">Все материалы
                        <span class="tab-count">0</span>
                    </div>
                </div>
            </div>

            <script>{HIGHCHARTS}</script>

            <div style="display: flex;gap: 15px;padding: 15px 15px 0;flex-wrap: wrap;justify-content: center;">
            <div id="container" style="min-width: 424px; height: 230px; border-radius: 6px; overflow: hidden;"></div>
            <div class="socials" id="socials" style="display:none">
                <div class="socials_type-info" data-social-name="Вконтакте">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected vk">
                        <path
                            d="M31.4907 63.4907C0 94.9813 0 145.671 0 247.04V264.96C0 366.329 0 417.019 31.4907 448.509C62.9813 480 113.671 480 215.04 480H232.96C334.329 480 385.019 480 416.509 448.509C448 417.019 448 366.329 448 264.96V247.04C448 145.671 448 94.9813 416.509 63.4907C385.019 32 334.329 32 232.96 32H215.04C113.671 32 62.9813 32 31.4907 63.4907ZM75.6 168.267H126.747C128.427 253.76 166.133 289.973 196 297.44V168.267H244.16V242C273.653 238.827 304.64 205.227 315.093 168.267H363.253C359.313 187.435 351.46 205.583 340.186 221.579C328.913 237.574 314.461 251.071 297.733 261.227C316.41 270.499 332.907 283.63 346.132 299.751C359.357 315.873 369.01 334.618 374.453 354.747H321.44C316.555 337.262 306.614 321.61 292.865 309.754C279.117 297.899 262.173 290.368 244.16 288.107V354.747H238.373C136.267 354.747 78.0267 284.747 75.6 168.267Z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Facebook">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected fb">
                        <path
                            d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h137.25V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.27c-30.81 0-40.42 19.12-40.42 38.73V256h68.78l-11 71.69h-57.78V480H400a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Instagram">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected insta">
                        <path
                            d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Telegram">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"
                        class="social_type selected tg">
                        <path d="M248,8C111.033,8,0,119.033,0,256S111.033,504,248,504,496,392.967,496,256,384.967,8,248,8ZM362.952,176.66c-3.732,39.215-19.881,134.378-28.1,178.3-3.476,18.584-10.322,24.816-16.948,25.425-14.4,1.326-25.338-9.517-39.287-18.661-21.827-14.308-34.158-23.215-55.346-37.177-24.485-16.135-8.612-25,5.342-39.5,3.652-3.793,67.107-61.51,68.335-66.746.153-.655.3-3.1-1.154-4.384s-3.59-.849-5.135-.5q-3.283.746-104.608,69.142-14.845,10.194-26.894,9.934c-8.855-.191-25.888-5.006-38.551-9.123-15.531-5.048-27.875-7.717-26.8-16.291q.84-6.7,18.45-13.7,108.446-47.248,144.628-62.3c68.872-28.647,83.183-33.623,92.511-33.789,2.052-.034,6.639.474,9.61,2.885a10.452,10.452,0,0,1,3.53,6.716A43.765,43.765,0,0,1,362.952,176.66Z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Одноклассники">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected ok">
                        <path
                            d="M184.2 177.1c0-22.1 17.9-40 39.8-40s39.8 17.9 39.8 40c0 22-17.9 39.8-39.8 39.8s-39.8-17.9-39.8-39.8zM448 80v352c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V80c0-26.5 21.5-48 48-48h352c26.5 0 48 21.5 48 48zm-305.1 97.1c0 44.6 36.4 80.9 81.1 80.9s81.1-36.2 81.1-80.9c0-44.8-36.4-81.1-81.1-81.1s-81.1 36.2-81.1 81.1zm174.5 90.7c-4.6-9.1-17.3-16.8-34.1-3.6 0 0-22.7 18-59.3 18s-59.3-18-59.3-18c-16.8-13.2-29.5-5.5-34.1 3.6-7.9 16.1 1.1 23.7 21.4 37 17.3 11.1 41.2 15.2 56.6 16.8l-12.9 12.9c-18.2 18-35.5 35.5-47.7 47.7-17.6 17.6 10.7 45.8 28.4 28.6l47.7-47.9c18.2 18.2 35.7 35.7 47.7 47.9 17.6 17.2 46-10.7 28.6-28.6l-47.7-47.7-13-12.9c15.5-1.6 39.1-5.9 56.2-16.8 20.4-13.3 29.3-21 21.5-37z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
            </div>
            <div class="documents" id="documents" style="display:none">
                <div class="doc_type-info" data-document-name="PDF" title="Формат - PDF">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
                        class="doc_type selected pdf">
                        <path d="M64 464H96v48H64c-35.3 0-64-28.7-64-64V64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V288H336V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16zM176 352h32c30.9 0 56 25.1 56 56s-25.1 56-56 56H192v32c0 8.8-7.2 16-16 16s-16-7.2-16-16V448 368c0-8.8 7.2-16 16-16zm32 80c13.3 0 24-10.7 24-24s-10.7-24-24-24H192v48h16zm96-80h32c26.5 0 48 21.5 48 48v64c0 26.5-21.5 48-48 48H304c-8.8 0-16-7.2-16-16V368c0-8.8 7.2-16 16-16zm32 128c8.8 0 16-7.2 16-16V400c0-8.8-7.2-16-16-16H320v96h16zm80-112c0-8.8 7.2-16 16-16h48c8.8 0 16 7.2 16 16s-7.2 16-16 16H448v32h32c8.8 0 16 7.2 16 16s-7.2 16-16 16H448v48c0 8.8-7.2 16-16 16s-16-7.2-16-16V432 368z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Word" title="Формат - Word">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected word">
                        <path d="M48 448V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm55 241.1c-3.8-12.7-17.2-19.9-29.9-16.1s-19.9 17.2-16.1 29.9l48 160c3 10.2 12.4 17.1 23 17.1s19.9-7 23-17.1l25-83.4 25 83.4c3 10.2 12.4 17.1 23 17.1s19.9-7 23-17.1l48-160c3.8-12.7-3.4-26.1-16.1-29.9s-26.1 3.4-29.9 16.1l-25 83.4-25-83.4c-3-10.2-12.4-17.1-23-17.1s-19.9 7-23 17.1l-25 83.4-25-83.4z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Excel" title="Формат - Excel">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected excel">
                        <path d="M48 448V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm90.9 233.3c-8.1-10.5-23.2-12.3-33.7-4.2s-12.3 23.2-4.2 33.7L161.6 320l-44.5 57.3c-8.1 10.5-6.3 25.5 4.2 33.7s25.5 6.3 33.7-4.2L192 359.1l37.1 47.6c8.1 10.5 23.2 12.3 33.7 4.2s12.3-23.2 4.2-33.7L222.4 320l44.5-57.3c8.1-10.5 6.3-25.5-4.2-33.7s-25.5-6.3-33.7 4.2L192 280.9l-37.1-47.6z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="PowerPoint" title="Формат - PowerPoint">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected pptx">
                        <path d="M64 464c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm72 208c-13.3 0-24 10.7-24 24V336v56c0 13.3 10.7 24 24 24s24-10.7 24-24V360h44c42 0 76-34 76-76s-34-76-76-76H136zm68 104H160V256h44c15.5 0 28 12.5 28 28s-12.5 28-28 28z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Txt" title="Формат - Txt">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected txt">
                        <path d="M64 464c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm56 256c-13.3 0-24 10.7-24 24s10.7 24 24 24H264c13.3 0 24-10.7 24-24s-10.7-24-24-24H120zm0 96c-13.3 0-24 10.7-24 24s10.7 24 24 24H264c13.3 0 24-10.7 24-24s-10.7-24-24-24H120z"/>
                    </svg>
                    <span>0</span>
                </div>
            </div>
            <div>
                <div
                    style="display: flex;align-items: center;height: 34px;font-size: 13.5px;background: white;padding: 0 10px;border-radius: 5px;white-space:nowrap">
                    <div style="font-size: 16px;margin-right: 10px;">Совпадения: </div>
                    <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                            onchange="update_fullname_filter(event)" checked value="0"> все данные <span
                            id="fullname-0">48</span> </label>
                    <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                            onchange="update_fullname_filter(event)" value="1"> полное совпадение <span
                            id="fullname-1">32</span> </label>
                    <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                            onchange="update_fullname_filter(event)" value="2"> частичное совпадение <span
                            id="fullname-2">16</span></label>
                </div>
                <label class="parent-prompt-hover" style="display: inline-flex;align-items: center;margin: 6px 0;background: white;border-radius: 4px;height: 32px;padding: 0 11px 3px 9px;cursor: pointer;user-select: none;"> 
                    <input id="minus-social-resources" type="checkbox" onchange="render_items(false, true)" style="margin: 2px 5px 0px 0;cursor: pointer;"> 
                    <small class="prompt">Исключает из справки сервисы поиска аккаунтов в соц. сетях: socialbase.ru, bigbookname.com и другие.</small> 
                    <span style="font-size: 15px;">Скрыть архивы социальных сетей</span> 
                </label>
                <!-- -->
                <div style="
                    display: flex;
                    align-items: center;
                ">
                    <div style="font-weight: 600;margin-top: 4px;margin-right: 6px;letter-spacing: .75px;">Стоп-фильтр: </div>
                    <div class="minus-keywords-block" style="
                    margin-top: 5px;
                    display: flex;
                    align-items: center;
                    width: 350px;height: 30px;">
                        <div style="
                    position: relative;
                    height: 30px;
                    width: 100%;
                    display: flex;
                " class="parent-prompt">
                            <input type="text" onkeydown="event.keyCode == 13 ? add_minus_keyword() : ''"
                                style="height: 30px;outline: none;border: none;padding: 0 10px;font-size: 14.5px;width: 100%;border-radius: 3px 0 0 3px;"
                                placeholder="Минус-слова" id="minus-keyword">
                            <small class="prompt">Добавьте стоп-слова для исключения содержащих их материалов. Пример: для исключения всех материалов, содержащих слова "адвокат", "адвокатский", "адвоката", достаточно добавить одно стоп-слово "адвокат".</small>
                            <svg xmlns="http://www.w3.org/2000/svg"
                                onclick="this.nextElementSibling.classList.toggle('hide-keywords-modal')" viewBox="0 0 448 512" style="
                    background: white;
                    width: 20px;
                    fill: #676666;
                    padding-right: 6px;
                    cursor: pointer;
                ">
                                <path
                                    d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z">
                                </path>
                            </svg>


                            <div class="minus-keywords-modal scrollbar hide-keywords-modal">
                                <div class="minus-keyword" onclick="remove_minus_keyword(this)">
                                    <span>Список пустой</span>
                                </div>
                            </div>
                        </div>

                        <button style="
                    padding: 0 8px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    border: none;
                    background: rgb(26, 179, 148);
                    color: white;
                    border-radius: 0 3px 3px 0;
                    cursor: pointer;
                " onclick="add_minus_keyword()">Добавить</button>
                    </div>
                </div>
                <!-- -->
            </div>
        </div>

        <div class="flex items-center wrap-reverse-container" style="padding: 0 10px;">
            <div class="similars-range" style="padding-left: 20px;">
                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="position:absolute;left:5px;top:4px;"
                    viewBox="0 0 512 512">
                    <path
                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                </svg>
                <div slider id="slider-distance">
                    <div>
                        <div inverse-left style="width:100%;"></div>
                        <div inverse-right style="width:100%;"></div>
                        <div range style="left:0%;right:0%;"></div>
                        <span thumb style="left:0%;"></span>
                        <span thumb style="left:100%;"></span>
                        <div sign style="left:0%;">
                            <span id="value">0</span>
                        </div>
                        <div sign style="left:100%;">
                            <span id="value">100</span>
                        </div>
                    </div>
                    <input id="startRangeValue" type="range" tabindex="0" value="0" max="100" min="0" step="1"
                        onchange="update_startRangeValue(+event.target.value)" oninput="startRange(event)" />

                    <input id="endRangeValue" type="range" tabindex="0" value="100" max="100" min="0" step="1"
                        onchange="update_endRangeValue(+event.target.value)" oninput="endRange(event)" />
                </div>
            </div>
            <div class="filter-search-arbitrary" style="display: none;">
                <label class="input">
                    <!-- Введите название произвольного ключа -->
                    <input type="text" placeholder="Введите название ключа" onclick="showListModal(event)"
                        oninput="updateList(event)" />
                    <svg onclick="toggleListModal(event)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" id="arbitrary-angle-id">
                        <path
                            d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
                    </svg>
                    <div class="arbitrary-keys" onclick="showListModal(event)">
                    </div>
                </label>
            </div>
            <div class="pagination-container" onclick="closeModal(event)">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <div class="content" onclick="closeModal(event)">
            <div class="tab-content-1 selected">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-2">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-3">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-4">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-5">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-6">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-7">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-8">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
        </div>

        <div class="flex" onclick="closeModal(event)">
            <div class="pagination-container" style="padding: 0 7.5px 15px;">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <script>

            let minus_keywords = [];

            function remove_minus_keyword(element) {{
                let keyword_name = element.previousElementSibling.textContent.trim()
                let keyword_index = minus_keywords.indexOf(keyword_name);
                if (keyword_index != -1) {{
                    delete minus_keywords[keyword_index];
                    document.querySelector('#minus-keyword').value = '';
                    add_minus_keyword()
                }}
            }}

            function add_minus_keyword() {{
                let keyword_name = document.querySelector('#minus-keyword')?.value ?? '';
                keyword_name = keyword_name.trim().toLowerCase()
                if (!minus_keywords.includes(keyword_name) && keyword_name != '') {{
                    minus_keywords.push(keyword_name);
                }}
                render_items(false, true)

                let minus_keywords_modal = '';

                minus_keywords.forEach(keyword => {{
                    minus_keywords_modal += `
                        <div class="minus-keyword">
                            <span title="${{keyword}}">${{keyword}}</span>
                            <svg onclick="remove_minus_keyword(this)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"></path></svg>
                        </div>
                    `
                }})

                document.querySelector('.minus-keywords-modal').innerHTML = minus_keywords_modal

                console.log('minus_keywords', minus_keywords);


                document.querySelector('.minus-keywords-modal').classList.remove('hide-keywords-modal');

                document.querySelector('#minus-keyword').value = '';
                document.querySelector('#minus-keyword').focus();
                update_global_counts()
            }}

            let startRangeValue = 0;
            let endRangeValue = 0;

            function update_startRangeValue(value) {{
                startRangeValue = value;
                render_items()
            }}
            function update_endRangeValue(value) {{
                endRangeValue = value;
                render_items()
            }}

            const startRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.min($this.value, $this.parentNode.childNodes[5].value - 1);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[1].style.width = value + '%';
                children[5].style.left = value + '%';
                children[7].style.left = value + '%'; children[11].style.left = value + '%';
                children[11].childNodes[1].innerHTML = $this.value;
            }}
            const endRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.max($this.value, $this.parentNode.childNodes[3].value);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[3].style.width = (100 - value) + '%';
                children[5].style.right = (100 - value) + '%';
                children[9].style.left = value + '%'; children[13].style.left = value + '%';
                children[13].childNodes[1].innerHTML = $this.value;
            }}

            const isMobile = Boolean(navigator.userAgent.match(/Android/i)
                || navigator.userAgent.match(/webOS/i)
                || navigator.userAgent.match(/iPhone/i)
                || navigator.userAgent.match(/iPad/i)
                || navigator.userAgent.match(/iPod/i)
                || navigator.userAgent.match(/BlackBerry/i)
                || navigator.userAgent.match(/Windows Phone/i));

            console.log('isMobile', isMobile, navigator.userAgent);

            let selected_tab_index = 1
            function $(str) {{
                let elements = document?.querySelectorAll(str);

                return (elements?.length == 1 || str[0] == '#') ? document?.querySelector(str) : elements;
            }}
            Object.prototype.html = function (html) {{
                this?.forEach(item => {{
                    item.innerHTML = html
                }});
            }}
            Object.prototype.hasClass = function (className) {{
                return this?.classList?.contains(className)
            }}
            Object.prototype.addClass = function (className) {{
                this?.classList?.add(className)
            }}
            Object.prototype.removeClass = function (className) {{
                this?.classList?.remove(className)
            }}

            let filterable_tabs = [2, 3, 4, 5, 6, 7, 8]
            const items = {{
                    main: [
                        {items.get("main")}
                    ],
                    arbitrary: [{items.get("free")}],
                    negative: [{items.get("negative")}],
                    reputation: [{items.get("reputation")}],
                    connections: [{items.get("relation")}],
                    socials: [{items.get("socials")}],
                    documents: [{items.get("documents")}],
                    all_materials: [{items.get("all")}],
                }}

            endRangeValue = []
            items.main.forEach(item => {{
                endRangeValue.push(+item.keyword_list.length)
            }});
            startRangeValue = endRangeValue.length ? Math.min(...endRangeValue) : 0
            endRangeValue = endRangeValue.length ? Math.max(...endRangeValue) : 0

            let endRangeElement = $('#endRangeValue');
            let startRangeElement = $('#startRangeValue');
            startRangeElement.min = endRangeElement.min = startRangeElement.value = startRangeValue;
            startRangeElement.max = endRangeElement.max = endRangeElement.value = endRangeValue;
            startRange({{ target: startRangeElement }})
            endRange({{ target: endRangeElement }})


            const tab_names = {{
                1: 'main',
                2: 'arbitrary',
                3: 'negative',
                4: 'reputation',
                5: 'connections',
                6: 'socials',
                7: 'documents',
                8: 'all_materials',
            }}

            function isFilterableTab() {{
                return filterable_tabs.find(filterable_tab => filterable_tab == selected_tab_index) != undefined
            }}
            function select_tab(new_tab_index) {{
                $('#socials').style.display = new_tab_index == 6 ? '' : 'none'
                $('#documents').style.display = new_tab_index == 7 ? '' : 'none'
                if (selected_tab_index == new_tab_index) return //  || items[tab_names[new_tab_index]]?.length == 0

                $('#container').style.display = new_tab_index == 1 ? '' : 'none'
                document.querySelector('.minus-keywords-block').parentElement.style.display = new_tab_index == 1 ? 'flex' : 'none';
                document.querySelector('#minus-social-resources').parentElement.style.display = new_tab_index == 1 ? 'inline-flex' : 'none';

                $(`.tab-${{new_tab_index}}`)?.addClass('selected')
                $(`.tab-content-${{new_tab_index}}`)?.addClass('selected')

                $(`.tab-${{selected_tab_index}}`)?.removeClass('selected')
                $(`.tab-content-${{selected_tab_index}}`)?.removeClass('selected')

                selected_tab_index = new_tab_index

                render_items(false, true)
                let tab_name = tab_names[selected_tab_index];

                if (isFilterableTab() && items[tab_names[selected_tab_index]]?.length > 0) {{

                    filter_counts[selected_tab_index] = {{}};
                    items[tab_names[selected_tab_index]].forEach(item => {{
                        item.keyword_list.forEach(keyword => {{
                            if (!filter_counts[selected_tab_index][keyword]) {{
                                filter_counts[selected_tab_index][keyword] = 0;
                            }}
                            filter_counts[selected_tab_index][keyword]++;
                        }});
                    }})
                    updateList({{ target: {{ value: '' }} }})
                    $(`.filter-search-arbitrary`).style.display = 'block';
                }}
                else {{
                    $(`.filter-search-arbitrary`).style.display = 'none';
                }}
                $(`.similars-range`).style.display = new_tab_index == 1 ? 'block' : 'none';

            }}
            function copy(that) {{
                var inp = document.createElement('input');
                document.body.appendChild(inp)
                inp.value = that.textContent
                inp.select();
                document.execCommand('copy', false);
                inp.remove();
            }}
            const tab_indexes = {{
                main: 1,
                arbitrary: 2,
                negative: 3,
                reputation: 4,
                connections: 5,
                socials: 6,
                documents: 7,
                all_materials: 8,
            }}

            const fullname_data = {{
                    main: {fullname_counters.get("main")},
                    arbitrary: {fullname_counters.get("arbitrary")},
                    negative: {fullname_counters.get("negative")},
                    reputation: {fullname_counters.get("reputation")},
                    connections: {fullname_counters.get("connections")},
                    socials: {fullname_counters.get("socials")},
                    documents: {fullname_counters.get("documents")},
                    all_materials: {fullname_counters.get("all_materials")},
                }}

            const fullname_filter = {{
                main: 0,
                arbitrary: 0,
                negative: 0,
                reputation: 0,
                connections: 0,
                socials: 0,
                documents: 0,
                all_materials: 0,
            }}


            Object.entries(tab_indexes).forEach(([tab_name, tab_index]) => {{
                $(`.tab-${{tab_index}} .tab-count`).innerHTML = items[tab_name]?.length
            }});
            const tab_pages = {{
                main: {{
                    count: 0,
                    page: 1,
                }},
                arbitrary: {{
                    count: 0,
                    page: 1,
                }},
                negative: {{
                    count: 0,
                    page: 1,
                }},
                reputation: {{
                    count: 0,
                    page: 1,
                }},
                connections: {{
                    count: 0,
                    page: 1,
                }},
                socials: {{
                    count: 0,
                    page: 1,
                }},
                documents: {{
                    count: 0,
                    page: 1,
                }},
                all_materials: {{
                    count: 0,
                    page: 1,
                }},
            }}

            function set_page(tab_name, page) {{
                tab_pages[tab_name].page = page;
                render_items()
                update_pagination()
            }}
            function minus_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page -= 1;
                render_items()
                update_pagination()
            }}
            function first_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page = 1;
                render_items()
                update_pagination()
            }}
            function plus_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page += 1;
                render_items()
                update_pagination()
            }}
            function last_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page = tab_pages[tab_name].count;
                render_items()
                update_pagination()
            }}

            const range = 20;

            let seriesData = [
                {{
                    name: 'Произвольные',
                    y: 0,
                }},
                {{
                    name: 'Негатив',
                    y: 0
                }},
                {{
                    name: 'Репутация',
                    y: 0
                }},
                {{
                    name: 'Связи',
                    y: 0
                }},
                {{
                    name: 'Соц.сети',
                    y: 0
                }},
                {{
                    name: 'Документы',
                    y: 0
                }}
            ]

            function update_global_counts() {{

                Object.keys(items).forEach(tab_name => {{
                    if (items[tab_name]?.length) {{
                        if (filterable_tabs.includes(tab_indexes[tab_name])) {{

                            let temp_items = [...items[tab_name]];

                            if (minus_keywords.length) {{
                                temp_items = temp_items.filter(item => !minus_keywords.some(minus_keyword => (item.title.toLowerCase().includes(minus_keyword) || item.link.toLowerCase().includes(minus_keyword) || item.content.toLowerCase().includes(minus_keyword))))
                            }}
                            tab_pages[tab_name].count = Math.ceil(temp_items?.length / range);

                            $(`.tab-${{tab_indexes[tab_name]}} .tab-count`).innerHTML = seriesData[tab_indexes[tab_name] - 2].y = temp_items?.length ?? 0;
                        }}
                    }}
                }});
            }}
            let page = 1;
            let onfocused = false;

            function showListModal(event) {{
                event.stopPropagation()
                if (event.pointerType == '') return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
            }}
            function toggleListModal(event, from_html = false) {{
                event.stopPropagation()

                if (from_html && !$('.arbitrary-keys').hasClass('show')) return;
                //if (['path', 'svg'].includes(event.target.tagName)) return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
                else {{
                    $('.arbitrary-keys').removeClass('show')
                    $('.filter-search-arbitrary .input').removeClass('selected')
                    onfocused = false;
                }}
            }}
            function closeModal(event) {{
                event?.stopPropagation()
                if (onfocused) {{
                    setTimeout(() => {{
                        $('.arbitrary-keys').removeClass('show')
                        $('.filter-search-arbitrary .input').removeClass('selected')
                        event?.target?.blur()
                    }}, 100);
                    onfocused = false;
                }}
            }}

            let filters = {{
                    2: {{ {filters.get("free_kwds")} }}, 
                    3: {{ {filters.get("neg_kwds")} }}, 
                    4: {{ {filters.get("rep_kwds")} }}, 
                    5: {{ {filters.get("rel_kwds")} }},
                    6: {{ {filters.get("soc_kwds")} }},
                    7: {{ {filters.get("doc_kwds")} }},
                    8: {{ {filters.get("free_kwds")} }},
                }}

            let social_types = {{
                'Вконтакте': true,
                'Facebook': true,
                'Одноклассники': true,
                'Instagram': true,
                'Telegram': true,
            }}
            let document_types = {{
                'PDF': true,
                'Word': true,
                'Excel': true,
                'PowerPoint': true,
                'Txt': true,
            }}

            let social_type_counts = {{
                'Вконтакте': 0,
                'Facebook': 0,
                'Одноклассники': 0,
                'Instagram': 0,
                'Telegram': 0,
            }}
            let document_type_counts = {{
                'PDF': 0,
                'Word': 0,
                'Excel': 0,
                'PowerPoint': 0,
                'Txt': 0,
            }}
            let filter_counts = {{
            }}

            console.log('items', items)

            function makeSafeForCSS(name) {{
                return name.replace(/[^a-z0-9]/g, function (s) {{
                    var c = s.charCodeAt(0);
                    if (c == 32) return '-';
                    if (c >= 65 && c <= 90) return '_' + s.toLowerCase();
                    return '__' + ('000' + c.toString(16)).slice(-4);
                }});
            }}

            let temp_link_classes = {{}};
            let seen_links = {{}};

            const decode_filter_classes = Object.entries(filters).reduce((prev, next) => ({{
                ...prev, [next[0]]: {{
                    ...(Object.keys(next[1]).reduce((_prev, key) => ({{
                        ..._prev,
                        [makeSafeForCSS(key)]: key
                    }}), {{}}))
                }}
            }}), {{}})

            function filter() {{
                updateList({{ target: {{ value: '' }} }})
                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            function uncheckAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = false;
                }});
                filter()
            }}

            function checkAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = true;
                }});
                filter()
            }}

            function toggleArbitraryKey(event, key_name) {{
                if (event.ctrlKey) {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = false;
                        $(`.keyword-id-${{makeSafeForCSS(arbitrary_key)}} input`).checked = false;
                    }});
                }}
                let decode_base_64 = decode_filter_classes[selected_tab_index][key_name];
                filters[selected_tab_index][decode_base_64] = !filters[selected_tab_index][decode_base_64]
                $(`.keyword-id-${{key_name}} input`).checked = filters[selected_tab_index][decode_base_64];

                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            String.prototype.lowerIncludes = function (string) {{
                return this.toLowerCase().includes(string.toLowerCase())
            }}
            String.prototype.maxLength = function (max_length) {{
                if (this?.length > max_length) return this.slice(0, max_length) + '...';
                else return this;
            }}

            function updateList(event) {{

                let filter_keys_tags = ``

                let temp_keys = Object.keys(filters[selected_tab_index]).filter(key_name => key_name?.lowerIncludes(event.target.value));

                temp_keys.sort((a, b) => {{
                    if (a?.lowerIncludes(event.target.value) == false && b?.lowerIncludes(event.target.value) == false) {{
                        return 0
                    }}
                    else if (a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value)) {{
                        return a?.indexOf(event.target.value) < b?.indexOf(event.target.value) ? -1 : 0
                    }}
                    else {{
                        return a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value) == false ? -1 : 0
                    }}
                }});

                temp_keys.forEach(arbitrary_key => {{
                    filter_keys_tags += `
                                    <label style="${{filter_counts[selected_tab_index][arbitrary_key] == undefined ? 'display:none' : ''}}" class="arbitrary-key keyword-id-${{makeSafeForCSS(arbitrary_key)}}">
                                        <input type="checkbox" onclick="toggleArbitraryKey(event, '${{makeSafeForCSS(arbitrary_key)}}')" ${{filters[selected_tab_index][arbitrary_key] ? 'checked' : 'unchecked'}}/>
                                        <span style="margin-right: 4px;" title='${{arbitrary_key}}'>${{arbitrary_key}}</span>
                                        <div class="filter-count">${{filter_counts[selected_tab_index][arbitrary_key] ?? 0}}</div>
                                    </label>
                                `;
                }});

                $('.filter-search-arbitrary .arbitrary-keys').innerHTML = `<div>` + filter_keys_tags + `</div>
                        <div class="filter-btns">
                            <span onclick="checkAll()">Выделить все</span>
                            <span onclick="uncheckAll()">Снять выделение</span>
                        </div>
                        ${{isMobile ? '' : `
                            <div class="filter-info">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
                                <div class="filter-info_prompt">Выделить только один<br/> через Ctrl + Click</div>
                            </div>
                        `}}
                    `
            }}

            let temp_pagination_count = 1;

            function get_domain_name(url) {{
                let a = document.createElement('a')
                a.href = url;
                return a.hostname;
            }}

            function isInViewport(el) {{
                const rect = el.getBoundingClientRect();

                var isinview = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)

                );

                return isinview;
            }}

            function check_all_items() {{
                Object.keys(temp_link_classes).forEach(link_class_name => {{
                    let bool = isInViewport($('#' + link_class_name))
                    if (bool) {{
                        seen_links[temp_link_classes[link_class_name]] = true;
                        let temp_svg = $(`#${{link_class_name}} .checkmark.unseen`);
                        if (temp_svg) temp_svg.addClass('seen_scale');
                        setTimeout(() => {{
                            if (temp_svg?.style?.display != undefined) temp_svg.style.display = 'none';
                        }}, 1100);
                    }}
                }})
            }}

            function update_fullname_data(tab_name) {{
                $(`input[name="fullname"]`).forEach(radio => {{
                    radio.checked = false;
                }})
                $(`input[name="fullname"]`)[fullname_filter[tab_name]].checked = true
                fullname_data[tab_name].forEach((count, i) => {{
                    $(`#fullname-${{i}}`).innerHTML = '&nbsp;' + (count ?? 0);
                }});
            }}

            function update_fullname_filter(event) {{
                let tab_name = tab_names[selected_tab_index];
                fullname_filter[tab_name] = event?.target?.value ?? 0;
                render_items(false, true)
            }}
            function update_social_type_counts(temp_items, type = 'socials') {{
                if (type == 'socials') {{
                    social_type_counts = {{
                        'Вконтакте': 0,
                        'Facebook': 0,
                        'Одноклассники': 0,
                        'Instagram': 0,
                        'Telegram': 0,
                    }}
                    temp_items.forEach(item => {{
                        social_type_counts[item.social_type]++;
                    }})
                }}
                else if (type == 'doc') {{
                    document_type_counts = {{
                        'PDF': 0,
                        'Word': 0,
                        'Excel': 0,
                        'PowerPoint': 0,
                        'Txt': 0,
                    }}
                    temp_items.forEach(item => {{
                        document_type_counts[item.doc_type]++;
                    }})
                    console.log('document_type_counts', document_type_counts);
                }}
                $(`.${{type}}_type-info`).forEach(temp_type => {{
                    temp_type.querySelector('span').innerText = (type == 'socials' ? social_type_counts : document_type_counts)[temp_type.dataset[type == 'socials' ? 'socialName' : 'documentName']]
                }})
            }}
            update_social_type_counts(items['socials'], 'socials')
            update_social_type_counts(items['documents'], 'doc')

            $('.socials_type-info').forEach(social_type => {{
                social_type.addEventListener('click', (event) => {{
                    if (event.ctrlKey) {{
                        $('.socials_type-info').forEach(sub_social_type => {{
                            sub_social_type.firstElementChild.removeClass('selected')
                            social_types[sub_social_type.dataset.socialName] = false;
                        }})
                    }}
                    if (social_type.firstElementChild.hasClass('selected')) {{
                        social_type.firstElementChild.removeClass('selected')
                        social_types[social_type.dataset.socialName] = false;
                    }}
                    else {{
                        social_type.firstElementChild.addClass('selected')
                        social_types[social_type.dataset.socialName] = true;
                    }}
                    render_items(true)
                }})
            }})
            $('.doc_type-info').forEach(social_type => {{
                social_type.addEventListener('click', (event) => {{
                    if (event.ctrlKey) {{
                        $('.doc_type-info').forEach(sub_social_type => {{
                            sub_social_type.firstElementChild.removeClass('selected')
                            document_types[sub_social_type.dataset.documentName] = false;
                        }})
                    }}
                    if (social_type.firstElementChild.hasClass('selected')) {{
                        social_type.firstElementChild.removeClass('selected')
                        document_types[social_type.dataset.documentName] = false;
                    }}
                    else {{
                        social_type.firstElementChild.addClass('selected')
                        document_types[social_type.dataset.documentName] = true;
                    }}
                    render_items(true)
                }})
            }})

            const minus_social_resources = [
                'sociumin.com',
                'socialbase.ru',
                'sociuminfo.com',
                'vkanketa.ru',
                'namebook.club',
                'bigbookname.com',
                'vk.watch',
                'vkplaneta.ru',
            ];

            function render_items(update_social_type = false, update_social_type_count = false) {{
                let result = ``;
                let tab_name = tab_names[selected_tab_index];


                let temp_items = [...items[tab_name]];

                // fullname_data
                // fullname_filter

                let fullname = fullname_filter[tab_name] ?? 0;

                const minus_social_resources_chbox = $('#minus-social-resources').checked;

                if (minus_social_resources_chbox) {{
                    fullname_data[tab_name] = [0,0,0];
                    temp_items = temp_items.filter(item => {{
                        let bool = !minus_social_resources.some(social_resource => item.link.toLowerCase().includes(social_resource));

                        if (bool) {{
                            if (item.fullname) {{
                                fullname_data[tab_name][1]++
                            }}
                            else {{
                                fullname_data[tab_name][2]++
                            }}
                            fullname_data[tab_name][0]++
                        }}

                        return bool
                    }})
                }}


                if (minus_keywords.length) {{
                    fullname_data[tab_name] = [0,0,0];
                    temp_items = temp_items.filter(item => {{
                        let bool = !minus_keywords.some(minus_keyword => (item.title.toLowerCase().includes(minus_keyword) || item.link.toLowerCase().includes(minus_keyword) || item.content.toLowerCase().includes(minus_keyword)));

                        if (bool) {{
                            if (item.fullname) {{
                                fullname_data[tab_name][1]++
                            }}
                            else {{
                                fullname_data[tab_name][2]++
                            }}
                            fullname_data[tab_name][0]++
                        }}

                        return bool
                    }})
                }}

                update_fullname_data(tab_name);

                if ([1, 2].includes(+fullname)) {{
                    temp_items = temp_items.filter(item => (item.fullname == {{ 1: true, 2: false }}[fullname]))
                }}
                $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;

                if (update_social_type_count) update_social_type_counts(temp_items, tab_name == 'socials' ? tab_name : 'doc')

                if (isFilterableTab()) {{
                    if (tab_name == 'socials') {{
                        temp_items = temp_items.filter(item => (social_types[item?.social_type]))
                    }}
                    else if (tab_name == 'documents') {{
                        temp_items = temp_items.filter(item => (document_types[item?.doc_type]))
                    }}

                    if (update_social_type) {{
                        filter_counts[selected_tab_index] = {{}};
                        temp_items.forEach(item => {{
                            item.keyword_list.forEach(keyword => {{
                                if (!filter_counts[selected_tab_index][keyword]) {{
                                    filter_counts[selected_tab_index][keyword] = 0;
                                }}
                                filter_counts[selected_tab_index][keyword]++;
                            }});
                        }})
                        updateList({{ target: {{ value: '' }} }})
                    }}

                    temp_items = temp_items.filter(item => (item.keyword_list.find(keyword => filters[selected_tab_index][keyword])))

                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}
                else if (tab_name == 'main') {{
                    temp_items = temp_items.filter(item => (+(item?.keyword_list?.length ?? 0) >= startRangeValue && +(item?.keyword_list?.length ?? 0) <= endRangeValue))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}

                temp_pagination_count = Math.ceil(temp_items?.length / range) || 1;

                if (tab_pages[tab_name].page > temp_pagination_count) tab_pages[tab_name].page = temp_pagination_count;


                let sliced_items = JSON.parse(JSON.stringify(
                    temp_items.slice((tab_pages[tab_name].page - 1) * range, tab_pages[tab_name].page * range)
                ));

                if (isFilterableTab()) {{
                    sliced_items.forEach(sliced_item => {{
                        sliced_item.keyword_list = sliced_item.keyword_list.filter(keyword => filters[selected_tab_index][keyword])
                    }});
                }}

                temp_link_classes = {{}};

                sliced_items.forEach(item => {{

                    let keyword_list = ``
                    item?.keyword_list.forEach(query => {{
                        if (keyword_list) keyword_list += '<span style="color:black;font-size:17px">, </span>'
                        keyword_list += `<span
                                        class="query"
                                        onclick="copy(this)">${{decodeURI(query.trim())}}</span>`
                    }})

                    // Вес ссылки
                    // Похожие

                    let temp_link_class = makeSafeForCSS(item?.link);

                    temp_link_classes[temp_link_class] = item?.link;

                    result += `
                                <div class="item-container ${{seen_links[item?.link] ? 'seen_link' : ''}}" id="${{temp_link_class}}">
                                    <div class="item" style="position:relative">
                                        ${{seen_links[item?.link] ? '<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>' : '<svg class="checkmark unseen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"></circle></svg>'}}

                                        <div class="flex items-center">
                                            <a target="_blank" href="${{item?.link}}" class="item-title" title="${{item?.title}}">${{item?.title}}</a>
                                            <!-- <a target="_blank" href="${{item?.link}}" class="item-more">Источник <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M320 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h82.7L201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L448 109.3V192c0 17.7 14.3 32 32 32s32-14.3 32-32V32c0-17.7-14.3-32-32-32H320zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg></a> -->
                                        </div>
                                        <div class="item-content">${{item?.content}}</div>
                                        <div class="item-info" style="display:flex;align-items:center;margin-top:5px;font-size:12px;">
                                            <a href="${{item?.link}}" target="_blank" style="color: #4d4dff;" title="${{get_domain_name(item?.link)}}">${{get_domain_name(item?.link).maxLength(20)}}</a>

                                            <span style="margin: 0 .8em;white-space:nowrap;display:flex;align-items:center;cursor:default;" title="Вес ссылки: найдено ${{item?.keyword_list?.length ?? 0}} раз">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="max-width:12px;min-width:12px;"
                                                    viewBox="0 0 512 512">
                                                    <path
                                                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                                                </svg>
                                                <span style="margin-left:5px;font-size:12px;">${{item?.keyword_list?.length ?? 0}}</span>
                                            </span>

                                            <div class="mt-auto item-keywords">
                                                <div class="item-param"><div class="query-content" title='${{decodeURI(item?.keyword_list?.join(',  '))}}'><span style="color:black">
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:12px;fill:#9300FF;margin-bottom: -2.1px;"><path d="M336 352c97.2 0 176-78.8 176-176S433.2 0 336 0S160 78.8 160 176c0 18.7 2.9 36.8 8.3 53.7L7 391c-4.5 4.5-7 10.6-7 17v80c0 13.3 10.7 24 24 24h80c13.3 0 24-10.7 24-24V448h40c13.3 0 24-10.7 24-24V384h40c6.4 0 12.5-2.5 17-7l33.3-33.3c16.9 5.4 35 8.3 53.7 8.3zM376 96a40 40 0 1 1 0 80 40 40 0 1 1 0-80z"/></svg> </span>${{keyword_list}}
                                                    <small class="prompt">Копировать при клике</small></div>
                                                </div>
                                                <!-- <div class="item-param">Дубликаты: <span class="param-text">${{item?.link_weight}}</span></div> -->
                                                <!-- <div class="item-param">Фигурирует в списках: <span class="param-text">${{item?.has_in_list}}</span></div> -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                }});

                if (items[tab_name].length) {{
                    $(`.tab-content-${{tab_indexes[tab_name]}}`).innerHTML = result
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'flex'
                    }});
                }}
                else {{
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'none'
                    }});
                }}

                update_pagination()
                check_all_items()

            }}

            function update_pagination() {{
                let tab_name = tab_names[selected_tab_index];
                let start_page = 1

                if (tab_pages[tab_name].page > 5) start_page = tab_pages[tab_name].page - 5;

                let page_tags = ``

                for (let i = start_page; i <= ((start_page + 9) <= temp_pagination_count ? start_page + 9 : temp_pagination_count); i++) {{
                    page_tags += `<span onclick="set_page('${{tab_names[selected_tab_index]}}', ${{i}})" ${{tab_pages[tab_name].page == i ? 'class="selected"' : ''}}>${{i}}</span>`
                }}
                $(`.pagination`).html(`
                        <div class="flex hovered-angle">
                            <svg class="first-page" onclick="first_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                            </svg>
                            <svg onclick="minus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z" />
                            </svg>
                        </div>
                        <div class="flex h-full scrollbar">
                            ${{page_tags}}
                        </div>
                        <div class="flex hovered-angle">
                            <svg onclick="plus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
                            </svg>
                            <svg class="last-page" onclick="last_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                            </svg>
                        </div>
                    `);
            }}

            render_items()

            window.onscroll = function (event) {{

                check_all_items();
            }}

            update_global_counts()

        </script>

        <script>

            const colors = Highcharts.getOptions().colors.map((c, i) =>
                // Start out with a darkened base color (negative brighten), and end
                // up with a much brighter color
                Highcharts.color(Highcharts.getOptions().colors[0])
                    .brighten((i - 3) / 7)
                    .get()
            );
            // Data retrieved from https://netmarketshare.com/
            // Build the chart
            Highcharts.chart('container', {{
                chart: {{
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie',
                }},
                credits: false,
                title: {{
                    text: `<div style="text-align: center;line-height: 1.6"><b style="font-size:35px">${{Object.values(seriesData).reduce((prev, next) => (prev + next.y), 0)}}</b><br><span style="font-size:16px;color: #ccc">материалов</span></div>`,
                    useHTML: true,
                    align: 'center',
                    verticalAlign: 'middle',
                    y: 15,
                    x: -100,
                }},
                legend: {{
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical',
                    x: 0,
                    useHTML: true,
                    labelFormat: `<div style="display:flex;width: 150px"><span>{{name}}</span> <div style="margin-left:auto;font-weight:600;">{{y}}</div></div>`, // : {{y}} | {{percentage:.1f}}%
                }},
                tooltip: {{
                    pointFormat: '{{point.name}}: <b>{{point.percentage:.1f}}%</b>',
                    headerFormat: ''
                }},
                accessibility: {{
                    point: {{
                        valueSuffix: '%'
                    }}
                }},
                plotOptions: {{
                    pie: {{
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {{
                            enabled: false,
                        }},
                        colors,
                        showInLegend: true,
                        // tooltip: {{
                        //     footerFormat: ''
                        // }}
                    }}
                }},
                series: [{{
                    // name: ' ',
                    colorByPoint: true,
                    innerSize: '80%',
                    // dataLabels: {{
                    //     formatter: function() {{
                    //         return this.point.name; //<--------------- If the slice has a value greater than 5 show it.
                    //     }},
                    //     // color: '#ffffff',
                    //     // distance: -30
                    // }},
                    data: seriesData,
                }}]
            }})
            const first_tab_index = (Object.values(items).findIndex(item_values => item_values.length) || 0) + 1; 

            // if (first_tab_index != 1) {{ 
            //     $('.tab-1').style.display = 'none'; 
            // }}

            select_tab(first_tab_index);
        </script>
    </body>

    </html>
"""

    return report_html


def response_company_template(titles, items, filters, fullname_counters, extra_titles="") -> str:
    report_html = f"""<!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titles[0]}</title>
            {COMPANY_STYLE}
        </head>

        <body>
            <div class="tab-head" onclick="closeModal(event)">
                <div id="head-info" style="margin-bottom: 6px;transition: .15s;overflow:hidden;width: 100%;height:105px">
            <h2 style="display: inline;cursor:pointer;" class="object-full_name" onclick="$('#head-info').style.height = ($('#head-info').style.height == '105px' ? '28px' : '105px');$('#head-info h2 svg').style.transform = ($('#head-info').style.height == '105px' ? 'rotateX(180deg)' : 'rotateX(0deg)')">Объект: <span style="white-space:nowrap; text-transform: capitalize;">{titles[0]}</span>
                <svg xmlns="http://www.w3.org/2000/svg" style="width:15px;margin-bottom: -2px;transition: .15s;transform:rotateX(180deg);" viewBox="0 0 448 512"><path d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>
                    </h2>
                <div class="flex justify-center" style="flex-direction:column;width: 100%;">
                    <span class="max-text-length" title="Категории поиска: {titles[1]}"><b>Категории поиска:</b>{titles[1]}</span>
                    <span class="max-text-length" title="Произвольные ключевые слова: {titles[2]}"><b>Произвольные ключевые слова: </b> {titles[2]}</span>
                    <span class="max-text-length" title="Минус-слова: {titles[3]}"><b>Минус-слова:</b> {titles[3]}</span>
                    <span class="max-text-length" title="Плюс-слова: {titles[4]}"><b>Плюс-слова:</b> {titles[4]}</span>
                    {extra_titles}
                </div>

                </div>

                <div class=" tabs flex flex-wrap items-center">
                    <div class="tab-1 selected" onclick="select_tab(1)">
                        Главное
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-2" onclick="select_tab(2)">
                        Произвольные
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-3" onclick="select_tab(3)">
                        Негатив
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-4" onclick="select_tab(4)">
                        Репутация
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-5" onclick="select_tab(5)">
                        Связи
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-6" onclick="select_tab(6)">
                        Соц.сети
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-7" onclick="select_tab(7)">Документы
                        <span class="tab-count">0</span>
                    </div>
                    <div class="tab-8" onclick="select_tab(8)">Все материалы
                        <span class="tab-count">0</span>
                    </div>
                </div>
            </div>

            <script>{HIGHCHARTS}</script>

            <div style="display: flex;gap: 15px;padding: 15px 15px 0;flex-wrap: wrap;justify-content: center;">
            <div id="container" style="min-width: 424px; height: 230px; border-radius: 6px; overflow: hidden;"></div>
            <div class="socials" id="socials" style="display:none">
                <div class="socials_type-info" data-social-name="Вконтакте">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected vk">
                        <path
                            d="M31.4907 63.4907C0 94.9813 0 145.671 0 247.04V264.96C0 366.329 0 417.019 31.4907 448.509C62.9813 480 113.671 480 215.04 480H232.96C334.329 480 385.019 480 416.509 448.509C448 417.019 448 366.329 448 264.96V247.04C448 145.671 448 94.9813 416.509 63.4907C385.019 32 334.329 32 232.96 32H215.04C113.671 32 62.9813 32 31.4907 63.4907ZM75.6 168.267H126.747C128.427 253.76 166.133 289.973 196 297.44V168.267H244.16V242C273.653 238.827 304.64 205.227 315.093 168.267H363.253C359.313 187.435 351.46 205.583 340.186 221.579C328.913 237.574 314.461 251.071 297.733 261.227C316.41 270.499 332.907 283.63 346.132 299.751C359.357 315.873 369.01 334.618 374.453 354.747H321.44C316.555 337.262 306.614 321.61 292.865 309.754C279.117 297.899 262.173 290.368 244.16 288.107V354.747H238.373C136.267 354.747 78.0267 284.747 75.6 168.267Z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Facebook">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected fb">
                        <path
                            d="M400 32H48A48 48 0 0 0 0 80v352a48 48 0 0 0 48 48h137.25V327.69h-63V256h63v-54.64c0-62.15 37-96.48 93.67-96.48 27.14 0 55.52 4.84 55.52 4.84v61h-31.27c-30.81 0-40.42 19.12-40.42 38.73V256h68.78l-11 71.69h-57.78V480H400a48 48 0 0 0 48-48V80a48 48 0 0 0-48-48z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Instagram">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected insta">
                        <path
                            d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Telegram">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512"
                        class="social_type selected tg">
                        <path d="M248,8C111.033,8,0,119.033,0,256S111.033,504,248,504,496,392.967,496,256,384.967,8,248,8ZM362.952,176.66c-3.732,39.215-19.881,134.378-28.1,178.3-3.476,18.584-10.322,24.816-16.948,25.425-14.4,1.326-25.338-9.517-39.287-18.661-21.827-14.308-34.158-23.215-55.346-37.177-24.485-16.135-8.612-25,5.342-39.5,3.652-3.793,67.107-61.51,68.335-66.746.153-.655.3-3.1-1.154-4.384s-3.59-.849-5.135-.5q-3.283.746-104.608,69.142-14.845,10.194-26.894,9.934c-8.855-.191-25.888-5.006-38.551-9.123-15.531-5.048-27.875-7.717-26.8-16.291q.84-6.7,18.45-13.7,108.446-47.248,144.628-62.3c68.872-28.647,83.183-33.623,92.511-33.789,2.052-.034,6.639.474,9.61,2.885a10.452,10.452,0,0,1,3.53,6.716A43.765,43.765,0,0,1,362.952,176.66Z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="socials_type-info" data-social-name="Одноклассники">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"
                        class="social_type selected ok">
                        <path
                            d="M184.2 177.1c0-22.1 17.9-40 39.8-40s39.8 17.9 39.8 40c0 22-17.9 39.8-39.8 39.8s-39.8-17.9-39.8-39.8zM448 80v352c0 26.5-21.5 48-48 48H48c-26.5 0-48-21.5-48-48V80c0-26.5 21.5-48 48-48h352c26.5 0 48 21.5 48 48zm-305.1 97.1c0 44.6 36.4 80.9 81.1 80.9s81.1-36.2 81.1-80.9c0-44.8-36.4-81.1-81.1-81.1s-81.1 36.2-81.1 81.1zm174.5 90.7c-4.6-9.1-17.3-16.8-34.1-3.6 0 0-22.7 18-59.3 18s-59.3-18-59.3-18c-16.8-13.2-29.5-5.5-34.1 3.6-7.9 16.1 1.1 23.7 21.4 37 17.3 11.1 41.2 15.2 56.6 16.8l-12.9 12.9c-18.2 18-35.5 35.5-47.7 47.7-17.6 17.6 10.7 45.8 28.4 28.6l47.7-47.9c18.2 18.2 35.7 35.7 47.7 47.9 17.6 17.2 46-10.7 28.6-28.6l-47.7-47.7-13-12.9c15.5-1.6 39.1-5.9 56.2-16.8 20.4-13.3 29.3-21 21.5-37z">
                        </path>
                    </svg>
                    <span>0</span>
                </div>
            </div>
            <div class="documents" id="documents" style="display:none">
                <div class="doc_type-info" data-document-name="PDF" title="Формат - PDF">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
                        class="doc_type selected pdf">
                        <path d="M64 464H96v48H64c-35.3 0-64-28.7-64-64V64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V288H336V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16zM176 352h32c30.9 0 56 25.1 56 56s-25.1 56-56 56H192v32c0 8.8-7.2 16-16 16s-16-7.2-16-16V448 368c0-8.8 7.2-16 16-16zm32 80c13.3 0 24-10.7 24-24s-10.7-24-24-24H192v48h16zm96-80h32c26.5 0 48 21.5 48 48v64c0 26.5-21.5 48-48 48H304c-8.8 0-16-7.2-16-16V368c0-8.8 7.2-16 16-16zm32 128c8.8 0 16-7.2 16-16V400c0-8.8-7.2-16-16-16H320v96h16zm80-112c0-8.8 7.2-16 16-16h48c8.8 0 16 7.2 16 16s-7.2 16-16 16H448v32h32c8.8 0 16 7.2 16 16s-7.2 16-16 16H448v48c0 8.8-7.2 16-16 16s-16-7.2-16-16V432 368z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Word" title="Формат - Word">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected word">
                        <path d="M48 448V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm55 241.1c-3.8-12.7-17.2-19.9-29.9-16.1s-19.9 17.2-16.1 29.9l48 160c3 10.2 12.4 17.1 23 17.1s19.9-7 23-17.1l25-83.4 25 83.4c3 10.2 12.4 17.1 23 17.1s19.9-7 23-17.1l48-160c3.8-12.7-3.4-26.1-16.1-29.9s-26.1 3.4-29.9 16.1l-25 83.4-25-83.4c-3-10.2-12.4-17.1-23-17.1s-19.9 7-23 17.1l-25 83.4-25-83.4z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Excel" title="Формат - Excel">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected excel">
                        <path d="M48 448V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm90.9 233.3c-8.1-10.5-23.2-12.3-33.7-4.2s-12.3 23.2-4.2 33.7L161.6 320l-44.5 57.3c-8.1 10.5-6.3 25.5 4.2 33.7s25.5 6.3 33.7-4.2L192 359.1l37.1 47.6c8.1 10.5 23.2 12.3 33.7 4.2s12.3-23.2 4.2-33.7L222.4 320l44.5-57.3c8.1-10.5 6.3-25.5-4.2-33.7s-25.5-6.3-33.7 4.2L192 280.9l-37.1-47.6z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="PowerPoint" title="Формат - PowerPoint">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected pptx">
                        <path d="M64 464c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm72 208c-13.3 0-24 10.7-24 24V336v56c0 13.3 10.7 24 24 24s24-10.7 24-24V360h44c42 0 76-34 76-76s-34-76-76-76H136zm68 104H160V256h44c15.5 0 28 12.5 28 28s-12.5 28-28 28z"/>
                    </svg>
                    <span>0</span>
                </div>
                <div class="doc_type-info" data-document-name="Txt" title="Формат - Txt">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"
                        class="doc_type selected txt">
                        <path d="M64 464c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16H224v80c0 17.7 14.3 32 32 32h80V448c0 8.8-7.2 16-16 16H64zM64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V154.5c0-17-6.7-33.3-18.7-45.3L274.7 18.7C262.7 6.7 246.5 0 229.5 0H64zm56 256c-13.3 0-24 10.7-24 24s10.7 24 24 24H264c13.3 0 24-10.7 24-24s-10.7-24-24-24H120zm0 96c-13.3 0-24 10.7-24 24s10.7 24 24 24H264c13.3 0 24-10.7 24-24s-10.7-24-24-24H120z"/>
                    </svg>
                    <span>0</span>
                </div>
            </div>
            <div>
            <div
                style="display: none;align-items: center;height: 34px;font-size: 13.5px;background: white;padding: 0 10px;border-radius: 5px;white-space:nowrap">
                <div style="font-size: 16px;margin-right: 10px;">Совпадения: </div>
                <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                        onchange="update_fullname_filter(event)" checked value="0"> все данные <span
                        id="fullname-0">48</span> </label>
                <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                        onchange="update_fullname_filter(event)" value="1"> полное совпадение <span
                        id="fullname-1">32</span> </label>
                <label style="display: flex;"><input type="radio" style="margin-left: 20px;" name="fullname"
                        onchange="update_fullname_filter(event)" value="2"> частичное совпадение <span
                        id="fullname-2">16</span></label>
            </div>
            <label class="parent-prompt-hover" style="display: inline-flex;align-items: center;margin: 6px 0;background: white;border-radius: 4px;height: 32px;padding: 0 11px 3px 9px;cursor: pointer;user-select: none;"> 
                    <input id="minus-social-resources" type="checkbox" onchange="render_items(false, true)" style="margin: 2px 5px 0px 0;cursor: pointer;"> 
                    <small class="prompt">Исключает из справки сервисы поиска аккаунтов в соц. сетях: socialbase.ru, bigbookname.com и другие.</small> 
                    <span style="font-size: 15px;">Скрыть архивы социальных сетей</span> 
            </label>
                <!-- -->
                <div style="
                    display: flex;
                    align-items: center;
                ">
                    <div style="font-weight: 600;margin-top: 4px;margin-right: 6px;letter-spacing: .75px;">Стоп-фильтр: </div>
                    <div class="minus-keywords-block" style="
                    margin-top: 5px;
                    display: flex;
                    align-items: center;
                    width: 350px;height: 30px;">
                        <div style="
                    position: relative;
                    height: 30px;
                    width: 100%;
                    display: flex;
                " class="parent-prompt">
                            <input type="text" onkeydown="event.keyCode == 13 ? add_minus_keyword() : ''"
                                style="height: 30px;outline: none;border: none;padding: 0 10px;font-size: 14.5px;width: 100%;border-radius: 3px 0 0 3px;"
                                placeholder="Минус-слова" id="minus-keyword">
                            <small class="prompt">Добавьте стоп-слова для исключения содержащих их материалов. Пример: для исключения всех материалов, содержащих слова "адвокат", "адвокатский", "адвоката", достаточно добавить одно стоп-слово "адвокат".</small>
                            <svg xmlns="http://www.w3.org/2000/svg"
                                onclick="this.nextElementSibling.classList.toggle('hide-keywords-modal')" viewBox="0 0 448 512" style="
                    background: white;
                    width: 20px;
                    fill: #676666;
                    padding-right: 6px;
                    cursor: pointer;
                ">
                                <path
                                    d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z">
                                </path>
                            </svg>


                            <div class="minus-keywords-modal scrollbar hide-keywords-modal">
                                <div class="minus-keyword" onclick="remove_minus_keyword(this)">
                                    <span>Список пустой</span>
                                </div>
                            </div>
                        </div>

                        <button style="
                    padding: 0 8px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    border: none;
                    background: rgb(26, 179, 148);
                    color: white;
                    border-radius: 0 3px 3px 0;
                    cursor: pointer;
                " onclick="add_minus_keyword()">Добавить</button>
                    </div>
                </div>
                <!-- -->
                </div>
        </div>


        <div class="flex items-center wrap-reverse-container" style="padding: 0 10px;">
            <div class="similars-range" style="padding-left: 20px;">
                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="position:absolute;left:5px;top:4px;"
                    viewBox="0 0 512 512">
                    <path
                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                </svg>
                <div slider id="slider-distance">
                    <div>
                        <div inverse-left style="width:100%;"></div>
                        <div inverse-right style="width:100%;"></div>
                        <div range style="left:0%;right:0%;"></div>
                        <span thumb style="left:0%;"></span>
                        <span thumb style="left:100%;"></span>
                        <div sign style="left:0%;">
                            <span id="value">0</span>
                        </div>
                        <div sign style="left:100%;">
                            <span id="value">100</span>
                        </div>
                    </div>
                    <input id="startRangeValue" type="range" tabindex="0" value="0" max="100" min="0" step="1"
                        onchange="update_startRangeValue(+event.target.value)" oninput="startRange(event)" />

                    <input id="endRangeValue" type="range" tabindex="0" value="100" max="100" min="0" step="1"
                        onchange="update_endRangeValue(+event.target.value)" oninput="endRange(event)" />
                </div>
            </div>
            <div class="filter-search-arbitrary" style="display: none;">
                <label class="input">
                    <!-- Введите название произвольного ключа -->
                    <input type="text" placeholder="Введите название ключа" onclick="showListModal(event)"
                        oninput="updateList(event)" />
                    <svg onclick="toggleListModal(event)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" id="arbitrary-angle-id">
                        <path
                            d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
                    </svg>
                    <div class="arbitrary-keys" onclick="showListModal(event)">
                    </div>
                </label>
            </div>
            <div class="pagination-container" onclick="closeModal(event)">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <div class="content" onclick="closeModal(event)">
            <div class="tab-content-1 selected">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-2">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-3">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-4">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-5">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-6">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-7">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
            <div class="tab-content-8">
                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Недостаточно материалов, перейдите во вкладку «Все материалы»
                </div>
            </div>
        </div>

        <div class="flex" onclick="closeModal(event)">
            <div class="pagination-container" style="padding: 0 7.5px 15px;">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <script>

            let minus_keywords = [];

            function remove_minus_keyword(element) {{
                let keyword_name = element.previousElementSibling.textContent.trim()
                let keyword_index = minus_keywords.indexOf(keyword_name);
                if (keyword_index != -1) {{
                    delete minus_keywords[keyword_index];
                    document.querySelector('#minus-keyword').value = '';
                    add_minus_keyword()
                }}
            }}

            function add_minus_keyword() {{
                let keyword_name = document.querySelector('#minus-keyword')?.value ?? '';
                keyword_name = keyword_name.trim().toLowerCase()
                if (!minus_keywords.includes(keyword_name) && keyword_name != '') {{
                    minus_keywords.push(keyword_name);
                }}
                render_items(false, true)

                let minus_keywords_modal = '';

                minus_keywords.forEach(keyword => {{
                    minus_keywords_modal += `
                        <div class="minus-keyword">
                            <span title="${{keyword}}">${{keyword}}</span>
                            <svg onclick="remove_minus_keyword(this)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"></path></svg>
                        </div>
                    `
                }})

                document.querySelector('.minus-keywords-modal').innerHTML = minus_keywords_modal

                console.log('minus_keywords', minus_keywords);


                document.querySelector('.minus-keywords-modal').classList.remove('hide-keywords-modal');

                document.querySelector('#minus-keyword').value = '';
                document.querySelector('#minus-keyword').focus();
                update_global_counts()
            }}
            let startRangeValue = 0;
            let endRangeValue = 0;

            function update_startRangeValue(value) {{
                startRangeValue = value;
                render_items()
            }}
            function update_endRangeValue(value) {{
                endRangeValue = value;
                render_items()
            }}

            const startRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.min($this.value, $this.parentNode.childNodes[5].value - 1);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[1].style.width = value + '%';
                children[5].style.left = value + '%';
                children[7].style.left = value + '%'; children[11].style.left = value + '%';
                children[11].childNodes[1].innerHTML = $this.value;
            }}
            const endRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.max($this.value, $this.parentNode.childNodes[3].value);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[3].style.width = (100 - value) + '%';
                children[5].style.right = (100 - value) + '%';
                children[9].style.left = value + '%'; children[13].style.left = value + '%';
                children[13].childNodes[1].innerHTML = $this.value;
            }}

            const isMobile = Boolean(navigator.userAgent.match(/Android/i)
                || navigator.userAgent.match(/webOS/i)
                || navigator.userAgent.match(/iPhone/i)
                || navigator.userAgent.match(/iPad/i)
                || navigator.userAgent.match(/iPod/i)
                || navigator.userAgent.match(/BlackBerry/i)
                || navigator.userAgent.match(/Windows Phone/i));

            console.log('isMobile', isMobile, navigator.userAgent);

            let selected_tab_index = 1
            function $(str) {{
                let elements = document?.querySelectorAll(str);

                return (elements?.length == 1 || str[0] == '#') ? document?.querySelector(str) : elements;
            }}
            Object.prototype.html = function (html) {{
                this?.forEach(item => {{
                    item.innerHTML = html
                }});
            }}
            Object.prototype.hasClass = function (className) {{
                return this?.classList?.contains(className)
            }}
            Object.prototype.addClass = function (className) {{
                this?.classList?.add(className)
            }}
            Object.prototype.removeClass = function (className) {{
                this?.classList?.remove(className)
            }}

            let filterable_tabs = [2, 3, 4, 5, 6, 7, 8]
            const items = {{
                    main: [
                        {items.get("main")}
                    ],
                    arbitrary: [{items.get("free")}],
                    negative: [{items.get("negative")}],
                    reputation: [{items.get("reputation")}],
                    connections: [{items.get("relation")}],
                    socials: [{items.get("socials")}],
                    documents: [{items.get("documents")}],
                    all_materials: [{items.get("all")}],
                }}

            endRangeValue = []
            items.main.forEach(item => {{
                endRangeValue.push(+item.keyword_list.length)
            }});
            startRangeValue = endRangeValue.length ? Math.min(...endRangeValue) : 0
            endRangeValue = endRangeValue.length ? Math.max(...endRangeValue) : 0

            let endRangeElement = $('#endRangeValue');
            let startRangeElement = $('#startRangeValue');
            startRangeElement.min = endRangeElement.min = startRangeElement.value = startRangeValue;
            startRangeElement.max = endRangeElement.max = endRangeElement.value = endRangeValue;
            startRange({{ target: startRangeElement }})
            endRange({{ target: endRangeElement }})


            const tab_names = {{
                1: 'main',
                2: 'arbitrary',
                3: 'negative',
                4: 'reputation',
                5: 'connections',
                6: 'socials',
                7: 'documents',
                8: 'all_materials',
            }}

            function isFilterableTab() {{
                return filterable_tabs.find(filterable_tab => filterable_tab == selected_tab_index) != undefined
            }}
            function select_tab(new_tab_index) {{

                $('#socials').style.display = new_tab_index == 6 ? '' : 'none'
                $('#documents').style.display = new_tab_index == 7 ? '' : 'none'
                if (selected_tab_index == new_tab_index) return

                $('#container').style.display = new_tab_index == 1 ? '' : 'none'
                document.querySelector('.minus-keywords-block').parentElement.style.display = new_tab_index == 1 ? 'flex' : 'none';
                document.querySelector('#minus-social-resources').parentElement.style.display = new_tab_index == 1 ? 'inline-flex' : 'none';

                $(`.tab-${{new_tab_index}}`)?.addClass('selected')
                $(`.tab-content-${{new_tab_index}}`)?.addClass('selected')

                $(`.tab-${{selected_tab_index}}`)?.removeClass('selected')
                $(`.tab-content-${{selected_tab_index}}`)?.removeClass('selected')

                selected_tab_index = new_tab_index

                render_items(false, true)
                let tab_name = tab_names[selected_tab_index];

                if (isFilterableTab() && items[tab_names[selected_tab_index]]?.length > 0) {{

                    filter_counts[selected_tab_index] = {{}};
                    items[tab_names[selected_tab_index]].forEach(item => {{
                        item.keyword_list.forEach(keyword => {{
                            if (!filter_counts[selected_tab_index][keyword]) {{
                                filter_counts[selected_tab_index][keyword] = 0;
                            }}
                            filter_counts[selected_tab_index][keyword]++;
                        }});
                    }})
                    updateList({{ target: {{ value: '' }} }})
                    $(`.filter-search-arbitrary`).style.display = 'block';
                }}
                else {{
                    $(`.filter-search-arbitrary`).style.display = 'none';
                }}
                $(`.similars-range`).style.display = new_tab_index == 1 ? 'block' : 'none';

            }}
            function copy(that) {{
                var inp = document.createElement('input');
                document.body.appendChild(inp)
                inp.value = that.textContent
                inp.select();
                document.execCommand('copy', false);
                inp.remove();
            }}
            const tab_indexes = {{
                main: 1,
                arbitrary: 2,
                negative: 3,
                reputation: 4,
                connections: 5,
                socials: 6,
                documents: 7,
                all_materials: 8,
            }}

            const fullname_data = {{
                    main: {fullname_counters.get("main")},
                    arbitrary: {fullname_counters.get("arbitrary")},
                    negative: {fullname_counters.get("negative")},
                    reputation: {fullname_counters.get("reputation")},
                    connections: {fullname_counters.get("connections")},
                    socials: {fullname_counters.get("socials")},
                    documents: {fullname_counters.get("documents")},
                    all_materials: {fullname_counters.get("all_materials")},
                }}

            // items.forEach

            const fullname_filter = {{
                main: 0,
                arbitrary: 0,
                negative: 0,
                reputation: 0,
                connections: 0,
                socials: 0,
                documents: 0,
                all_materials: 0,
            }}


            Object.entries(tab_indexes).forEach(([tab_name, tab_index]) => {{
                $(`.tab-${{tab_index}} .tab-count`).innerHTML = items[tab_name]?.length
            }});
            const tab_pages = {{
                main: {{
                    count: 0,
                    page: 1,
                }},
                arbitrary: {{
                    count: 0,
                    page: 1,
                }},
                negative: {{
                    count: 0,
                    page: 1,
                }},
                reputation: {{
                    count: 0,
                    page: 1,
                }},
                connections: {{
                    count: 0,
                    page: 1,
                }},
                socials: {{
                    count: 0,
                    page: 1,
                }},
                documents: {{
                    count: 0,
                    page: 1,
                }},
                all_materials: {{
                    count: 0,
                    page: 1,
                }},
            }}

            function set_page(tab_name, page) {{
                tab_pages[tab_name].page = page;
                render_items()
                update_pagination()
            }}
            function minus_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page -= 1;
                render_items()
                update_pagination()
            }}
            function first_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page = 1;
                render_items()
                update_pagination()
            }}
            function plus_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page += 1;
                render_items()
                update_pagination()
            }}
            function last_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page = tab_pages[tab_name].count;
                render_items()
                update_pagination()
            }}

            const range = 20;

            let seriesData = [
                {{
                    name: 'Произвольные',
                    y: 0,
                }},
                {{
                    name: 'Негатив',
                    y: 0
                }},
                {{
                    name: 'Репутация',
                    y: 0
                }},
                {{
                    name: 'Связи',
                    y: 0
                }},
                {{
                    name: 'Соц.сети',
                    y: 0
                }},
                {{
                    name: 'Документы',
                    y: 0
                }}
            ]

            function update_global_counts() {{

                Object.keys(items).forEach(tab_name => {{
                    if (items[tab_name]?.length) {{
                        if (filterable_tabs.includes(tab_indexes[tab_name])) {{

                            let temp_items = [...items[tab_name]];

                            if (minus_keywords.length) {{
                                temp_items = temp_items.filter(item => !minus_keywords.some(minus_keyword => (item.title.toLowerCase().includes(minus_keyword) || item.link.toLowerCase().includes(minus_keyword) || item.content.toLowerCase().includes(minus_keyword))))
                            }}
                            tab_pages[tab_name].count = Math.ceil(temp_items?.length / range);

                            $(`.tab-${{tab_indexes[tab_name]}} .tab-count`).innerHTML = seriesData[tab_indexes[tab_name] - 2].y = temp_items?.length ?? 0;
                        }}
                    }}
                }});
            }}
            let page = 1;
            let onfocused = false;

            function showListModal(event) {{
                event.stopPropagation()
                if (event.pointerType == '') return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
            }}
            function toggleListModal(event, from_html = false) {{
                event.stopPropagation()

                if (from_html && !$('.arbitrary-keys').hasClass('show')) return;
                //if (['path', 'svg'].includes(event.target.tagName)) return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
                else {{
                    $('.arbitrary-keys').removeClass('show')
                    $('.filter-search-arbitrary .input').removeClass('selected')
                    onfocused = false;
                }}
            }}
            function closeModal(event) {{
                event?.stopPropagation()
                if (onfocused) {{
                    setTimeout(() => {{
                        $('.arbitrary-keys').removeClass('show')
                        $('.filter-search-arbitrary .input').removeClass('selected')
                        event?.target?.blur()
                    }}, 100);
                    onfocused = false;
                }}
            }}

            let filters = {{
                    2: {{ {filters.get("free_kwds")} }}, 
                    3: {{ {filters.get("neg_kwds")} }}, 
                    4: {{ {filters.get("rep_kwds")} }}, 
                    5: {{ {filters.get("rel_kwds")} }},
                    6: {{ {filters.get("soc_kwds")} }},
                    7: {{ {filters.get("doc_kwds")} }},
                    8: {{ {filters.get("free_kwds")} }}, 
                }}

            let social_types = {{
                'Вконтакте': true,
                'Facebook': true,
                'Одноклассники': true,
                'Instagram': true,
                'Telegram': true,
            }}
            let document_types = {{
                'PDF': true,
                'Word': true,
                'Excel': true,
                'PowerPoint': true,
                'Txt': true,
            }}

            let social_type_counts = {{
                'Вконтакте': 0,
                'Facebook': 0,
                'Одноклассники': 0,
                'Instagram': 0,
                'Telegram': 0,
            }}
            let document_type_counts = {{
                'PDF': 0,
                'Word': 0,
                'Excel': 0,
                'PowerPoint': 0,
                'Txt': 0,
            }}
            let filter_counts = {{
            }}

            console.log('items', items)

            function makeSafeForCSS(name) {{
                return name.replace(/[^a-z0-9]/g, function (s) {{
                    var c = s.charCodeAt(0);
                    if (c == 32) return '-';
                    if (c >= 65 && c <= 90) return '_' + s.toLowerCase();
                    return '__' + ('000' + c.toString(16)).slice(-4);
                }});
            }}

            let temp_link_classes = {{}};
            let seen_links = {{}};

            const decode_filter_classes = Object.entries(filters).reduce((prev, next) => ({{
                ...prev, [next[0]]: {{
                    ...(Object.keys(next[1]).reduce((_prev, key) => ({{
                        ..._prev,
                        [makeSafeForCSS(key)]: key
                    }}), {{}}))
                }}
            }}), {{}})

            function filter() {{
                updateList({{ target: {{ value: '' }} }})
                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            function uncheckAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = false;
                }});
                filter()
            }}

            function checkAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = true;
                }});
                filter()
            }}

            function toggleArbitraryKey(event, key_name) {{
                if (event.ctrlKey) {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = false;
                        $(`.keyword-id-${{makeSafeForCSS(arbitrary_key)}} input`).checked = false;
                    }});
                }}
                let decode_base_64 = decode_filter_classes[selected_tab_index][key_name];
                filters[selected_tab_index][decode_base_64] = !filters[selected_tab_index][decode_base_64]
                $(`.keyword-id-${{key_name}} input`).checked = filters[selected_tab_index][decode_base_64];

                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            String.prototype.lowerIncludes = function (string) {{
                return this.toLowerCase().includes(string.toLowerCase())
            }}
            String.prototype.maxLength = function (max_length) {{
                if (this?.length > max_length) return this.slice(0, max_length) + '...';
                else return this;
            }}

            function updateList(event) {{

                let filter_keys_tags = ``

                let temp_keys = Object.keys(filters[selected_tab_index]).filter(key_name => key_name?.lowerIncludes(event.target.value));

                temp_keys.sort((a, b) => {{
                    if (a?.lowerIncludes(event.target.value) == false && b?.lowerIncludes(event.target.value) == false) {{
                        return 0
                    }}
                    else if (a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value)) {{
                        return a?.indexOf(event.target.value) < b?.indexOf(event.target.value) ? -1 : 0
                    }}
                    else {{
                        return a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value) == false ? -1 : 0
                    }}
                }});

                temp_keys.forEach(arbitrary_key => {{
                    filter_keys_tags += `
                                    <label style="${{filter_counts[selected_tab_index][arbitrary_key] == undefined ? 'display:none' : ''}}" class="arbitrary-key keyword-id-${{makeSafeForCSS(arbitrary_key)}}">
                                        <input type="checkbox" onclick="toggleArbitraryKey(event, '${{makeSafeForCSS(arbitrary_key)}}')" ${{filters[selected_tab_index][arbitrary_key] ? 'checked' : 'unchecked'}}/>
                                        <span style="margin-right: 4px;" title='${{arbitrary_key}}'>${{arbitrary_key}}</span>
                                        <div class="filter-count">${{filter_counts[selected_tab_index][arbitrary_key] ?? 0}}</div>
                                    </label>
                                `;
                }});

                $('.filter-search-arbitrary .arbitrary-keys').innerHTML = `<div>` + filter_keys_tags + `</div>
                        <div class="filter-btns">
                            <span onclick="checkAll()">Выделить все</span>
                            <span onclick="uncheckAll()">Снять выделение</span>
                        </div>
                        ${{isMobile ? '' : `
                            <div class="filter-info">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
                                <div class="filter-info_prompt">Выделить только один<br/> через Ctrl + Click</div>
                            </div>
                        `}}
                    `
            }}

            let temp_pagination_count = 1;

            function get_domain_name(url) {{
                let a = document.createElement('a')
                a.href = url;
                return a.hostname;
            }}

            function isInViewport(el) {{
                const rect = el.getBoundingClientRect();

                var isinview = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)

                );

                return isinview;
            }}

            function check_all_items() {{
                Object.keys(temp_link_classes).forEach(link_class_name => {{
                    let bool = isInViewport($('#' + link_class_name))
                    if (bool) {{
                        seen_links[temp_link_classes[link_class_name]] = true;
                        let temp_svg = $(`#${{link_class_name}} .checkmark.unseen`);
                        if (temp_svg) temp_svg.addClass('seen_scale');
                        setTimeout(() => {{
                            if (temp_svg?.style?.display != undefined) temp_svg.style.display = 'none';
                        }}, 1100);
                    }}
                }})
            }}

            function update_fullname_data(tab_name) {{
                $(`input[name="fullname"]`).forEach(radio => {{
                    radio.checked = false;
                }})
                $(`input[name="fullname"]`)[fullname_filter[tab_name]].checked = true
                fullname_data[tab_name].forEach((count, i) => {{
                    $(`#fullname-${{i}}`).innerHTML = '&nbsp;' + (count ?? 0);
                }});
            }}

            function update_fullname_filter(event) {{
                let tab_name = tab_names[selected_tab_index];
                fullname_filter[tab_name] = event?.target?.value ?? 0;
                render_items(false, true)
            }}
            function update_social_type_counts(temp_items, type = 'socials') {{
                if (type == 'socials') {{
                    social_type_counts = {{
                        'Вконтакте': 0,
                        'Facebook': 0,
                        'Одноклассники': 0,
                        'Instagram': 0,
                        'Telegram': 0,
                    }}
                    temp_items.forEach(item => {{
                        social_type_counts[item.social_type]++;
                    }})
                }}
                else if (type == 'doc') {{
                    document_type_counts = {{
                        'PDF': 0,
                        'Word': 0,
                        'Excel': 0,
                        'PowerPoint': 0,
                        'Txt': 0,
                    }}
                    temp_items.forEach(item => {{
                        document_type_counts[item.doc_type]++;
                    }})
                    console.log('document_type_counts', document_type_counts);
                }}
                $(`.${{type}}_type-info`).forEach(temp_type => {{
                    temp_type.querySelector('span').innerText = (type == 'socials' ? social_type_counts : document_type_counts)[temp_type.dataset[type == 'socials' ? 'socialName' : 'documentName']]
                }})
            }}
            update_social_type_counts(items['socials'], 'socials')
            update_social_type_counts(items['documents'], 'doc')

            $('.socials_type-info').forEach(social_type => {{
                social_type.addEventListener('click', (event) => {{
                    if (event.ctrlKey) {{
                        $('.socials_type-info').forEach(sub_social_type => {{
                            sub_social_type.firstElementChild.removeClass('selected')
                            social_types[sub_social_type.dataset.socialName] = false;
                        }})
                    }}
                    if (social_type.firstElementChild.hasClass('selected')) {{
                        social_type.firstElementChild.removeClass('selected')
                        social_types[social_type.dataset.socialName] = false;
                    }}
                    else {{
                        social_type.firstElementChild.addClass('selected')
                        social_types[social_type.dataset.socialName] = true;
                    }}
                    render_items(true)
                }})
            }})
            $('.doc_type-info').forEach(social_type => {{
                social_type.addEventListener('click', (event) => {{
                    if (event.ctrlKey) {{
                        $('.doc_type-info').forEach(sub_social_type => {{
                            sub_social_type.firstElementChild.removeClass('selected')
                            document_types[sub_social_type.dataset.documentName] = false;
                        }})
                    }}
                    if (social_type.firstElementChild.hasClass('selected')) {{
                        social_type.firstElementChild.removeClass('selected')
                        document_types[social_type.dataset.documentName] = false;
                    }}
                    else {{
                        social_type.firstElementChild.addClass('selected')
                        document_types[social_type.dataset.documentName] = true;
                    }}
                    render_items(true)
                }})
            }})

            const minus_social_resources = [
                'sociumin.com',
                'socialbase.ru',
                'sociuminfo.com',
                'vkanketa.ru',
                'namebook.club',
                'bigbookname.com',
                'vk.watch',
                'vkplaneta.ru',
            ];

            function render_items(update_social_type = false, update_social_type_count = false) {{
                    let result = ``;
                    let tab_name = tab_names[selected_tab_index];


                    let temp_items = [...items[tab_name]];

                    // fullname_data
                    // fullname_filter

                    let fullname = fullname_filter[tab_name] ?? 0;

                    const minus_social_resources_chbox = $('#minus-social-resources').checked;

                    if (minus_social_resources_chbox) {{
                        fullname_data[tab_name] = [0,0,0];
                        temp_items = temp_items.filter(item => {{
                            let bool = !minus_social_resources.some(social_resource => item.link.toLowerCase().includes(social_resource));

                            if (bool) {{
                                if (item.fullname) {{
                                    fullname_data[tab_name][1]++
                                }}
                                else {{
                                    fullname_data[tab_name][2]++
                                }}
                                fullname_data[tab_name][0]++
                            }}

                            return bool
                        }})
                    }}


                    if (minus_keywords.length) {{
                        fullname_data[tab_name] = [0, 0, 0];
                        temp_items = temp_items.filter(item => {{
                            let bool = !minus_keywords.some(minus_keyword => (item.title.toLowerCase().includes(minus_keyword) || item.link.toLowerCase().includes(minus_keyword) || item.content.toLowerCase().includes(minus_keyword)));

                            if (bool) {{
                                if (item.fullname) {{
                                    fullname_data[tab_name][1]++
                                }}
                                else {{
                                    fullname_data[tab_name][2]++
                                }}
                                fullname_data[tab_name][0]++
                            }}

                            return bool
                        }})
                    }}

                    update_fullname_data(tab_name);


                if ([1, 2].includes(+fullname)) {{
                    temp_items = temp_items.filter(item => (item.fullname == {{ 1: true, 2: false }}[fullname]))
                }}
                $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;

                if (update_social_type_count) update_social_type_counts(temp_items, tab_name == 'socials' ? tab_name : 'doc')

                if (isFilterableTab()) {{
                    if (tab_name == 'socials') {{
                        temp_items = temp_items.filter(item => (social_types[item?.social_type]))
                    }}
                    else if (tab_name == 'documents') {{
                        temp_items = temp_items.filter(item => (document_types[item?.doc_type]))
                    }}

                    if (update_social_type) {{
                        filter_counts[selected_tab_index] = {{}};
                        temp_items.forEach(item => {{
                            item.keyword_list.forEach(keyword => {{
                                if (!filter_counts[selected_tab_index][keyword]) {{
                                    filter_counts[selected_tab_index][keyword] = 0;
                                }}
                                filter_counts[selected_tab_index][keyword]++;
                            }});
                        }})
                        updateList({{ target: {{ value: '' }} }})
                    }}

                    temp_items = temp_items.filter(item => (item.keyword_list.find(keyword => filters[selected_tab_index][keyword])))

                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}
                else if (tab_name == 'main') {{
                    temp_items = temp_items.filter(item => (+(item?.keyword_list?.length ?? 0) >= startRangeValue && +(item?.keyword_list?.length ?? 0) <= endRangeValue))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}

                temp_pagination_count = Math.ceil(temp_items?.length / range) || 1;

                if (tab_pages[tab_name].page > temp_pagination_count) tab_pages[tab_name].page = temp_pagination_count;


                let sliced_items = JSON.parse(JSON.stringify(
                    temp_items.slice((tab_pages[tab_name].page - 1) * range, tab_pages[tab_name].page * range)
                ));

                if (isFilterableTab()) {{
                    sliced_items.forEach(sliced_item => {{
                        sliced_item.keyword_list = sliced_item.keyword_list.filter(keyword => filters[selected_tab_index][keyword])
                    }});
                }}

                temp_link_classes = {{}};

                sliced_items.forEach(item => {{

                    let keyword_list = ``
                    item?.keyword_list.forEach(query => {{
                        if (keyword_list) keyword_list += '<span style="color:black;font-size:17px">, </span>'
                        keyword_list += `<span
                                        class="query"
                                        onclick="copy(this)">${{decodeURI(query.trim())}}</span>`
                    }})

                    // Вес ссылки
                    // Похожие

                    let temp_link_class = makeSafeForCSS(item?.link);

                    temp_link_classes[temp_link_class] = item?.link;

                    result += `
                                <div class="item-container ${{seen_links[item?.link] ? 'seen_link' : ''}}" id="${{temp_link_class}}">
                                    <div class="item" style="position:relative">
                                        ${{seen_links[item?.link] ? '<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>' : '<svg class="checkmark unseen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"></circle></svg>'}}

                                        <div class="flex items-center">
                                            <a target="_blank" href="${{item?.link}}" class="item-title" title="${{item?.title}}">${{item?.title}}</a>
                                            <!-- <a target="_blank" href="${{item?.link}}" class="item-more">Источник <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M320 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h82.7L201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L448 109.3V192c0 17.7 14.3 32 32 32s32-14.3 32-32V32c0-17.7-14.3-32-32-32H320zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg></a> -->
                                        </div>
                                        <div class="item-content">${{item?.content}}</div>
                                        <div class="item-info" style="display:flex;align-items:center;margin-top:5px;font-size:12px;">
                                            <a href="${{item?.link}}" target="_blank" style="color: #4d4dff;" title="${{get_domain_name(item?.link)}}">${{get_domain_name(item?.link).maxLength(20)}}</a>

                                            <span style="margin: 0 .8em;white-space:nowrap;display:flex;align-items:center;cursor:default;" title="Вес ссылки: найдено ${{item?.keyword_list?.length ?? 0}} раз">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="max-width:12px;min-width:12px;"
                                                    viewBox="0 0 512 512">
                                                    <path
                                                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                                                </svg>
                                                <span style="margin-left:5px;font-size:12px;">${{item?.keyword_list?.length ?? 0}}</span>
                                            </span>

                                            <div class="mt-auto item-keywords">
                                                <div class="item-param"><div class="query-content" title='${{decodeURI(item?.keyword_list?.join(',  '))}}'><span style="color:black">
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:12px;fill:#9300FF;margin-bottom: -2.1px;"><path d="M336 352c97.2 0 176-78.8 176-176S433.2 0 336 0S160 78.8 160 176c0 18.7 2.9 36.8 8.3 53.7L7 391c-4.5 4.5-7 10.6-7 17v80c0 13.3 10.7 24 24 24h80c13.3 0 24-10.7 24-24V448h40c13.3 0 24-10.7 24-24V384h40c6.4 0 12.5-2.5 17-7l33.3-33.3c16.9 5.4 35 8.3 53.7 8.3zM376 96a40 40 0 1 1 0 80 40 40 0 1 1 0-80z"/></svg> </span>${{keyword_list}}
                                                    <small class="prompt">Копировать при клике</small></div>
                                                </div>
                                                <!-- <div class="item-param">Дубликаты: <span class="param-text">${{item?.link_weight}}</span></div> -->
                                                <!-- <div class="item-param">Фигурирует в списках: <span class="param-text">${{item?.has_in_list}}</span></div> -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                }});

                if (items[tab_name].length) {{
                    $(`.tab-content-${{tab_indexes[tab_name]}}`).innerHTML = result
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'flex'
                    }});
                }}
                else {{
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'none'
                    }});
                }}

                update_pagination()
                check_all_items()

            }}

            function update_pagination() {{
                let tab_name = tab_names[selected_tab_index];
                let start_page = 1

                if (tab_pages[tab_name].page > 5) start_page = tab_pages[tab_name].page - 5;

                let page_tags = ``

                for (let i = start_page; i <= ((start_page + 9) <= temp_pagination_count ? start_page + 9 : temp_pagination_count); i++) {{
                    page_tags += `<span onclick="set_page('${{tab_names[selected_tab_index]}}', ${{i}})" ${{tab_pages[tab_name].page == i ? 'class="selected"' : ''}}>${{i}}</span>`
                }}
                $(`.pagination`).html(`
                        <div class="flex hovered-angle">
                            <svg class="first-page" onclick="first_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                            </svg>
                            <svg onclick="minus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z" />
                            </svg>
                        </div>
                        <div class="flex h-full scrollbar">
                            ${{page_tags}}
                        </div>
                        <div class="flex hovered-angle">
                            <svg onclick="plus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
                            </svg>
                            <svg class="last-page" onclick="last_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                            </svg>
                        </div>
                    `);
            }}

            render_items()

            window.onscroll = function (event) {{

                check_all_items();
            }}

            update_global_counts()



            const colors = Highcharts.getOptions().colors.map((c, i) =>
                // Start out with a darkened base color (negative brighten), and end
                // up with a much brighter color
                Highcharts.color(Highcharts.getOptions().colors[0])
                    .brighten((i - 3) / 7)
                    .get()
            );
            // Data retrieved from https://netmarketshare.com/
            // Build the chart
            Highcharts.chart('container', {{
                chart: {{
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie',
                }},
                credits: false,
                title: {{
                    text: `<div style="text-align: center;line-height: 1.6"><b style="font-size:35px">${{Object.values(seriesData).reduce((prev, next) => (prev + next.y), 0)}}</b><br><span style="font-size:16px;color: #ccc">материалов</span></div>`,
                    useHTML: true,
                    align: 'center',
                    verticalAlign: 'middle',
                    y: 15,
                    x: -100,
                }},
                legend: {{
                    align: 'right',
                    verticalAlign: 'middle',
                    layout: 'vertical',
                    x: 0,
                    useHTML: true,
                    labelFormat: `<div style="display:flex;width: 150px"><span>{{name}}</span> <div style="margin-left:auto;font-weight:600;">{{y}}</div></div>`, // : {{y}} | {{percentage:.1f}}%
                }},
                tooltip: {{
                    pointFormat: '{{point.name}}: <b>{{point.percentage:.1f}}%</b>',
                    headerFormat: ''
                }},
                accessibility: {{
                    point: {{
                        valueSuffix: '%'
                    }}
                }},
                plotOptions: {{
                    pie: {{
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {{
                            enabled: false,
                        }},
                        colors,
                        showInLegend: true,
                        // tooltip: {{
                        //     footerFormat: ''
                        // }}
                    }}
                }},
                series: [{{
                    // name: ' ',
                    colorByPoint: true,
                    innerSize: '80%',
                    // dataLabels: {{
                    //     formatter: function() {{
                    //         return this.point.name; //<--------------- If the slice has a value greater than 5 show it.
                    //     }},
                    //     // color: '#ffffff',
                    //     // distance: -30
                    // }},
                    data: seriesData,
                }}]
            }})
            const first_tab_index = (Object.values(items).findIndex(item_values => item_values.length) || 0) + 1; 

            // if (first_tab_index != 1) {{ 
            //     $('.tab-1').style.display = 'none'; 
            // }}

            select_tab(first_tab_index);
        </script>
    </body>

    </html>
"""

    return report_html


def response_num_template(title, items, filters, lampyre_html, tags, osint_html) -> str:
    report_html = f"""<!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            {NUM_STYLE}
        </head>

        <body>
        <div class="tab-head" onclick="closeModal(event)">
            <div class="flex items-center" style="flex-wrap: wrap;">
                <h2 class="object-full_name">Номер: <span style="white-space:nowrap">{title}</span></h2>
            </div>

            <div class=" tabs flex flex-wrap items-center">
                <div class="tab-1 selected" onclick="select_tab(1)">
                    Упоминания
                    <span class="tab-count">0</span>
                </div>
                <div class="tab-2" onclick="select_tab(2)"> 
                    Теги 
                    <span class="tab-count" style="display: none;">0</span> 
                </div> 
                <div class="tab-3" onclick="select_tab(3)"> 
                    Аккаунты 
                    <span class="tab-count" style="display: none;">0</span> 
                </div>
            </div>
        </div>

        <div class="flex items-center wrap-reverse-container only-for-mentions" style="padding: 0 10px;">
            <div class="similars-range" style="padding-left: 20px;display: none;">
                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="position:absolute;left:5px;top:4px;"
                    viewBox="0 0 512 512">
                    <path
                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                </svg>
                <div slider id="slider-distance">
                    <div>
                        <div inverse-left style="width:100%;"></div>
                        <div inverse-right style="width:100%;"></div>
                        <div range style="left:0%;right:0%;"></div>
                        <span thumb style="left:0%;"></span>
                        <span thumb style="left:100%;"></span>
                        <div sign style="left:0%;">
                            <span id="value">0</span>
                        </div>
                        <div sign style="left:100%;">
                            <span id="value">100</span>
                        </div>
                    </div>
                    <input id="startRangeValue" type="range" tabindex="0" value="0" max="100" min="0" step="1"
                        onchange="update_startRangeValue(+event.target.value)" oninput="startRange(event)" />

                    <input id="endRangeValue" type="range" tabindex="0" value="100" max="100" min="0" step="1"
                        onchange="update_endRangeValue(+event.target.value)" oninput="endRange(event)" />
                </div>
            </div>
            <div class="filter-search-arbitrary" style="display: none;">
                <label class="input">
                    <!-- Введите название произвольного ключа -->
                    <input type="text" placeholder="Введите название ключа" onclick="showListModal(event)"
                        oninput="updateList(event)" />
                    <svg onclick="toggleListModal(event)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                        <path
                            d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
                    </svg>
                    <div class="arbitrary-keys" onclick="showListModal(event)">
                    </div>
                </label>
            </div>
            <div class="pagination-container" onclick="closeModal(event)">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <div class="content" onclick="closeModal(event)">
            <div class="tab-content-1 selected">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Нет найденных результатов!
                </div>
            </div>
            <div class="tab-content-2" style="overflow-x: scroll;min-height: calc(100vh - 103px);">
                <div>
                    <div class="leaks" id="tags" style="margin-bottom: 15px;margin-left:10px;"> 
                        <div class="leak-description"><span class="f-w-600">Теги из популярных мобильных приложений определения звонящего: </span></div> 
                        <div class="flex"> 
                            <!-- Leaks --> 
                        </div> 

                    </div> 
                    <script> 
                        let start_tags = {tags};

                        let tags = {{}};

                        start_tags.forEach(tag => {{
                            if (tags[tag]) {{
                                tags[tag].count++;
                            }}
                            else {{
                                tags[tag] = {{
                                    name: tag,
                                    count: 1
                                }}
                            }}
                        }})

                        tags = Object.values(tags)

                        tags.sort((a,b) => (b.count - a.count))

                        console.log(tags)

                        if (tags.length) {{ 
                            let tags_container = document.querySelector('#tags .flex'); 
                            let leak_tags = '<div class="flex flex-col">'; 

                            console.log('tags_container', tags_container); 

                            let per_col = Math.ceil(tags.length ** .65) + 1; 

                            console.log('per_col', per_col);

                            per_col = Math.ceil(((tags.length) / per_col) > 5 ? (tags.length) / 5 : per_col); 
                            console.log('per_col', per_col);

                            console.log('per_col', per_col); 

                            tags.forEach((tag, i) => {{ 
                                if (((i) % per_col) == 0 && i != 0) {{ 
                                    leak_tags += `</div>`; 
                                    if (i != (tags.length - 1)) leak_tags += `<div class="flex flex-col">`; 
                                }} 
                                    leak_tags += `<span class="leak" style="position: relative;">${{tag.name}}${{tag.count == 1 ? '' : `<div class="tag-repeated-count">${{tag.count}}</div>`}}</span>`; 

                                if (i == (tags.length - 1) || ((i + 1) / per_col) == 5) {{ 
                                    leak_tags += `</div>`; 
                                }}
                            }}) 


                            tags_container.innerHTML += leak_tags; 
                        }} 
                        else {{ 
                            document.querySelector('#tags .leak-description .f-w-600').textContent = 'Нет тегов из популярных мобильных приложений' 
                            document.querySelector('#tags .flex').innerHTML = '...' 
                        }} 
                    </script>
                </div>
            </div>
            <div class="tab-content-3">
                <table style="border-radius: 7px;overflow: hidden;margin-right: auto;margin-left: auto;outline: 1px solid #a7a3a3;margin-bottom: 15px;"
                    cellspacing="0">
                    <tbody style="margin: 5px 8px;">
                        <tr style="">
                            <th
                                style="width: 250px;height: 45px;background: #c4d9ce;border-right: 1px solid #939393;border-bottom: 1px solid #939393;">
                                Проверка</th>
                            <th style="/* width: 100px; */height: 45px;background: #c4d9ce;border-bottom: 1px solid #939393;">Результат</th>
                        </tr>
                        {osint_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="flex only-for-mentions" onclick="closeModal(event)">
            <div class="pagination-container" style="padding: 0 7.5px 15px;">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let startRangeValue = 0;
            let endRangeValue = 0;

            function update_startRangeValue(value) {{
                startRangeValue = value;
                render_items()
            }}
            function update_endRangeValue(value) {{
                endRangeValue = value;
                render_items()
            }}

            const startRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.min($this.value, $this.parentNode.childNodes[5].value - 1);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[1].style.width = value + '%';
                children[5].style.left = value + '%';
                children[7].style.left = value + '%'; children[11].style.left = value + '%';
                children[11].childNodes[1].innerHTML = $this.value;
            }}
            const endRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.max($this.value, $this.parentNode.childNodes[3].value);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[3].style.width = (100 - value) + '%';
                children[5].style.right = (100 - value) + '%';
                children[9].style.left = value + '%'; children[13].style.left = value + '%';
                children[13].childNodes[1].innerHTML = $this.value;
            }}

            const isMobile = Boolean(navigator.userAgent.match(/Android/i)
                || navigator.userAgent.match(/webOS/i)
                || navigator.userAgent.match(/iPhone/i)
                || navigator.userAgent.match(/iPad/i)
                || navigator.userAgent.match(/iPod/i)
                || navigator.userAgent.match(/BlackBerry/i)
                || navigator.userAgent.match(/Windows Phone/i));

            console.log('isMobile', isMobile, navigator.userAgent);

            let selected_tab_index = 1
            function $(str) {{
                let elements = document?.querySelectorAll(str);

                return (elements?.length == 1) ? document?.querySelector(str) : elements;
            }}
            Object.prototype.html = function (html) {{
                this?.forEach(item => {{
                    item.innerHTML = html
                }});
            }}
            Object.prototype.hasClass = function (className) {{
                return this?.classList?.contains(className)
            }}
            Object.prototype.addClass = function (className) {{
                this?.classList?.add(className)
            }}
            Object.prototype.removeClass = function (className) {{
                this?.classList?.remove(className)
            }}

            let filterable_tabs = [1, 2, 3, 4, 5, 6]
            const items = {{
                main: [{items.get("all")}]
            }}

            endRangeValue = []
            items.main.forEach(item => {{
                endRangeValue.push(+item.link_weight)
            }});
            startRangeValue = endRangeValue.length ? Math.min(...endRangeValue) : 0
            endRangeValue = endRangeValue.length ? Math.max(...endRangeValue) : 0

            let endRangeElement = $('#endRangeValue');
            let startRangeElement = $('#startRangeValue');
            startRangeElement.min = endRangeElement.min = startRangeElement.value = startRangeValue;
            startRangeElement.max = endRangeElement.max = endRangeElement.value = endRangeValue;
            startRange({{ target: startRangeElement }})
            endRange({{ target: endRangeElement }})


            const tab_names = {{
                1: 'main',
                2: 'arbitrary',
                3: 'negative',
                4: 'reputation',
                5: 'connections',
                6: 'socials',
                7: 'all_materials',
            }}

            function isFilterableTab() {{
                return filterable_tabs.find(filterable_tab => filterable_tab == selected_tab_index) != undefined
            }}
            function select_tab(new_tab_index) {{
                if (selected_tab_index == new_tab_index) return

                $(`.tab-${{new_tab_index}}`)?.addClass('selected')
                $(`.tab-content-${{new_tab_index}}`)?.addClass('selected')

                $(`.tab-${{selected_tab_index}}`)?.removeClass('selected')
                $(`.tab-content-${{selected_tab_index}}`)?.removeClass('selected')

                selected_tab_index = new_tab_index
                if (new_tab_index != 1) {{
                    $('.only-for-mentions').forEach(el => {{
                        el.style.display = 'none';
                    }})
                    return;
                }}
                else {{
                    $('.only-for-mentions').forEach(el => {{
                        el.style.display = '';
                    }})
                }}
                render_items()
                let tab_name = tab_names[selected_tab_index];

                // if (isFilterableTab() && items[tab_names[selected_tab_index]]?.length > 0) {{

                //     updateList({{ target: {{ value: '' }} }})
                //     $(`.filter-search-arbitrary`).style.display = 'block';
                // }}
                // else {{
                //     $(`.filter-search-arbitrary`).style.display = 'none';
                // }}
                // $(`.similars-range`).style.display = new_tab_index == 1 ? 'block' : 'none';
            }}
            function copy(that) {{
                var inp = document.createElement('input');
                document.body.appendChild(inp)
                inp.value = that.textContent
                inp.select();
                document.execCommand('copy', false);
                inp.remove();
            }}
            const tab_indexes = {{
                main: 1,
                arbitrary: 2,
                negative: 3,
                reputation: 4,
                connections: 5,
                socials: 6,
                all_materials: 7,
            }}

            Object.entries(tab_indexes).forEach(([tab_name, tab_index]) => {{
                $(`.tab-${{tab_index}} .tab-count`).innerHTML = items[tab_name]?.length
            }});
            const tab_pages = {{
                main: {{
                    count: 0,
                    page: 1,
                }},
                arbitrary: {{
                    count: 0,
                    page: 1,
                }},
                negative: {{
                    count: 0,
                    page: 1,
                }},
                reputation: {{
                    count: 0,
                    page: 1,
                }},
                connections: {{
                    count: 0,
                    page: 1,
                }},
                socials: {{
                    count: 0,
                    page: 1,
                }},
                all_materials: {{
                    count: 0,
                    page: 1,
                }},
            }}

            function set_page(tab_name, page) {{
                tab_pages[tab_name].page = page;
                render_items()
                update_pagination()
            }}
            function minus_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page -= 1;
                render_items()
                update_pagination()
            }}
            function first_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page = 1;
                render_items()
                update_pagination()
            }}
            function plus_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page += 1;
                render_items()
                update_pagination()
            }}
            function last_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page = tab_pages[tab_name].count;
                render_items()
                update_pagination()
            }}

            const range = 20;

            Object.keys(items).forEach(tab_name => {{
                    if (items[tab_name]?.length) tab_pages[tab_name].count = Math.ceil(items[tab_name]?.length / range);
                }});

            let page = 1;
            let onfocused = false;

            function showListModal(event) {{
                event.stopPropagation()
                if (event.pointerType == '') return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
            }}
            function toggleListModal(event) {{
                event.stopPropagation()
                //if (['path', 'svg'].includes(event.target.tagName)) return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
                else {{
                    $('.arbitrary-keys').removeClass('show')
                    $('.filter-search-arbitrary .input').removeClass('selected')
                    onfocused = false;
                }}
            }}
            function closeModal(event) {{
                event?.stopPropagation()
                if (onfocused) {{
                    setTimeout(() => {{
                        $('.arbitrary-keys').removeClass('show')
                        $('.filter-search-arbitrary .input').removeClass('selected')
                        event?.target?.blur()
                    }}, 100);
                    onfocused = false;
                }}
            }}

            let filters = {{
                    1: {{ {filters.get("free_kwds")} }},
                    }}

            function makeSafeForCSS(name) {{
                return name.replace(/[^a-z0-9]/g, function (s) {{
                    var c = s.charCodeAt(0);
                    if (c == 32) return '-';
                    if (c >= 65 && c <= 90) return '_' + s.toLowerCase();
                    return '__' + ('000' + c.toString(16)).slice(-4);
                }});
            }}

            let temp_link_classes = {{}};
            let seen_links = {{}};

            const decode_filter_classes = Object.entries(filters).reduce((prev,next) => ({{ ...prev, [next[0]]: {{
                ...(Object.keys(next[1]).reduce((_prev, key) => ({{
                    ..._prev,
                    [makeSafeForCSS(key)]: key
                }}), {{}}))
            }} }}), {{}})

            function filter() {{
                updateList({{ target: {{ value: '' }} }})
                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            function uncheckAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = false;
                }});
                filter()
            }}

            function checkAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = true;
                }});
                filter()
            }}

            function toggleArbitraryKey(event, key_name) {{
                if (event.ctrlKey) {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = false;
                        $(`.keyword-id-${{makeSafeForCSS(arbitrary_key)}} input`).checked = false;
                    }});
                }}
                let decode_base_64 = decode_filter_classes[selected_tab_index][key_name];
                console.log('decode_base_64', decode_base_64);
                filters[selected_tab_index][decode_base_64] = !filters[selected_tab_index][decode_base_64]
                $(`.keyword-id-${{key_name}} input`).checked = filters[selected_tab_index][decode_base_64];

                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            String.prototype.lowerIncludes = function (string) {{
                return this.toLowerCase().includes(string.toLowerCase())
            }}
            String.prototype.maxLength = function (max_length) {{
                if (this?.length > max_length) return this.slice(0,max_length) + '...';
                else return this;
            }}

            function updateList(event) {{

                let filter_keys_tags = ``

                let temp_keys = Object.keys(filters[selected_tab_index]).filter(key_name => key_name?.lowerIncludes(event.target.value));

                temp_keys.sort((a, b) => {{
                    if (a?.lowerIncludes(event.target.value) == false && b?.lowerIncludes(event.target.value) == false) {{
                        return 0
                    }}
                    else if (a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value)) {{
                        return a?.indexOf(event.target.value) < b?.indexOf(event.target.value) ? -1 : 0
                    }}
                    else {{
                        return a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value) == false ? -1 : 0
                    }}
                }});

                temp_keys.forEach(arbitrary_key => {{
                    filter_keys_tags += `
                                <label class="arbitrary-key keyword-id-${{makeSafeForCSS(arbitrary_key)}}">
                                    <input type="checkbox" onclick="toggleArbitraryKey(event, '${{makeSafeForCSS(arbitrary_key)}}')" ${{filters[selected_tab_index][arbitrary_key] ? 'checked' : 'unchecked'}}/>
                                    <span title='${{arbitrary_key}}'>${{arbitrary_key}}</span>
                                </label>
                            `;
                }});

                $('.filter-search-arbitrary .arbitrary-keys').innerHTML = `<div>` + filter_keys_tags + `</div>
                    <div class="filter-btns">
                        <span onclick="checkAll()">Выделить все</span>
                        <span onclick="uncheckAll()">Снять выделение</span>
                    </div>
                    ${{isMobile ? '' : `
                        <div class="filter-info">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
                            <div class="filter-info_prompt">Выделить только один<br/> через Ctrl + Click</div>
                        </div>
                    `}}
                `
            }}

            updateList({{ target: {{ value: '' }} }})
            let temp_pagination_count = 1;

            function get_domain_name(url) {{
                let a = document.createElement('a')
                a.href = url;
                return a.hostname;
            }}

            function isInViewport(el) {{
                const rect = el.getBoundingClientRect();

                var isinview = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)

                );

                return isinview;
            }}

            function check_all_items() {{
                Object.keys(temp_link_classes).forEach(link_class_name => {{
                    let bool = isInViewport($('#'+link_class_name))
                    if (bool) {{
                        seen_links[temp_link_classes[link_class_name]] = true;
                        let temp_svg = $(`#${{link_class_name}} .checkmark.unseen`);
                        if (temp_svg) temp_svg.addClass('seen_scale');
                        setTimeout(() => {{
                            if (temp_svg?.style?.display != undefined) temp_svg.style.display = 'none';
                        }}, 1100);
                    }}
                }})
            }}

            function render_items() {{
                let result = ``;
                let tab_name = tab_names[selected_tab_index];

                let temp_items = [...items[tab_name]];

                if (isFilterableTab()) {{
                    temp_items = temp_items.filter(item => (item.keyword_list.find(keyword => filters[selected_tab_index][keyword])))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}
                else if (tab_name == 'main') {{
                    temp_items = temp_items.filter(item => (+item.link_weight >= startRangeValue && +item.link_weight <= endRangeValue))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}

                temp_pagination_count = Math.ceil(temp_items?.length / range) || 1;

                if (tab_pages[tab_name].page > temp_pagination_count) tab_pages[tab_name].page = temp_pagination_count;

                let sliced_items = JSON.parse(JSON.stringify(
                    temp_items.slice((tab_pages[tab_name].page - 1) * range, tab_pages[tab_name].page * range)
                ));

                if (isFilterableTab()) {{
                    sliced_items.forEach(sliced_item => {{
                        sliced_item.keyword_list = sliced_item.keyword_list.filter(keyword => filters[selected_tab_index][keyword])
                    }});
                }}

                temp_link_classes = {{}};

                sliced_items.forEach(item => {{

                    let keyword_list = ``
                    item?.keyword_list.forEach(query => {{
                        if (keyword_list) keyword_list += '<span style="color:black;font-size:17px">, </span>'
                        keyword_list += `<span
                                    class="query"
                                    onclick="copy(this)">
                                    ${{decodeURI(query)}}
                                </span>`
                    }})

                    // Вес ссылки
                    // Похожие

                    let temp_link_class = makeSafeForCSS(item?.link);

                    temp_link_classes[temp_link_class] = item?.link;

                    result += `
                            <div class="item-container ${{seen_links[item?.link] ? 'seen_link' : ''}}" id="${{temp_link_class}}">
                                <div class="item" style="position:relative">
                                    ${{seen_links[item?.link] ? '<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>' : '<svg class="checkmark unseen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"></circle></svg>'}}

                                    <div class="flex items-center">
                                        <a target="_blank" href="${{item?.link}}" class="item-title" title="${{item?.title}}">${{item?.title}}</a>
                                        <!-- <a target="_blank" href="${{item?.link}}" class="item-more">Источник <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M320 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h82.7L201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L448 109.3V192c0 17.7 14.3 32 32 32s32-14.3 32-32V32c0-17.7-14.3-32-32-32H320zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg></a> -->
                                    </div>
                                    <div class="item-content">${{item?.content}}</div>
                                    <div class="item-info" style="display:flex;align-items:center;margin-top:5px;font-size:12px;">
                                        <a href="${{item?.link}}" target="_blank" style="color: #4d4dff;" title="${{get_domain_name(item?.link)}}">${{get_domain_name(item?.link).maxLength(20)}}</a>

                                        <!-- <span style="margin: 0 .8em;white-space:nowrap;display:flex;align-items:center;cursor:default;" title="Вес ссылки: найдено ${{item?.keyword_list?.length ?? 0}} раз">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="max-width:12px;min-width:12px;"
                                                viewBox="0 0 512 512">
                                                <path
                                                    d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                                            </svg>
                                            <span style="margin-left:5px;font-size:12px;">${{item?.keyword_list?.length ?? 0}}</span>
                                        </span> -->

                                        <div class="mt-auto item-keywords" style="margin-left:9.6px">
                                            <div class="item-param"><div class="query-content" title='${{decodeURI(item?.keyword_list?.join(',  '))}}'><span style="color:black">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:12px;fill:#9300FF;margin-bottom: -2.1px;"><path d="M336 352c97.2 0 176-78.8 176-176S433.2 0 336 0S160 78.8 160 176c0 18.7 2.9 36.8 8.3 53.7L7 391c-4.5 4.5-7 10.6-7 17v80c0 13.3 10.7 24 24 24h80c13.3 0 24-10.7 24-24V448h40c13.3 0 24-10.7 24-24V384h40c6.4 0 12.5-2.5 17-7l33.3-33.3c16.9 5.4 35 8.3 53.7 8.3zM376 96a40 40 0 1 1 0 80 40 40 0 1 1 0-80z"/></svg> </span>${{keyword_list}}
                                                <small class="prompt">Копировать при клике</small></div>
                                            </div>
                                            <!-- <div class="item-param">Дубликаты: <span class="param-text">${{item?.link_weight}}</span></div> -->
                                            <!-- <div class="item-param">Фигурирует в списках: <span class="param-text">${{item?.has_in_list}}</span></div> -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                }});

                if (items[tab_name].length) {{
                    $(`.tab-content-${{tab_indexes[tab_name]}}`).innerHTML = result
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'flex'
                    }});
                }}
                else {{
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'none'
                    }});
                }}

                update_pagination()
                check_all_items()

            }}

            function update_pagination() {{
                let tab_name = tab_names[selected_tab_index];
                let start_page = 1

                if (tab_pages[tab_name].page > 5) start_page = tab_pages[tab_name].page - 5;

                let page_tags = ``

                for (let i = start_page; i <= ((start_page + 9) <= temp_pagination_count ? start_page + 9 : temp_pagination_count); i++) {{
                    page_tags += `<span onclick="set_page('${{tab_names[selected_tab_index]}}', ${{i}})" ${{tab_pages[tab_name].page == i ? 'class="selected"' : ''}}>${{i}}</span>`
                }}
                $(`.pagination`).html(`
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z" />
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        ${{page_tags}}
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
                        </svg>
                        <svg class="last-page" onclick="last_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                `);
            }}

            render_items()

            window.onscroll = function(event) {{

                console.log('window.onscroll', Object.keys(seen_links).length);
                check_all_items();
        }}
        </script>
</body>

</html>
"""

    return report_html


def response_email_template(title, items, filters, leak_html, acc_search_html, fitness_html, check_html) -> str:
    report_html = f"""<!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            {NUM_STYLE}
        </head>

        <body>
        <div class="tab-head" onclick="closeModal(event)">
            <div class="flex items-center" style="flex-wrap: wrap;">
                <h2 class="object-full_name">Почта: <span style="white-space:nowrap">{title}</span></h2>

            </div>
            <div class=" tabs flex flex-wrap items-center">
                <div class="tab-1 selected" onclick="select_tab(1)">
                    Упоминания
                    <span class="tab-count">0</span>
                </div>
                <div class="tab-2" onclick="select_tab(2)">
                    Аккаунты 
                    <span class="tab-count" style="display: none;">0</span>
                </div>
            </div>
        </div>

        <div class="flex items-center wrap-reverse-container only-for-mentions" style="padding: 0 10px;">
            <div class="similars-range" style="padding-left: 20px;display: none;">
                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="position:absolute;left:5px;top:4px;"
                    viewBox="0 0 512 512">
                    <path
                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                </svg>
                <div slider id="slider-distance">
                    <div>
                        <div inverse-left style="width:100%;"></div>
                        <div inverse-right style="width:100%;"></div>
                        <div range style="left:0%;right:0%;"></div>
                        <span thumb style="left:0%;"></span>
                        <span thumb style="left:100%;"></span>
                        <div sign style="left:0%;">
                            <span id="value">0</span>
                        </div>
                        <div sign style="left:100%;">
                            <span id="value">100</span>
                        </div>
                    </div>
                    <input id="startRangeValue" type="range" tabindex="0" value="0" max="100" min="0" step="1"
                        onchange="update_startRangeValue(+event.target.value)" oninput="startRange(event)" />

                    <input id="endRangeValue" type="range" tabindex="0" value="100" max="100" min="0" step="1"
                        onchange="update_endRangeValue(+event.target.value)" oninput="endRange(event)" />
                </div>
            </div>
            <div class="filter-search-arbitrary" style="display: none;">
                <label class="input">
                    <!-- Введите название произвольного ключа -->
                    <input type="text" placeholder="Введите название ключа" onclick="showListModal(event)"
                        oninput="updateList(event)" />
                    <svg onclick="toggleListModal(event)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                        <path
                            d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
                    </svg>
                    <div class="arbitrary-keys" onclick="showListModal(event)">
                    </div>
                </label>
            </div>
            <div class="pagination-container" onclick="closeModal(event)">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <div class="content" onclick="closeModal(event)">
            <div class="tab-content-1 selected">

                <div class="empty-list">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                        <path
                            d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z" />
                    </svg>Нет найденных результатов!
                </div>
            </div>
            <div class="tab-content-2">
                <table style="border-radius: 7px;overflow: hidden;margin-right: auto;margin-left: auto;outline: 1px solid #a7a3a3;margin-bottom: 15px;"
                    cellspacing="0">
                    <tbody style="margin: 5px 8px;">
                        <tr style="">
                            <th
                                style="width: 130px;height: 45px;background: #c4d9ce;border-right: 1px solid #939393;border-bottom: 1px solid #939393;">
                                Проверка</th>
                            <th style="/* width: 100px; */height: 45px;background: #c4d9ce;border-bottom: 1px solid #939393;">Результат</th>
                        </tr>
                        {acc_search_html}
                    </tbody>
                </table>                
            </div>
        </div>

        <div class="flex only-for-mentions" onclick="closeModal(event)">
            <div class="pagination-container" style="padding: 0 7.5px 15px;">
                <div class="pagination">
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                            </path>
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        <span onclick="set_page('main', 1)" class="selected">1</span><span
                            onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                            onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                            onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                            onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                            onclick="set_page('main', 10)">10</span>
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                            </path>
                        </svg>
                        <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let startRangeValue = 0;
            let endRangeValue = 0;

            function update_startRangeValue(value) {{
                startRangeValue = value;
                render_items()
            }}
            function update_endRangeValue(value) {{
                endRangeValue = value;
                render_items()
            }}

            const startRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.min($this.value, $this.parentNode.childNodes[5].value - 1);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[1].style.width = value + '%';
                children[5].style.left = value + '%';
                children[7].style.left = value + '%'; children[11].style.left = value + '%';
                children[11].childNodes[1].innerHTML = $this.value;
            }}
            const endRange = (event) => {{
                let $this = event?.target;
                $this.value = Math.max($this.value, $this.parentNode.childNodes[3].value);
                var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                var children = $this.parentNode.childNodes[1].childNodes;
                children[3].style.width = (100 - value) + '%';
                children[5].style.right = (100 - value) + '%';
                children[9].style.left = value + '%'; children[13].style.left = value + '%';
                children[13].childNodes[1].innerHTML = $this.value;
            }}

            const isMobile = Boolean(navigator.userAgent.match(/Android/i)
                || navigator.userAgent.match(/webOS/i)
                || navigator.userAgent.match(/iPhone/i)
                || navigator.userAgent.match(/iPad/i)
                || navigator.userAgent.match(/iPod/i)
                || navigator.userAgent.match(/BlackBerry/i)
                || navigator.userAgent.match(/Windows Phone/i));

            console.log('isMobile', isMobile, navigator.userAgent);

            let selected_tab_index = 1
            function $(str) {{
                let elements = document?.querySelectorAll(str);

                return (elements?.length == 1) ? document?.querySelector(str) : elements;
            }}
            Object.prototype.html = function (html) {{
                this?.forEach(item => {{
                    item.innerHTML = html
                }});
            }}
            Object.prototype.hasClass = function (className) {{
                return this?.classList?.contains(className)
            }}
            Object.prototype.addClass = function (className) {{
                this?.classList?.add(className)
            }}
            Object.prototype.removeClass = function (className) {{
                this?.classList?.remove(className)
            }}

            let filterable_tabs = [1, 2, 3, 4, 5, 6]
            const items = {{
                main: [{items.get("all")}]
            }}

            endRangeValue = []
            items.main.forEach(item => {{
                endRangeValue.push(+item.link_weight)
            }});
            startRangeValue = endRangeValue.length ? Math.min(...endRangeValue) : 0
            endRangeValue = endRangeValue.length ? Math.max(...endRangeValue) : 0

            let endRangeElement = $('#endRangeValue');
            let startRangeElement = $('#startRangeValue');
            startRangeElement.min = endRangeElement.min = startRangeElement.value = startRangeValue;
            startRangeElement.max = endRangeElement.max = endRangeElement.value = endRangeValue;
            startRange({{ target: startRangeElement }})
            endRange({{ target: endRangeElement }})


            const tab_names = {{
                1: 'main',
                2: 'arbitrary',
                3: 'negative',
                4: 'reputation',
                5: 'connections',
                6: 'socials',
                7: 'all_materials',
            }}

            function isFilterableTab() {{
                return filterable_tabs.find(filterable_tab => filterable_tab == selected_tab_index) != undefined
            }}
            function select_tab(new_tab_index) {{
                if (selected_tab_index == new_tab_index) return

                $(`.tab-${{new_tab_index}}`)?.addClass('selected')
                $(`.tab-content-${{new_tab_index}}`)?.addClass('selected')

                $(`.tab-${{selected_tab_index}}`)?.removeClass('selected')
                $(`.tab-content-${{selected_tab_index}}`)?.removeClass('selected')

                selected_tab_index = new_tab_index
                if (new_tab_index != 1) {{
                    $('.only-for-mentions').forEach(el => {{
                        el.style.display = 'none';
                    }})
                    return;
                }}
                else {{
                    $('.only-for-mentions').forEach(el => {{
                        el.style.display = '';
                    }})
                }}
                render_items()
                let tab_name = tab_names[selected_tab_index];

                // if (isFilterableTab() && items[tab_names[selected_tab_index]]?.length > 0) {{

                //     updateList({{ target: {{ value: '' }} }})
                //     $(`.filter-search-arbitrary`).style.display = 'block';
                // }}
                // else {{
                //     $(`.filter-search-arbitrary`).style.display = 'none';
                // }}
                // $(`.similars-range`).style.display = new_tab_index == 1 ? 'block' : 'none';
            }}
            function copy(that) {{
                var inp = document.createElement('input');
                document.body.appendChild(inp)
                inp.value = that.textContent
                inp.select();
                document.execCommand('copy', false);
                inp.remove();
            }}
            const tab_indexes = {{
                main: 1,
                arbitrary: 2,
                negative: 3,
                reputation: 4,
                connections: 5,
                socials: 6,
                all_materials: 7,
            }}

            Object.entries(tab_indexes).forEach(([tab_name, tab_index]) => {{
                $(`.tab-${{tab_index}} .tab-count`).innerHTML = items[tab_name]?.length
            }});
            const tab_pages = {{
                main: {{
                    count: 0,
                    page: 1,
                }},
                arbitrary: {{
                    count: 0,
                    page: 1,
                }},
                negative: {{
                    count: 0,
                    page: 1,
                }},
                reputation: {{
                    count: 0,
                    page: 1,
                }},
                connections: {{
                    count: 0,
                    page: 1,
                }},
                socials: {{
                    count: 0,
                    page: 1,
                }},
                all_materials: {{
                    count: 0,
                    page: 1,
                }},
            }}

            function set_page(tab_name, page) {{
                tab_pages[tab_name].page = page;
                render_items()
                update_pagination()
            }}
            function minus_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page -= 1;
                render_items()
                update_pagination()
            }}
            function first_page(tab_name) {{
                if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page = 1;
                render_items()
                update_pagination()
            }}
            function plus_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page += 1;
                render_items()
                update_pagination()
            }}
            function last_page(tab_name) {{
                if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page = tab_pages[tab_name].count;
                render_items()
                update_pagination()
            }}

            const range = 20;

            Object.keys(items).forEach(tab_name => {{
                    if (items[tab_name]?.length) tab_pages[tab_name].count = Math.ceil(items[tab_name]?.length / range);
                }});

            let page = 1;
            let onfocused = false;

            function showListModal(event) {{
                event.stopPropagation()
                if (event.pointerType == '') return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
            }}
            function toggleListModal(event) {{
                event.stopPropagation()
                //if (['path', 'svg'].includes(event.target.tagName)) return;
                if (!$('.arbitrary-keys').hasClass('show')) {{
                    $('.arbitrary-keys').addClass('show')
                    $('.filter-search-arbitrary .input').addClass('selected')
                    onfocused = true;
                }}
                else {{
                    $('.arbitrary-keys').removeClass('show')
                    $('.filter-search-arbitrary .input').removeClass('selected')
                    onfocused = false;
                }}
            }}
            function closeModal(event) {{
                event?.stopPropagation()
                if (onfocused) {{
                    setTimeout(() => {{
                        $('.arbitrary-keys').removeClass('show')
                        $('.filter-search-arbitrary .input').removeClass('selected')
                        event?.target?.blur()
                    }}, 100);
                    onfocused = false;
                }}
            }}

            let filters = {{
                    1: {{ {filters.get("free_kwds")} }},
                    }}

            function makeSafeForCSS(name) {{
                return name.replace(/[^a-z0-9]/g, function (s) {{
                    var c = s.charCodeAt(0);
                    if (c == 32) return '-';
                    if (c >= 65 && c <= 90) return '_' + s.toLowerCase();
                    return '__' + ('000' + c.toString(16)).slice(-4);
                }});
            }}

            let temp_link_classes = {{}};
            let seen_links = {{}};

            const decode_filter_classes = Object.entries(filters).reduce((prev,next) => ({{ ...prev, [next[0]]: {{
                ...(Object.keys(next[1]).reduce((_prev, key) => ({{
                    ..._prev,
                    [makeSafeForCSS(key)]: key
                }}), {{}}))
            }} }}), {{}})

            function filter() {{
                updateList({{ target: {{ value: '' }} }})
                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            function uncheckAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = false;
                }});
                filter()
            }}

            function checkAll() {{
                Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                    filters[selected_tab_index][arbitrary_key] = true;
                }});
                filter()
            }}

            function toggleArbitraryKey(event, key_name) {{
                if (event.ctrlKey) {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = false;
                        $(`.keyword-id-${{makeSafeForCSS(arbitrary_key)}} input`).checked = false;
                    }});
                }}
                let decode_base_64 = decode_filter_classes[selected_tab_index][key_name];
                console.log('decode_base_64', decode_base_64);
                filters[selected_tab_index][decode_base_64] = !filters[selected_tab_index][decode_base_64]
                $(`.keyword-id-${{key_name}} input`).checked = filters[selected_tab_index][decode_base_64];

                render_items()
                $('.filter-search-arbitrary .input > input').focus()
            }}

            String.prototype.lowerIncludes = function (string) {{
                return this.toLowerCase().includes(string.toLowerCase())
            }}
            String.prototype.maxLength = function (max_length) {{
                if (this?.length > max_length) return this.slice(0,max_length) + '...';
                else return this;
            }}

            function updateList(event) {{

                let filter_keys_tags = ``

                let temp_keys = Object.keys(filters[selected_tab_index]).filter(key_name => key_name?.lowerIncludes(event.target.value));

                temp_keys.sort((a, b) => {{
                    if (a?.lowerIncludes(event.target.value) == false && b?.lowerIncludes(event.target.value) == false) {{
                        return 0
                    }}
                    else if (a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value)) {{
                        return a?.indexOf(event.target.value) < b?.indexOf(event.target.value) ? -1 : 0
                    }}
                    else {{
                        return a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value) == false ? -1 : 0
                    }}
                }});

                temp_keys.forEach(arbitrary_key => {{
                    filter_keys_tags += `
                                <label class="arbitrary-key keyword-id-${{makeSafeForCSS(arbitrary_key)}}">
                                    <input type="checkbox" onclick="toggleArbitraryKey(event, '${{makeSafeForCSS(arbitrary_key)}}')" ${{filters[selected_tab_index][arbitrary_key] ? 'checked' : 'unchecked'}}/>
                                    <span title='${{arbitrary_key}}'>${{arbitrary_key}}</span>
                                </label>
                            `;
                }});

                $('.filter-search-arbitrary .arbitrary-keys').innerHTML = `<div>` + filter_keys_tags + `</div>
                    <div class="filter-btns">
                        <span onclick="checkAll()">Выделить все</span>
                        <span onclick="uncheckAll()">Снять выделение</span>
                    </div>
                    ${{isMobile ? '' : `
                        <div class="filter-info">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
                            <div class="filter-info_prompt">Выделить только один<br/> через Ctrl + Click</div>
                        </div>
                    `}}
                `
            }}

            updateList({{ target: {{ value: '' }} }})
            let temp_pagination_count = 1;

            function get_domain_name(url) {{
                let a = document.createElement('a')
                a.href = url;
                return a.hostname;
            }}

            function isInViewport(el) {{
                const rect = el.getBoundingClientRect();

                var isinview = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    rect.right <= (window.innerWidth || document.documentElement.clientWidth)

                );

                return isinview;
            }}

            function check_all_items() {{
                Object.keys(temp_link_classes).forEach(link_class_name => {{
                    let bool = isInViewport($('#'+link_class_name))
                    if (bool) {{
                        seen_links[temp_link_classes[link_class_name]] = true;
                        let temp_svg = $(`#${{link_class_name}} .checkmark.unseen`);
                        if (temp_svg) temp_svg.addClass('seen_scale');
                        setTimeout(() => {{
                            if (temp_svg?.style?.display != undefined) temp_svg.style.display = 'none';
                        }}, 1100);
                    }}
                }})
            }}

            function render_items() {{
                let result = ``;
                let tab_name = tab_names[selected_tab_index];

                let temp_items = [...items[tab_name]];

                if (isFilterableTab()) {{
                    temp_items = temp_items.filter(item => (item.keyword_list.find(keyword => filters[selected_tab_index][keyword])))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}
                else if (tab_name == 'main') {{
                    temp_items = temp_items.filter(item => (+item.link_weight >= startRangeValue && +item.link_weight <= endRangeValue))
                    $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                }}

                temp_pagination_count = Math.ceil(temp_items?.length / range) || 1;

                if (tab_pages[tab_name].page > temp_pagination_count) tab_pages[tab_name].page = temp_pagination_count;

                let sliced_items = JSON.parse(JSON.stringify(
                    temp_items.slice((tab_pages[tab_name].page - 1) * range, tab_pages[tab_name].page * range)
                ));

                if (isFilterableTab()) {{
                    sliced_items.forEach(sliced_item => {{
                        sliced_item.keyword_list = sliced_item.keyword_list.filter(keyword => filters[selected_tab_index][keyword])
                    }});
                }}

                temp_link_classes = {{}};

                sliced_items.forEach(item => {{

                    let keyword_list = ``
                    item?.keyword_list.forEach(query => {{
                        if (keyword_list) keyword_list += '<span style="color:black;font-size:17px">, </span>'
                        keyword_list += `<span
                                    class="query"
                                    onclick="copy(this)">
                                    ${{decodeURI(query)}}
                                </span>`
                    }})

                    // Вес ссылки
                    // Похожие

                    let temp_link_class = makeSafeForCSS(item?.link);

                    temp_link_classes[temp_link_class] = item?.link;

                    result += `
                            <div class="item-container ${{seen_links[item?.link] ? 'seen_link' : ''}}" id="${{temp_link_class}}">
                                <div class="item" style="position:relative">
                                    ${{seen_links[item?.link] ? '<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>' : '<svg class="checkmark unseen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"></circle></svg>'}}

                                    <div class="flex items-center">
                                        <a target="_blank" href="${{item?.link}}" class="item-title" title="${{item?.title}}">${{item?.title}}</a>
                                        <!-- <a target="_blank" href="${{item?.link}}" class="item-more">Источник <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M320 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h82.7L201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L448 109.3V192c0 17.7 14.3 32 32 32s32-14.3 32-32V32c0-17.7-14.3-32-32-32H320zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg></a> -->
                                    </div>
                                    <div class="item-content">${{item?.content}}</div>
                                    <div class="item-info" style="display:flex;align-items:center;margin-top:5px;font-size:12px;">
                                        <a href="${{item?.link}}" target="_blank" style="color: #4d4dff;" title="${{get_domain_name(item?.link)}}">${{get_domain_name(item?.link).maxLength(20)}}</a>

                                        <!-- <span style="margin: 0 .8em;white-space:nowrap;display:flex;align-items:center;cursor:default;" title="Вес ссылки: найдено ${{item?.keyword_list?.length ?? 0}} раз">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="max-width:12px;min-width:12px;"
                                                viewBox="0 0 512 512">
                                                <path
                                                    d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                                            </svg>
                                            <span style="margin-left:5px;font-size:12px;">${{item?.keyword_list?.length ?? 0}}</span>
                                        </span> -->

                                        <div class="mt-auto item-keywords" style="margin-left:9.6px">
                                            <div class="item-param"><div class="query-content" title='${{decodeURI(item?.keyword_list?.join(',  '))}}'><span style="color:black">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:12px;fill:#9300FF;margin-bottom: -2.1px;"><path d="M336 352c97.2 0 176-78.8 176-176S433.2 0 336 0S160 78.8 160 176c0 18.7 2.9 36.8 8.3 53.7L7 391c-4.5 4.5-7 10.6-7 17v80c0 13.3 10.7 24 24 24h80c13.3 0 24-10.7 24-24V448h40c13.3 0 24-10.7 24-24V384h40c6.4 0 12.5-2.5 17-7l33.3-33.3c16.9 5.4 35 8.3 53.7 8.3zM376 96a40 40 0 1 1 0 80 40 40 0 1 1 0-80z"/></svg> </span>${{keyword_list}}
                                                <small class="prompt">Копировать при клике</small></div>
                                            </div>
                                            <!-- <div class="item-param">Дубликаты: <span class="param-text">${{item?.link_weight}}</span></div> -->
                                            <!-- <div class="item-param">Фигурирует в списках: <span class="param-text">${{item?.has_in_list}}</span></div> -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                }});

                if (items[tab_name].length) {{
                    $(`.tab-content-${{tab_indexes[tab_name]}}`).innerHTML = result
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'flex'
                    }});
                }}
                else {{
                    $(`.pagination`).forEach(pagination_element => {{
                        pagination_element.style.display = 'none'
                    }});
                }}

                update_pagination()
                check_all_items()

            }}

            function update_pagination() {{
                let tab_name = tab_names[selected_tab_index];
                let start_page = 1

                if (tab_pages[tab_name].page > 5) start_page = tab_pages[tab_name].page - 5;

                let page_tags = ``

                for (let i = start_page; i <= ((start_page + 9) <= temp_pagination_count ? start_page + 9 : temp_pagination_count); i++) {{
                    page_tags += `<span onclick="set_page('${{tab_names[selected_tab_index]}}', ${{i}})" ${{tab_pages[tab_name].page == i ? 'class="selected"' : ''}}>${{i}}</span>`
                }}
                $(`.pagination`).html(`
                    <div class="flex hovered-angle">
                        <svg class="first-page" onclick="first_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                        </svg>
                        <svg onclick="minus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 320 512">
                            <path
                                d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z" />
                        </svg>
                    </div>
                    <div class="flex h-full scrollbar">
                        ${{page_tags}}
                    </div>
                    <div class="flex hovered-angle">
                        <svg onclick="plus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 320 512">
                            <path
                                d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
                        </svg>
                        <svg class="last-page" onclick="last_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                            <path
                                d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                        </svg>
                    </div>
                `);
            }}

            render_items()

            window.onscroll = function(event) {{

                console.log('window.onscroll', Object.keys(seen_links).length);
                check_all_items();
        }}
        </script>
</body>

</html>
"""

    return report_html


def response_tg_template(title, interests_html, groups1_html: list[str], groups2_html: list[str],
                         profile_html: list[str], phones: list[str]):
    html = f"""
    <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            {TG_STYLE}
        </head>

        <body>
            <div class="tab-head" onclick="closeModal(event)">
                <div class="flex items-center" style="flex-wrap: wrap;">
                    <h2 class="object-full_name">Пользователь: <span style="white-space:nowrap">{title}</span></h2>

                </div>
                <div class=" tabs flex flex-wrap items-center">
                    <div class="tab-1 selected" onclick="select_tab(1)">
                        Интересы
                    </div>
                    <div class="tab-2" onclick="select_tab(2)">
                        Группы №1
                    </div>
                    <div class="tab-3" onclick="select_tab(3)">
                        Группы №2
                    </div>
                    <div class="tab-4" onclick="select_tab(4)">
                        История профиля  
                    </div>
                    <div class="tab-5" onclick="select_tab(5)">
                        Телефоны
                    </div>
                </div>
            </div>

            <div class="flex items-center wrap-reverse-container only-for-mentions" style="padding: 0 10px;">
                <div class="similars-range" style="padding-left: 20px;display: none;">
                    <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="position:absolute;left:5px;top:4px;"
                        viewBox="0 0 512 512">
                        <path
                            d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                    </svg>
                    <div slider id="slider-distance">
                        <div>
                            <div inverse-left style="width:100%;"></div>
                            <div inverse-right style="width:100%;"></div>
                            <div range style="left:0%;right:0%;"></div>
                            <span thumb style="left:0%;"></span>
                            <span thumb style="left:100%;"></span>
                            <div sign style="left:0%;">
                                <span id="value">0</span>
                            </div>
                            <div sign style="left:100%;">
                                <span id="value">100</span>
                            </div>
                        </div>
                        <input id="startRangeValue" type="range" tabindex="0" value="0" max="100" min="0" step="1"
                            onchange="update_startRangeValue(+event.target.value)" oninput="startRange(event)" />

                        <input id="endRangeValue" type="range" tabindex="0" value="100" max="100" min="0" step="1"
                            onchange="update_endRangeValue(+event.target.value)" oninput="endRange(event)" />
                    </div>
                </div>
                <div class="filter-search-arbitrary" style="display: none;">
                    <label class="input">
                        <!-- Введите название произвольного ключа -->
                        <input type="text" placeholder="Введите название ключа" onclick="showListModal(event)"
                            oninput="updateList(event)" />
                        <svg onclick="toggleListModal(event)" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
                            <path
                                d="M201.4 342.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 274.7 86.6 137.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z" />
                        </svg>
                        <div class="arbitrary-keys" onclick="showListModal(event)">
                        </div>
                    </label>
                </div>
                <div class="pagination-container" onclick="closeModal(event)">
                    <div class="pagination">
                        <div class="flex hovered-angle">
                            <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 512 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                            </svg>
                            <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                                </path>
                            </svg>
                        </div>
                        <div class="flex h-full scrollbar">
                            <span onclick="set_page('main', 1)" class="selected">1</span><span
                                onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                                onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                                onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                                onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                                onclick="set_page('main', 10)">10</span>
                        </div>
                        <div class="flex hovered-angle">
                            <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                                <path
                                    d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                                </path>
                            </svg>
                            <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 512 512">
                                <path
                                    d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <div class="content" onclick="closeModal(event)">
                <div class="tab-content-1 selected">

                    <table style="margin-bottom: 15px;">
                        <tr>
                            <th style="width: 130px;">Блок</th>
                            <th style="width: 400px;">Категория</th>
                            <th style="width: 400px;">Тэг</th>
                        </tr>
                        
                        {interests_html}
                    </table>
                </div>
                <div class="tab-content-2" style="overflow-x: scroll;min-height: calc(100vh - 103px);">
                    <div>
                        <div class="groups" style="margin-bottom: 15px;margin-left:10px">
                            {
                                '<div class="groups-description"><span class="f-w-600">Группы №1, в которых замечен пользователь:<br> (в формате [имя группы | дата выявления]):</span></div>' if len(groups1_html) != 0 else '<div class="phones-description"><span class="f-w-600">Группы не найдены</span></div>'
                            }
                            <div class="block">
                                <!-- Leaks -->
                            </div>

                        </div>
                        <script>
                            let groups = {groups1_html};

                            if (groups.length) {{
                                let leaks_container = document.querySelector('.groups .flex');
                                let leak_leaks = '<div class="flex flex-col group-block">';

                                console.log('leaks_container', leaks_container);

                                let per_col = Math.ceil(groups.length ** .65) + 1;

                                per_col = Math.ceil(((groups.length) / per_col) > 6 ? (groups.length) / 6 : per_col);

                                console.log('per_col', per_col);

                                groups.forEach((leak, i) => {{
                                    if (((i) % per_col) == 0 && i != 0) {{
                                        leak_leaks += `</div>`;
                                        if (i != (groups.length - 1)) leak_leaks += `<div class="flex flex-col group-block">`;
                                    }}
                                    leak_leaks += `<span class="leak">${{leak}}</span>`;

                                    if (i == (groups.length - 1) || ((i + 1) / per_col) == 6) {{
                                        leak_leaks += `</div>`;
                                    }}
                                }})


                                leaks_container.innerHTML += leak_leaks;
                            }}
                            else {{
                                document.querySelector('.groups-description .f-w-600').textContent = 'Информация о группах отсудствует'
                                document.querySelector('.groups .flex').innerHTML = '...'
                            }} 
                        </script>
                    </div>
                </div>
                <div class="tab-content-3" style="overflow-x: scroll;min-height: calc(100vh - 103px);">
                    <div>
                        <div class="groups2" style="margin-bottom: 15px;margin-left:10px">
                        {
                            '<div class="groups2-description"><span class="f-w-600">Группы №2, в которых замечен пользователь:<br> (в формате [имя группы | дата выявления]):</span></div>' if len(groups2_html) != 0 else '<div class="phones-description"><span class="f-w-600">Группы не найдены</span></div>'
                        }
                            <div class="block">
                                <!-- Leaks -->
                            </div>

                        </div>
                        <script>
                            let groups2 = {groups2_html};

                            if (groups2.length) {{
                                let leaks_container = document.querySelector('.groups2 .flex');
                                let leak_leaks = '<div class="flex flex-col">';

                                console.log('leaks_container', leaks_container);

                                let per_col = Math.ceil(groups2.length ** .65) + 1;

                                per_col = Math.ceil(((groups2.length) / per_col) > 6 ? (groups2.length) / 6 : per_col);

                                console.log('per_col', per_col);

                                groups2.forEach((leak, i) => {{
                                    if (((i) % per_col) == 0 && i != 0) {{
                                        leak_leaks += `</div>`;
                                        if (i != (groups2.length - 1)) leak_leaks += `<div class="flex flex-col">`;
                                    }}
                                    leak_leaks += `<span class="leak">${{leak}}</span>`;

                                    if (i == (groups2.length - 1) || ((i + 1) / per_col) == 6) {{
                                        leak_leaks += `</div>`;
                                    }}
                                }})


                                leaks_container.innerHTML += leak_leaks;
                            }}
                            else {{
                                document.querySelector('.groups2-description .f-w-600').textContent = 'Информация о группах отсудствует'
                                document.querySelector('.groups2 .flex').innerHTML = '...'
                            }} 
                        </script>
                    </div>
                </div>
                <div class="tab-content-4" style="overflow-x: scroll;min-height: calc(100vh - 103px);">
                    <div>
                        <div class="leaks" style="margin-bottom: 15px;margin-left:10px">
                        {
                            '<div class="leak-description"><span class="f-w-600">История изменения профиля пользователя содержит записей: {len(profile_html)}<br></span></div>' if len(profile_html) != 0 else '<div class="phones-description"><span class="f-w-600">История изменения профиля пользователя не выявлена</span></div>'
                        }
                            
                            <div class="flex">
                                <!-- Leaks -->
                            </div>

                        </div>
                        <script>
                            let leaks = {profile_html};

                            if (leaks.length) {{
                                let leaks_container = document.querySelector('.leaks .flex');
                                let leak_leaks = '<div class="flex flex-col">';

                                console.log('leaks_container', leaks_container);

                                let per_col = Math.ceil(leaks.length ** .65) + 1;

                                per_col = Math.ceil(((leaks.length) / per_col) > 6 ? (leaks.length) / 6 : per_col);

                                console.log('per_col', per_col);

                                leaks.forEach((leak, i) => {{
                                    if (((i) % per_col) == 0 && i != 0) {{
                                        leak_leaks += `</div>`;
                                        if (i != (leaks.length - 1)) leak_leaks += `<div class="flex flex-col">`;
                                    }}
                                    leak_leaks += `<span class="leak">${{leak}}</span>`;

                                    if (i == (leaks.length - 1) || ((i + 1) / per_col) == 6) {{
                                        leak_leaks += `</div>`;
                                    }}
                                }})


                                leaks_container.innerHTML += leak_leaks;
                            }}
                            else {{
                                document.querySelector('.leak-description .f-w-600').textContent = 'Информация об изменений профиля отсутствует'
                                document.querySelector('.leaks .flex').innerHTML = '...'
                            }} 
                        </script>
                    </div>
                </div>
                <div class="tab-content-5" style="overflow-x: scroll;min-height: calc(100vh - 103px);">
                    <div>
                        <div class="phones" style="margin-bottom: 15px;margin-left:10px">
                            {
                                '<div class="phones-description"><span class="f-w-600">Список телефонов пользователя: </span></div>' if len(phones) != 0 else '<div class="phones-description"><span class="f-w-600">Привязанный номер телефона не выявлен</span></div>'
                            }
                            <div class="flex">
                                <!-- Leaks -->
                            </div>

                        </div>
                        <script>
                            let phones = {phones};

                            if (phones.length) {{
                                let leaks_container = document.querySelector('.phones .flex');
                                let leak_leaks = '<div class="flex flex-col">';

                                console.log('leaks_container', leaks_container);

                                let per_col = Math.ceil(phones.length ** .65) + 1;

                                per_col = Math.ceil(((phones.length) / per_col) > 6 ? (phones.length) / 6 : per_col);

                                console.log('per_col', per_col);

                                phones.forEach((leak, i) => {{
                                    if (((i) % per_col) == 0 && i != 0) {{
                                        leak_leaks += `</div>`;
                                        if (i != (phones.length - 1)) leak_leaks += `<div class="flex flex-col">`;
                                    }}
                                    leak_leaks += `<span class="leak">${{leak}}</span>`;

                                    if (i == (phones.length - 1) || ((i + 1) / per_col) == 6) {{
                                        leak_leaks += `</div>`;
                                    }}
                                }})


                                leaks_container.innerHTML += leak_leaks;
                            }}
                            else {{
                                document.querySelector('.phones-description .f-w-600').textContent = 'Информация об телефоне пользователя отсудствует'
                                document.querySelector('.phones .flex').innerHTML = '...'
                            }} 
                        </script>
                    </div>
                </div>
            </div>

            <div class="flex only-for-mentions" onclick="closeModal(event)">
                <div class="pagination-container" style="padding: 0 7.5px 15px;">
                    <div class="pagination">
                        <div class="flex hovered-angle">
                            <svg class="first-page" onclick="first_page('main')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 512 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                            </svg>
                            <svg onclick="minus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z">
                                </path>
                            </svg>
                        </div>
                        <div class="flex h-full scrollbar">
                            <span onclick="set_page('main', 1)" class="selected">1</span><span
                                onclick="set_page('main', 2)">2</span><span onclick="set_page('main', 3)">3</span><span
                                onclick="set_page('main', 4)">4</span><span onclick="set_page('main', 5)">5</span><span
                                onclick="set_page('main', 6)">6</span><span onclick="set_page('main', 7)">7</span><span
                                onclick="set_page('main', 8)">8</span><span onclick="set_page('main', 9)">9</span><span
                                onclick="set_page('main', 10)">10</span>
                        </div>
                        <div class="flex hovered-angle">
                            <svg onclick="plus_page('main')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                                <path
                                    d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z">
                                </path>
                            </svg>
                            <svg class="last-page" onclick="last_page('main')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 512 512">
                                <path
                                    d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                            </svg>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                let startRangeValue = 0;
                let endRangeValue = 0;

                function update_startRangeValue(value) {{
                    startRangeValue = value;
                    render_items()
                }}
                function update_endRangeValue(value) {{
                    endRangeValue = value;
                    render_items()
                }}

                const startRange = (event) => {{
                    let $this = event?.target;
                    $this.value = Math.min($this.value, $this.parentNode.childNodes[5].value - 1);
                    var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                    var children = $this.parentNode.childNodes[1].childNodes;
                    children[1].style.width = value + '%';
                    children[5].style.left = value + '%';
                    children[7].style.left = value + '%'; children[11].style.left = value + '%';
                    children[11].childNodes[1].innerHTML = $this.value;
                }}
                const endRange = (event) => {{
                    let $this = event?.target;
                    $this.value = Math.max($this.value, $this.parentNode.childNodes[3].value);
                    var value = (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.value) - (100 / (parseInt($this.max) - parseInt($this.min))) * parseInt($this.min);
                    var children = $this.parentNode.childNodes[1].childNodes;
                    children[3].style.width = (100 - value) + '%';
                    children[5].style.right = (100 - value) + '%';
                    children[9].style.left = value + '%'; children[13].style.left = value + '%';
                    children[13].childNodes[1].innerHTML = $this.value;
                }}

                const isMobile = Boolean(navigator.userAgent.match(/Android/i)
                    || navigator.userAgent.match(/webOS/i)
                    || navigator.userAgent.match(/iPhone/i)
                    || navigator.userAgent.match(/iPad/i)
                    || navigator.userAgent.match(/iPod/i)
                    || navigator.userAgent.match(/BlackBerry/i)
                    || navigator.userAgent.match(/Windows Phone/i));

                console.log('isMobile', isMobile, navigator.userAgent);

                let selected_tab_index = 1
                function $(str) {{
                    let elements = document?.querySelectorAll(str);

                    return (elements?.length == 1) ? document?.querySelector(str) : elements;
                }}
                Object.prototype.html = function (html) {{
                    this?.forEach(item => {{
                        item.innerHTML = html
                    }});
                }}
                Object.prototype.hasClass = function (className) {{
                    return this?.classList?.contains(className)
                }}
                Object.prototype.addClass = function (className) {{
                    this?.classList?.add(className)
                }}
                Object.prototype.removeClass = function (className) {{
                    this?.classList?.remove(className)
                }}

                let filterable_tabs = [1, 2, 3, 4, 5, 6]
                const items = {{
                    main: []
                }}

                endRangeValue = []
                items.main.forEach(item => {{
                    endRangeValue.push(+item.link_weight)
                }});
                startRangeValue = endRangeValue.length ? Math.min(...endRangeValue) : 0
                endRangeValue = endRangeValue.length ? Math.max(...endRangeValue) : 0

                let endRangeElement = $('#endRangeValue');
                let startRangeElement = $('#startRangeValue');
                startRangeElement.min = endRangeElement.min = startRangeElement.value = startRangeValue;
                startRangeElement.max = endRangeElement.max = endRangeElement.value = endRangeValue;
                startRange({{ target: startRangeElement }})
                endRange({{ target: endRangeElement }})


                const tab_names = {{
                    1: 'main',
                    2: 'arbitrary',
                    3: 'negative',
                    4: 'reputation',
                    5: 'connections',
                    6: 'socials',
                    7: 'all_materials',
                }}

                function isFilterableTab() {{
                    return filterable_tabs.find(filterable_tab => filterable_tab == selected_tab_index) != undefined
                }}
                function select_tab(new_tab_index) {{
                    if (selected_tab_index == new_tab_index) return

                    $(`.tab-${{new_tab_index}}`)?.addClass('selected')
                    $(`.tab-content-${{new_tab_index}}`)?.addClass('selected')

                    $(`.tab-${{selected_tab_index}}`)?.removeClass('selected')
                    $(`.tab-content-${{selected_tab_index}}`)?.removeClass('selected')

                    selected_tab_index = new_tab_index
                    if (new_tab_index != 1) {{
                        $('.only-for-mentions').forEach(el => {{
                            el.style.display = 'none';
                        }})
                        return;
                    }}
                    else {{
                        $('.only-for-mentions').forEach(el => {{
                            el.style.display = '';
                        }})
                    }}
                    render_items()
                    let tab_name = tab_names[selected_tab_index];

                    // if (isFilterableTab() && items[tab_names[selected_tab_index]]?.length > 0) {{

                    //     updateList({{ target: {{ value: '' }} }})
                    //     $(`.filter-search-arbitrary`).style.display = 'block';
                    // }}
                    // else {{
                    //     $(`.filter-search-arbitrary`).style.display = 'none';
                    // }}
                    // $(`.similars-range`).style.display = new_tab_index == 1 ? 'block' : 'none';
                }}
                function copy(that) {{
                    var inp = document.createElement('input');
                    document.body.appendChild(inp)
                    inp.value = that.textContent
                    inp.select();
                    document.execCommand('copy', false);
                    inp.remove();
                }}
                const tab_indexes = {{
                    main: 1,
                    arbitrary: 2,
                    negative: 3,
                    reputation: 4,
                    connections: 5,
                    socials: 6,
                    all_materials: 7,
                }}

                Object.entries(tab_indexes).forEach(([tab_name, tab_index]) => {{
                    $(`.tab-${{tab_index}} .tab-count`).innerHTML = items[tab_name]?.length
                }});
                const tab_pages = {{
                    main: {{
                        count: 0,
                        page: 1,
                    }},
                    arbitrary: {{
                        count: 0,
                        page: 1,
                    }},
                    negative: {{
                        count: 0,
                        page: 1,
                    }},
                    reputation: {{
                        count: 0,
                        page: 1,
                    }},
                    connections: {{
                        count: 0,
                        page: 1,
                    }},
                    socials: {{
                        count: 0,
                        page: 1,
                    }},
                    all_materials: {{
                        count: 0,
                        page: 1,
                    }},
                }}

                function set_page(tab_name, page) {{
                    tab_pages[tab_name].page = page;
                    render_items()
                    update_pagination()
                }}
                function minus_page(tab_name) {{
                    if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page -= 1;
                    render_items()
                    update_pagination()
                }}
                function first_page(tab_name) {{
                    if (tab_pages[tab_name].page > 1) tab_pages[tab_name].page = 1;
                    render_items()
                    update_pagination()
                }}
                function plus_page(tab_name) {{
                    if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page += 1;
                    render_items()
                    update_pagination()
                }}
                function last_page(tab_name) {{
                    if (tab_pages[tab_name].page < tab_pages[tab_name].count) tab_pages[tab_name].page = tab_pages[tab_name].count;
                    render_items()
                    update_pagination()
                }}

                const range = 20;

                Object.keys(items).forEach(tab_name => {{
                        if (items[tab_name]?.length) tab_pages[tab_name].count = Math.ceil(items[tab_name]?.length / range);
                    }});

                let page = 1;
                let onfocused = false;

                function showListModal(event) {{
                    event.stopPropagation()
                    if (event.pointerType == '') return;
                    if (!$('.arbitrary-keys').hasClass('show')) {{
                        $('.arbitrary-keys').addClass('show')
                        $('.filter-search-arbitrary .input').addClass('selected')
                        onfocused = true;
                    }}
                }}
                function toggleListModal(event) {{
                    event.stopPropagation()
                    //if (['path', 'svg'].includes(event.target.tagName)) return;
                    if (!$('.arbitrary-keys').hasClass('show')) {{
                        $('.arbitrary-keys').addClass('show')
                        $('.filter-search-arbitrary .input').addClass('selected')
                        onfocused = true;
                    }}
                    else {{
                        $('.arbitrary-keys').removeClass('show')
                        $('.filter-search-arbitrary .input').removeClass('selected')
                        onfocused = false;
                    }}
                }}
                function closeModal(event) {{
                    event?.stopPropagation()
                    if (onfocused) {{
                        setTimeout(() => {{
                            $('.arbitrary-keys').removeClass('show')
                            $('.filter-search-arbitrary .input').removeClass('selected')
                            event?.target?.blur()
                        }}, 100);
                        onfocused = false;
                    }}
                }}

                let filters = {{
                        1: {{  }},
                        }}

                function makeSafeForCSS(name) {{
                    return name.replace(/[^a-z0-9]/g, function (s) {{
                        var c = s.charCodeAt(0);
                        if (c == 32) return '-';
                        if (c >= 65 && c <= 90) return '_' + s.toLowerCase();
                        return '__' + ('000' + c.toString(16)).slice(-4);
                    }});
                }}

                let temp_link_classes = {{}};
                let seen_links = {{}};

                const decode_filter_classes = Object.entries(filters).reduce((prev,next) => ({{ ...prev, [next[0]]: {{
                    ...(Object.keys(next[1]).reduce((_prev, key) => ({{
                        ..._prev,
                        [makeSafeForCSS(key)]: key
                    }}), {{}}))
                }} }}), {{}})

                function filter() {{
                    updateList({{ target: {{ value: '' }} }})
                    render_items()
                    $('.filter-search-arbitrary .input > input').focus()
                }}

                function uncheckAll() {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = false;
                    }});
                    filter()
                }}

                function checkAll() {{
                    Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                        filters[selected_tab_index][arbitrary_key] = true;
                    }});
                    filter()
                }}

                function toggleArbitraryKey(event, key_name) {{
                    if (event.ctrlKey) {{
                        Object.keys(filters[selected_tab_index]).forEach(arbitrary_key => {{
                            filters[selected_tab_index][arbitrary_key] = false;
                            $(`.keyword-id-${{makeSafeForCSS(arbitrary_key)}} input`).checked = false;
                        }});
                    }}
                    let decode_base_64 = decode_filter_classes[selected_tab_index][key_name];
                    console.log('decode_base_64', decode_base_64);
                    filters[selected_tab_index][decode_base_64] = !filters[selected_tab_index][decode_base_64]
                    $(`.keyword-id-${{key_name}} input`).checked = filters[selected_tab_index][decode_base_64];

                    render_items()
                    $('.filter-search-arbitrary .input > input').focus()
                }}

                String.prototype.lowerIncludes = function (string) {{
                    return this.toLowerCase().includes(string.toLowerCase())
                }}
                String.prototype.maxLength = function (max_length) {{
                    if (this?.length > max_length) return this.slice(0,max_length) + '...';
                    else return this;
                }}

                function updateList(event) {{

                    let filter_keys_tags = ``

                    let temp_keys = Object.keys(filters[selected_tab_index]).filter(key_name => key_name?.lowerIncludes(event.target.value));

                    temp_keys.sort((a, b) => {{
                        if (a?.lowerIncludes(event.target.value) == false && b?.lowerIncludes(event.target.value) == false) {{
                            return 0
                        }}
                        else if (a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value)) {{
                            return a?.indexOf(event.target.value) < b?.indexOf(event.target.value) ? -1 : 0
                        }}
                        else {{
                            return a?.lowerIncludes(event.target.value) && b?.lowerIncludes(event.target.value) == false ? -1 : 0
                        }}
                    }});

                    temp_keys.forEach(arbitrary_key => {{
                        filter_keys_tags += `
                                    <label class="arbitrary-key keyword-id-${{makeSafeForCSS(arbitrary_key)}}">
                                        <input type="checkbox" onclick="toggleArbitraryKey(event, '${{makeSafeForCSS(arbitrary_key)}}')" ${{filters[selected_tab_index][arbitrary_key] ? 'checked' : 'unchecked'}}/>
                                        <span title='${{arbitrary_key}}'>${{arbitrary_key}}</span>
                                    </label>
                                `;
                    }});

                    $('.filter-search-arbitrary .arbitrary-keys').innerHTML = `<div>` + filter_keys_tags + `</div>
                        <div class="filter-btns">
                            <span onclick="checkAll()">Выделить все</span>
                            <span onclick="uncheckAll()">Снять выделение</span>
                        </div>
                        ${{isMobile ? '' : `
                            <div class="filter-info">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zm0-384c13.3 0 24 10.7 24 24V264c0 13.3-10.7 24-24 24s-24-10.7-24-24V152c0-13.3 10.7-24 24-24zM224 352a32 32 0 1 1 64 0 32 32 0 1 1 -64 0z"/></svg>
                                <div class="filter-info_prompt">Выделить только один<br/> через Ctrl + Click</div>
                            </div>
                        `}}
                    `
                }}

                updateList({{ target: {{ value: '' }} }})
                let temp_pagination_count = 1;

                function get_domain_name(url) {{
                    let a = document.createElement('a')
                    a.href = url;
                    return a.hostname;
                }}

                function isInViewport(el) {{
                    const rect = el.getBoundingClientRect();

                    var isinview = (
                        rect.top >= 0 &&
                        rect.left >= 0 &&
                        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                        rect.right <= (window.innerWidth || document.documentElement.clientWidth)

                    );

                    return isinview;
                }}

                function check_all_items() {{
                    Object.keys(temp_link_classes).forEach(link_class_name => {{
                        let bool = isInViewport($('#'+link_class_name))
                        if (bool) {{
                            seen_links[temp_link_classes[link_class_name]] = true;
                            let temp_svg = $(`#${{link_class_name}} .checkmark.unseen`);
                            if (temp_svg) temp_svg.addClass('seen_scale');
                            setTimeout(() => {{
                                if (temp_svg?.style?.display != undefined) temp_svg.style.display = 'none';
                            }}, 1100);
                        }}
                    }})
                }}

                function render_items() {{
                    let result = ``;
                    let tab_name = tab_names[selected_tab_index];

                    let temp_items = [...items[tab_name]];

                    if (isFilterableTab()) {{
                        temp_items = temp_items.filter(item => (item.keyword_list.find(keyword => filters[selected_tab_index][keyword])))
                        $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                    }}
                    else if (tab_name == 'main') {{
                        temp_items = temp_items.filter(item => (+item.link_weight >= startRangeValue && +item.link_weight <= endRangeValue))
                        $(`.tab-${{selected_tab_index}} .tab-count`).innerHTML = temp_items.length;
                    }}

                    temp_pagination_count = Math.ceil(temp_items?.length / range) || 1;

                    if (tab_pages[tab_name].page > temp_pagination_count) tab_pages[tab_name].page = temp_pagination_count;

                    let sliced_items = JSON.parse(JSON.stringify(
                        temp_items.slice((tab_pages[tab_name].page - 1) * range, tab_pages[tab_name].page * range)
                    ));

                    if (isFilterableTab()) {{
                        sliced_items.forEach(sliced_item => {{
                            sliced_item.keyword_list = sliced_item.keyword_list.filter(keyword => filters[selected_tab_index][keyword])
                        }});
                    }}

                    temp_link_classes = {{}};

                    sliced_items.forEach(item => {{

                        let keyword_list = ``
                        item?.keyword_list.forEach(query => {{
                            if (keyword_list) keyword_list += '<span style="color:black;font-size:17px">, </span>'
                            keyword_list += `<span
                                        class="query"
                                        onclick="copy(this)">
                                        ${{decodeURI(query)}}
                                    </span>`
                        }})

                        // Вес ссылки
                        // Похожие

                        let temp_link_class = makeSafeForCSS(item?.link);

                        temp_link_classes[temp_link_class] = item?.link;

                        result += `
                                <div class="item-container ${{seen_links[item?.link] ? 'seen_link' : ''}}" id="${{temp_link_class}}">
                                    <div class="item" style="position:relative">
                                        ${{seen_links[item?.link] ? '<svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/><path class="checkmark__check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/></svg>' : '<svg class="checkmark unseen" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52"><circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"></circle></svg>'}}

                                        <div class="flex items-center">
                                            <a target="_blank" href="${{item?.link}}" class="item-title" title="${{item?.title}}">${{item?.title}}</a>
                                            <!-- <a target="_blank" href="${{item?.link}}" class="item-more">Источник <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M320 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h82.7L201.4 265.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L448 109.3V192c0 17.7 14.3 32 32 32s32-14.3 32-32V32c0-17.7-14.3-32-32-32H320zM80 32C35.8 32 0 67.8 0 112V432c0 44.2 35.8 80 80 80H400c44.2 0 80-35.8 80-80V320c0-17.7-14.3-32-32-32s-32 14.3-32 32V432c0 8.8-7.2 16-16 16H80c-8.8 0-16-7.2-16-16V112c0-8.8 7.2-16 16-16H192c17.7 0 32-14.3 32-32s-14.3-32-32-32H80z"/></svg></a> -->
                                        </div>
                                        <div class="item-content">${{item?.content}}</div>
                                        <div class="item-info" style="display:flex;align-items:center;margin-top:5px;font-size:12px;">
                                            <a href="${{item?.link}}" target="_blank" style="color: #4d4dff;" title="${{get_domain_name(item?.link)}}">${{get_domain_name(item?.link).maxLength(20)}}</a>

                                            <!-- <span style="margin: 0 .8em;white-space:nowrap;display:flex;align-items:center;cursor:default;" title="Вес ссылки: найдено ${{item?.keyword_list?.length ?? 0}} раз">
                                                <svg xmlns="http://www.w3.org/2000/svg" class="clone" style="max-width:12px;min-width:12px;"
                                                    viewBox="0 0 512 512">
                                                    <path
                                                        d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z" />
                                                </svg>
                                                <span style="margin-left:5px;font-size:12px;">${{item?.keyword_list?.length ?? 0}}</span>
                                            </span> -->

                                            <div class="mt-auto item-keywords" style="margin-left:9.6px">
                                                <div class="item-param"><div class="query-content" title='${{decodeURI(item?.keyword_list?.join(',  '))}}'><span style="color:black">
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style="width:12px;fill:#9300FF;margin-bottom: -2.1px;"><path d="M336 352c97.2 0 176-78.8 176-176S433.2 0 336 0S160 78.8 160 176c0 18.7 2.9 36.8 8.3 53.7L7 391c-4.5 4.5-7 10.6-7 17v80c0 13.3 10.7 24 24 24h80c13.3 0 24-10.7 24-24V448h40c13.3 0 24-10.7 24-24V384h40c6.4 0 12.5-2.5 17-7l33.3-33.3c16.9 5.4 35 8.3 53.7 8.3zM376 96a40 40 0 1 1 0 80 40 40 0 1 1 0-80z"/></svg> </span>${{keyword_list}}
                                                    <small class="prompt">Копировать при клике</small></div>
                                                </div>
                                                <!-- <div class="item-param">Дубликаты: <span class="param-text">${{item?.link_weight}}</span></div> -->
                                                <!-- <div class="item-param">Фигурирует в списках: <span class="param-text">${{item?.has_in_list}}</span></div> -->
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                    }});

                    if (items[tab_name].length) {{
                        $(`.tab-content-${{tab_indexes[tab_name]}}`).innerHTML = result
                        $(`.pagination`).forEach(pagination_element => {{
                            pagination_element.style.display = 'flex'
                        }});
                    }}
                    else {{
                        $(`.pagination`).forEach(pagination_element => {{
                            pagination_element.style.display = 'none'
                        }});
                    }}

                    update_pagination()
                    check_all_items()

                }}

                function update_pagination() {{
                    let tab_name = tab_names[selected_tab_index];
                    let start_page = 1

                    if (tab_pages[tab_name].page > 5) start_page = tab_pages[tab_name].page - 5;

                    let page_tags = ``

                    for (let i = start_page; i <= ((start_page + 9) <= temp_pagination_count ? start_page + 9 : temp_pagination_count); i++) {{
                        page_tags += `<span onclick="set_page('${{tab_names[selected_tab_index]}}', ${{i}})" ${{tab_pages[tab_name].page == i ? 'class="selected"' : ''}}>${{i}}</span>`
                    }}
                    $(`.pagination`).html(`
                        <div class="flex hovered-angle">
                            <svg class="first-page" onclick="first_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160zm352-160l-160 160c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L301.3 256 438.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0z" />
                            </svg>
                            <svg onclick="minus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z" />
                            </svg>
                        </div>
                        <div class="flex h-full scrollbar">
                            ${{page_tags}}
                        </div>
                        <div class="flex hovered-angle">
                            <svg onclick="plus_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 320 512">
                                <path
                                    d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z" />
                            </svg>
                            <svg class="last-page" onclick="last_page('${{tab_names[selected_tab_index]}}')" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
                                <path
                                    d="M470.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L402.7 256 265.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160zm-352 160l160-160c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L210.7 256 73.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0z" />
                            </svg>
                        </div>
                    `);
                }}

                render_items()

                window.onscroll = function(event) {{

                    console.log('window.onscroll', Object.keys(seen_links).length);
                    check_all_items();
            }}
            </script>
    </body>

    </html>
    """

    return html
