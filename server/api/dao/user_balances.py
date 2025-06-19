async def subtract_balance(user_id: int, amount: float, channel: str, db: AsyncSession):
    result = await db.execute(
        select(UserBalances)
        .filter_by(user_id=user_id),
    )
    user_balance = result.scalars().first()

    if not user_balance:
        return

    user_balance.balance = round(
        user_balance.balance + (-amount),
        2,
    )

    await db.commit()

    event_data = {
        "event_type": "balance",
        "balance": user_balance.balance,
    }

    await publish_event(channel, event_data)