from fastapi import FastAPI

app = FastAPI(
    title="GreenScape AI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "GreenScape AI Backend Running"
    }