from fastapi import FastAPI

app = FastAPI(
  title="FastAPI Fundamental",
  description="A simple API for learning Python and FastAPI",
  version="0.1.0"
)

@app.get("/")
def read_root():
  return { "message": "Hello, FastAPI!" }

@app.get("/health")
def health_check():
  return { "status": "ok" }