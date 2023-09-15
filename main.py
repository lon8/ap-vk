from fastapi import FastAPI
import uvicorn
from src.handlers import router

def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application

app = get_application()

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level='info')