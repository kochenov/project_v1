import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# инициализация приложения
app = FastAPI(
    title="DreamManor Parser Avito",
    version="0.0.1",
)

origins = [
    "http://localhost:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info", reload=True)
