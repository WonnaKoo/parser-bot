from telethon import TelegramClient, events
from env import API_ID, API_HASH, API_TOKEN_BOT
from models import Message, session

client = TelegramClient('view_bot_session', API_ID, API_HASH).start(bot_token=API_TOKEN_BOT)


@client.on(events.NewMessage(pattern='/latest'))
async def handle_message(event):
    messages = session.query(Message).order_by(Message.date.desc()).limit(10).all()

    response = "last 10 messages:\n"
    for msg in messages:
        response += (
            f"ID: {msg.user_id}, "
            f"First Name: {msg.first_name}, "
            f"Last Name: {msg.last_name}, "
            f"Username: {msg.username}, "
            f"Phone: {msg.phone}, Date: "
            f"{msg.date}, Text: "
            f"{msg.text}\n"
        )

    await event.respond(response)


def main():
    print("bot start")
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
