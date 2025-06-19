# event dao
async def save_event(data: str, query_id: int, db: AsyncSession):
    now = datetime.now()

    user_query = Events(
        event_type="test",
        query_id=query_id,
        created_time=now,
        additional_data=data,
        event_status="unseen"
    )

    db.add(user_query)
    await db.commit()
    await db.refresh(user_query)

    return user_query.event_id, user_query.event_type, user_query.created_time, user_query.event_status