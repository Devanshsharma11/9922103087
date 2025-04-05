from fastapi import FastAPI, HTTPException
import httpx
from collections import deque
from typing import List, Optional

app = FastAPI()

WINDOW_SIZE = 10
VALID_IDS = {
    "p": "primes",
    "f": "fibo",
    "e": "even",
    "r": "rand"
}

number_window = deque(maxlen=WINDOW_SIZE)
BASE_URL = "http://20.244.56.144/evaluation-service" 

async def fetch_numbers(numberid: str) -> List[int]:
    try:
        async with httpx.AsyncClient(timeout=2.0) as client: 
            response = await client.get(f"{BASE_URL}/{VALID_IDS[numberid]}")
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or "numbers" not in data:
                return []
            numbers = data["numbers"]
            if not isinstance(numbers, list):
                return []
            return [num for num in numbers if isinstance(num, (int, float))]
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
        return []

@app.get("/numbers/{numberid}")
async def get_numbers(numberid: str):
    if numberid not in VALID_IDS:
        raise HTTPException(status_code=400, detail="Invalid number ID")

    window_prev = list(number_window)
    numbers_fetched = await fetch_numbers(numberid)
    for num in numbers_fetched:
        if num not in number_window:
            number_window.append(num)

    window_curr = list(number_window)
    avg = 0.0
    if window_curr:
        try:
            avg = round(sum(window_curr) / len(window_curr), 2)
        except (TypeError, ZeroDivisionError):
            avg = 0.0

    return {
        "windowPrevState": window_prev,
        "windowCurrState": window_curr,
        "numbers": numbers_fetched,
        "avg": avg
    }