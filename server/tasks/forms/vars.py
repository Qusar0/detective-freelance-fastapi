def form_var_items(
    all_obj="",
    main="",
    free="",
    negative="",
    reputation="",
    relations="",
    socials="",
    documents="",
):
    items = {
        "all": all_obj,
        "main": main,
        "free": free,
        "negative": negative,
        "reputation": reputation,
        "relation": relations,
        "socials": socials,
        "documents": documents
    }
    return items

def form_var_filters(
    keywords_from_user="",
    neg_kwds="",
    rep_kwds="",
    rel_kwds="",
    soc_kwds="",
    doc_kwds="",
):
    kwds_objects, neg_objects, rep_objects, rel_objects, soc_objects, doc_objects = "", "", "", "", "", ""

    for kwd in keywords_from_user:
        kwds_objects += f"'{kwd}': true,\n"

    for neg_kwd in list(set(neg_kwds)):
        neg_objects += f"'{neg_kwd}': true,\n"

    for rep_kwd in list(set(rep_kwds)):
        rep_objects += f"'{rep_kwd}': true,\n"

    for rel_kwd in list(set(rel_kwds)):
        rel_objects += f"'{rel_kwd}': true,\n"

    for soc_kwd in list(set(soc_kwds)):
        soc_objects += f"'{soc_kwd}': true,\n"

    for doc_kwd in list(set(doc_kwds)):
        doc_objects += f"'{doc_kwd}': true,\n"

    all_kwds = f"{kwds_objects}{neg_objects}{rep_objects}{rel_objects}{soc_objects}{doc_objects}"
    filters = {
        "free_kwds": kwds_objects,
        "neg_kwds": neg_objects,
        "rep_kwds": rep_objects,
        "rel_kwds": rel_objects,
        "soc_kwds": soc_objects,
        "doc_kwds": doc_objects,
        "all_kwds": all_kwds,
    }

    return filters
