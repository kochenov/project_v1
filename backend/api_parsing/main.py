from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="DreamManor",
    version="0.0.1",
)


@app.get("/")
def hello_index():
    return {
        "message": "Hello index!",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info", reload=True)
