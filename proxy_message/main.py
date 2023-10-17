from telethon import TelegramClient, events
from config import settings
from proxy_message.kafka_sender import send_cases_to_kafka


async def wait_for_message_from_user(client, user_id):  # функция которая ждет сообщение от пользователя
    try:
        await client.start()
        client.add_event_handler(lambda event: send_cases_to_kafka(event), events.NewMessage(chats=user_id))
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        await client.disconnect()


def main():
    client = TelegramClient(
        settings.name_session,
        settings.api_id,
        settings.api_hash,
        system_version=settings.system_version,
        device_model=settings.device_model,
        app_version=settings.app_version
    )

    chat_username = settings.message_username

    with client:  # функция которая ждет сообщение от пользователя
        client.loop.run_until_complete(wait_for_message_from_user(client, settings.message_username))


if __name__ == '__main__':
    main()