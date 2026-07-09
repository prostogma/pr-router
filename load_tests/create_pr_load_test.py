import asyncio
import time
import uuid

import httpx

URL = "http://localhost:8080/pullRequest/create"

TOTAL_REQUESTS = 100
CONCURRENT_REQUESTS = 10

AUTHOR_ID = "u1"


async def send_request(client: httpx.AsyncClient):
    payload = {
        "pull_request_id": str(uuid.uuid4()),
        "pull_request_name": "Load test",
        "author_id": AUTHOR_ID,
    }

    start = time.perf_counter()

    response = await client.post(URL, json=payload)

    stop = time.perf_counter() - start

    return response.status_code, stop


async def worker(client, semaphore, results):
    async with semaphore:
        results.append(await send_request(client))


async def main():
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    results = []

    async with httpx.AsyncClient(timeout=30) as client:
        tasks = [worker(client, semaphore, results) for _ in range(TOTAL_REQUESTS)]

        started = time.perf_counter()

        await client.post(
            "http://localhost:8080/team/add",
            json={
                "team_name": "backend",
                "members": [
                    {"user_id": "u1", "username": "Alice", "is_active": True},
                    {"user_id": "u2", "username": "Bob", "is_active": True},
                    {"user_id": "u3", "username": "John", "is_active": True},
                ],
            },
        )

        await asyncio.gather(*tasks)

        finished = time.perf_counter()

        success = sum(status == 201 for status, _ in results)
        failed = TOTAL_REQUESTS - success

        times = [t for _, t in results]

        print("=" * 40)
        print(f"Total requests : {TOTAL_REQUESTS}")
        print(f"Success        : {success}")
        print(f"Failed         : {failed}")
        print(f"Total time     : {finished-started:.3f} sec")
        print(f"Average        : {sum(times)/len(times):.3f} sec")
        print(f"Min            : {min(times):.3f} sec")
        print(f"Max            : {max(times):.3f} sec")
        print("=" * 40)


if __name__ == "__main__":
    asyncio.run(main())
