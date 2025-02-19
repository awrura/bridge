import pytest
from fakeredis.aioredis import FakeRedis

from app.services.delivery.broker import RedisBrokerDelivery


class TestRedisDelivery:
    @pytest.mark.parametrize(
        'queue,matrix,data',
        [('hello', 'awrura', [(127, 127, 127)])],
    )
    @pytest.mark.asyncio
    async def test_send_pic(self, mocker, queue, matrix, data):
        redis = FakeRedis()
        conf = mocker.Mock(BROKER_QUEUE_NAME=queue)

        delivery = RedisBrokerDelivery(redis, conf)
        await delivery.send_pic(matrix, data)

        assert await redis.lpop(queue) is not None  # pyright: ignore[reportGeneralTypeIssues]

    @pytest.mark.parametrize(
        'queue,matrix,val',
        [('hello', 'awrura', 255)],
    )
    @pytest.mark.asyncio
    async def test_send_brightness(self, mocker, queue, matrix, val):
        redis = FakeRedis()
        conf = mocker.Mock(BROKER_QUEUE_NAME=queue)

        delivery = RedisBrokerDelivery(redis, conf)
        await delivery.send_brightness(matrix, val)

        assert await redis.lpop(queue) is not None  # pyright: ignore[reportGeneralTypeIssues]

    @pytest.mark.parametrize(
        'queue,matrix,val',
        [('hello', 'awrura', 256)],
    )
    @pytest.mark.asyncio
    async def test_send_brightness_out_of_range(self, mocker, queue, matrix, val):
        redis = FakeRedis()
        conf = mocker.Mock(BROKER_QUEUE_NAME=queue)

        delivery = RedisBrokerDelivery(redis, conf)

        with pytest.raises(ValueError):
            await delivery.send_brightness(matrix, val)
