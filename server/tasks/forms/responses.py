from server.api.schemas.query import FoundInfo, NumberInfo
from server.tasks.forms.forms import filter_by_weight, form_js_data
from server.tasks.forms.vars import form_var_filters, form_var_items


def form_number_response_html(all_found_data, phone_num):
    all_js_objs = ""
    filtered_data = filter_by_weight(all_found_data, "number")

    for i in range(len(filtered_data)):
        info: NumberInfo = filtered_data[i]
        title = info.title
        snippet = info.snippet
        uri = info.uri
        one_info = form_js_data(title, snippet, uri, [phone_num])

        all_js_objs += one_info

    filters = form_var_filters(keywords_from_user=[phone_num])
    items = form_var_items(all_obj=all_js_objs)

    return items, filters


def form_response_html(found_info_test) -> str:
    keywords_from_user = []
    all_js_objs, main_js_objs, free_js_objs, negative_js_objs = "", "", "", ""
    reputation_js_objs, relations_js_objs, soc_js_objs, doc_js_objs = "", "", "", ""

    neg_kwds, rep_kwds, rel_kwds, soc_kwds, doc_kwds = [], [], [], [], []

    filtered_data = filter_by_weight(found_info_test, "name")

    # простые счетчики категории
    main_c, free_c, neg_c, rep_c, rel_c, soc_c, doc_c = 0, 0, 0, 0, 0, 0, 0
    # счетики при ФИО для разных категории
    all_fio_c, free_fio_c, main_fio_c, neg_fio_c, rep_fio_c, rel_fio_c, soc_fio_c, doc_fio_c = 0, 0, 0, 0, 0, 0, 0, 0
    # счетики при ФИ для разных категории
    all_fi_c, free_fi_c, main_fi_c, neg_fi_c, rep_fi_c, rel_fi_c, soc_fi_c, doc_fi_c = 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(len(filtered_data)):
        info: FoundInfo = filtered_data[i]
        title = info.title
        snippet = info.snippet
        uri = info.uri
        weight = info.weight
        keyword_type = info.word_type.replace("company_", "")
        keywords_list = info.kwds_list
        kwd = info.kwd
        soc_type = info.soc_type
        doc_type = info.doc_type
        fullname = info.fullname

        one_info = form_js_data(title, snippet, uri, keywords_list, fullname)

        all_js_objs += one_info
        if fullname == 'true':
            all_fio_c += 1
        else:
            all_fi_c += 1

        if weight >= 3:
            main_js_objs += one_info
            main_c += 1
            if fullname == 'true':
                main_fio_c += 1
            else:
                main_fi_c += 1

        match keyword_type:
            case "free word":
                free_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                if kwd not in keywords_from_user:
                    keywords_from_user.append(kwd)

                free_c += 1
                if fullname == 'true':
                    free_fio_c += 1
                else:
                    free_fi_c += 1

            case "negativ":
                negative_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                neg_kwds.append(kwd)

                neg_c += 1
                if fullname == 'true':
                    neg_fio_c += 1
                else:
                    neg_fi_c += 1

            case "reputation":
                reputation_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                rep_kwds.append(kwd)

                rep_c += 1
                if fullname == 'true':
                    rep_fio_c += 1
                else:
                    rep_fi_c += 1

            case "relations":
                relations_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                rel_kwds.append(kwd)

                rel_c += 1
                if fullname == 'true':
                    rel_fio_c += 1
                else:
                    rel_fi_c += 1

        if soc_type:
            soc_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname, social_type=soc_type)
            soc_kwds.append(kwd)

            soc_c += 1
            if fullname == 'true':
                soc_fio_c += 1
            else:
                soc_fi_c += 1

        if doc_type:
            doc_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname, doc_type=doc_type)
            doc_kwds.append(kwd)

            doc_c += 1
            if fullname == 'true':
                doc_fio_c += 1
            else:
                doc_fi_c += 1

    filters = form_var_filters(
        keywords_from_user,
        neg_kwds,
        rep_kwds,
        rel_kwds,
        soc_kwds,
        doc_kwds,
    )
    items = form_var_items(
        all_obj=all_js_objs,
        main=main_js_objs,
        free=free_js_objs,
        negative=negative_js_objs,
        reputation=reputation_js_objs,
        relations=relations_js_objs,
        socials=soc_js_objs,
        documents=doc_js_objs,
    )

    fullname_counters = {
        "main": [
            main_c,
            main_fio_c,
            main_fi_c,
        ],
        "arbitrary": [
            free_c,
            free_fio_c,
            free_fi_c,
        ],
        "negative": [
            neg_c,
            neg_fio_c,
            neg_fi_c,
        ],
        "connections": [
            rel_c,
            rel_fio_c,
            rel_fi_c,
        ],
        "socials": [
            soc_c,
            soc_fio_c,
            soc_fi_c,
        ],
        "reputation": [
            rep_c,
            rep_fio_c,
            rep_fi_c,
        ],
        "documents": [
            doc_c,
            doc_fio_c,
            doc_fi_c,
        ],
        "all_materials": [
            len(filtered_data),
            all_fio_c,
            all_fi_c,
        ],
    }

    return items, filters, fullname_counters
