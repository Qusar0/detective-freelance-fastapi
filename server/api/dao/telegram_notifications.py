# telegram dao
async def save_user_and_chat(user_id, chat_id, db):
    result = await db.execute(
        select(TelegramNotifications).filter_by(user_id=user_id, chat_id=chat_id)
    )
    existing_chat = result.scalar_one_or_none()

    if existing_chat:
        return False

    db.add(
        TelegramNotifications(
            user_id=user_id,
            chat_id=chat_id,
        ),
    )
    await db.commit()

    return True


# telegram dao
async def is_user_subscribed_on_tg(user_id, db):
    result = await db.execute(
        select(TelegramNotifications).filter_by(user_id=user_id)
    )
    user = result.scalar_one_or_none()

    return user.chat_id if user else False