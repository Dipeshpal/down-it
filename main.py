from fastapi import FastAPI
import hammer_app
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def start_hammer_app():
    # Run hammer_app.start() in the background
    await asyncio.sleep(0)  # Allow the event loop to switch to other coroutines
    hammer_app.start()


# Default root endpoint
@app.get("/")
async def root():
    # Create a task to run start_hammer_app() in the background
    # asyncio.create_task(start_hammer_app())

    return templates.TemplateResponse("index.html", {"request": {}})


@app.get("/hack-it")
async def hack_it():
    # Create a task to run start_hammer_app() in the background
    asyncio.create_task(start_hammer_app())

    return templates.TemplateResponse("hack-it.html", {"request": {}})

if __name__ == "__main__":
    # Run the templates
    os.system("uvicorn main:app --reload")
