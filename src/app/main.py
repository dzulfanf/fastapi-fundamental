from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
  title="FastAPI Fundamental",
  description="A simple API for learning Python and FastAPI",
  version="0.1.0"
)

class ItemCreate(BaseModel):
  name: str
  description: str = ""

items: dict[int, dict] = {}
next_item_id = 1


@app.get("/")
def read_root():
  return { "message": "Hello, FastAPI!" }


@app.get("/health")
def health_check():
  return { "status": "ok" }


@app.post("/items", status_code=201)
def create_item(item: ItemCreate):
  global next_item_id

  item_id = next_item_id
  items[item_id] = {
    "id": item_id,
    "name": item.name,
    "description": item.description
  }

  next_item_id += 1

  return items[item_id]


@app.get("/items")
def list_items():
  return list(items.values())