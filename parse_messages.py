import asyncio
from telethon import TelegramClient
from models import session, Message
from env import API_ID, API_HASH, PHONE_NUMBER


client = TelegramClient("parser", API_ID, API_HASH)


async def main():
    await client.start(PHONE_NUMBER)
    print("Client Created")

    dialogs = await client.get_dialogs()
    private_chats = [dialog for dialog in dialogs if dialog.is_user]

    for chat in private_chats:
        last_saved_message = session.query(Message).filter_by(user_id=chat.id).order_by(Message.date.desc()).first()
        last_message_id = last_saved_message.id if last_saved_message else 0

        async for message in client.iter_messages(chat.id, min_id=last_message_id):
            sender = await message.get_sender()

            message_id = message.id
            user_id = sender.id
            first_name = sender.first_name
            last_name = sender.last_name
            username = sender.username
            phone_number = sender.phone
            message_text = message.message
            date = message.date

            if session.query(Message).filter_by(id=message_id).first():
                continue

            db_message = Message(
                id=message_id,
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone=phone_number,
                date=date,
                text=message_text
            )

            session.add(db_message)
            session.commit()

            print(f"Saved message from {first_name} {last_name} ({username}): {message_text}")

    await client.disconnect()
    print("Client Disconnected")

# Запуск
if __name__ == '__main__':
    asyncio.run(main())
