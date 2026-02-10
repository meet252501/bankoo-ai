import asyncio
import httpx
import logging
import time

logging.basicConfig(level=logging.INFO)

TOKEN = "8240626645:AAEV8qni7ITDDkRYxVQAofAzjwXAeRozgqg"
URL = f"https://api.telegram.org/bot{TOKEN}/getMe"

async def main():
    print(f"Testing connection to {URL}...")
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(URL)
            end_time = time.time()
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
            print(f"Time taken: {end_time - start_time:.2f}s")
    except Exception as e:
        end_time = time.time()
        print(f"Error: {e}")
        print(f"Time taken before error: {end_time - start_time:.2f}s")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
