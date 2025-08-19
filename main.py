from fastapi import FastAPI
import uvicorn
from router.singer import router as singer_router
import logging

app = FastAPI(title="Redis?!")
app.include_router(singer_router)

# общая настройка логов
# фабрика логов
logging.basicConfig(
    format="%(asctime)s %(name)5s  %(levelname)s : %(message)s",
    level=logging.DEBUG,
)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
