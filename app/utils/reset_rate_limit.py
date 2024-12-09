import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)


def reset_user_limit(ip, route):
    key_pattern = f"LIMITS:LIMITER/{ip}/{route}*"

    keys = redis_client.keys(key_pattern)

    for key in keys:
        redis_client.delete(key)
        print(f"Deleted rate limit key: {key.decode()}")
