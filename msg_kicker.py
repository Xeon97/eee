from datetime import timezone

# Преобразуем threshold в объект с временной зоной UTC
now = datetime.utcnow().replace(tzinfo=timezone.utc)
threshold = now - timedelta(days=days)

for user in participants.users:
    if user.bot or user.status is None:  # Пропускаем ботов и неизвестный статус
        continue

    last_seen = getattr(user.status, "was_online", None)
    if last_seen and last_seen < threshold:
        try:
            await self._client(EditBannedRequest(
                channel=chat_id,
                participant=user.id,
                banned_rights=ChatBannedRights(until_date=None, view_messages=True)
            ))
            kicked += 1
        except Exception as e:
            await message.reply(f"Ошибка при исключении {user.id}: {str(e)}")
