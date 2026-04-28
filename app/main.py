from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Procurement Risk API",
    description="API for processing procurement data and detecting invoice risk signals",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Procurement Risk API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}