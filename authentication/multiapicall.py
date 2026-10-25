
import asyncio
import httpx

from fastapi import FastAPI, HTTPException

app = FastAPI()


async def fetch_api(client, url):
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


@app.get("/combined-data")
async def combined_data():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
        "https://jsonplaceholder.typicode.com/comments/1",
    ]

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            result1, result2, result3 = await asyncio.gather(
                fetch_api(client, urls[0]),
                fetch_api(client, urls[1]),
                fetch_api(client, urls[2]),
            )

        return {
            "api1": result1,
            "api2": result2,
            "api3": result3,
        }

    except (httpx.HTTPError, asyncio.TimeoutError) as exc:
        raise HTTPException(
            status_code=502,
            detail="An external API request failed",
        ) from exc
