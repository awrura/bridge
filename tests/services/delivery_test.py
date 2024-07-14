import pytest
from fakeredis.aioredis import FakeRedis

from app.services.delivery.broker import RedisBrokerDelivery


class TestRedisDelivery:
    @pytest.mark.parametrize(
        'queue,matrix,data',
        [('hello', 'awrura', [(127, 127, 127)])],
    )
    @pytest.mark.asyncio
    async def test_send_message(self, mocker, queue, matrix, data):
        redis = FakeRedis()
        conf = mocker.Mock(BROKER_QUEUE_NAME=queue)

        delivery = RedisBrokerDelivery(redis, conf)
        await delivery.send(matrix, data)

        assert await redis.lpop(queue) is not None  # pyright: ignore[reportGeneralTypeIssues]
