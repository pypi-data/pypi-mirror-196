import os

from spt_factory import MongoFactory


if __name__ == '__main__':
    print(os.getenv('SSLROOT'))
    f = MongoFactory(
        mongo_url=os.getenv('MONGO_URL'),
        tlsCAFile=os.getenv('SSLROOT'),
    )
    bot_credes = f.get_any_credentials(type='core_inforeason_monitoring_bot')
    bot = f.get_telegram_alerts(**bot_credes)
    bot.send_message('test message')

