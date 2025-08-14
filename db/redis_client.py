# файл для подключения к redis
from redis.asyncio import Redis

# создаем объект клиента, который будет отправлять команды на сервер Redis
redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)
