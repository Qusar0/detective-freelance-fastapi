# progibited dao
async def add_sites_from_db(user_prohibited_sites: list, db) -> list:
    result = await db.execute(select(ProhibitedSites.site_link))
    sites_from_db = result.scalars().all()

    return list(set(sites_from_db + user_prohibited_sites))