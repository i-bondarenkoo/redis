from fastapi import FastAPI
import uvicorn
from router.singer import router as singer_router

app = FastAPI(title="Redis?!")
app.include_router(singer_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
