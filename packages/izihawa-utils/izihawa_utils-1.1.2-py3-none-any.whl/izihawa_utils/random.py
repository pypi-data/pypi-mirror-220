import random
import string


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_request_id(length: int = 12):
    return random_string(length)


async def reservoir_sampling_async(async_iterator, n):
    pool = []
    async for i in async_iterator:
        if i < n:
            pool.append(i)
        else:
            r = random.randint(0, i)
            if r < n:
                pool[r] = i
    return pool