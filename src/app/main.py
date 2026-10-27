from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
  title="FastAPI Fundamental",
  description="A simple API for learning Python and FastAPI",
  version="0.1.0"
)

class ItemCreate(BaseModel):
  name: str
  description: str = ""

class ItemUpdate(BaseModel):
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


@app.get("/items/{item_id}")
def get_item(item_id: int):
  item = items.get(item_id)

  if item is None:
    raise HTTPException(
      status_code=404,
      detail="Item not found"
    )

  return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate):
  existing_item = items.get(item_id)

  if existing_item is None:
    raise HTTPException(
      status_code=404,
      detail="Item not found"
    )

  updated_item = {
    "id": item_id,
    "name": item.name,
    "description": item.description
  }

  items[item_id] = updated_item

  return updated_item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
  if item_id not in items:
    raise HTTPException(
      status_code=404,
      detail="Item not found",
    )

  del items[item_id]
  return None