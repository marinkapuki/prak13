from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db, Base, engine
from .models import Todo

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Создание таблиц в базе данных при старте приложения
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/todos/")
async def create_todo(title: str, description: str, db: AsyncSession = Depends(get_db)):
    new_todo = Todo(title=title, description=description)
    db.add(new_todo)
    await db.commit()
    await db.refresh(new_todo)
    return new_todo

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, title: str, description: str, completed: bool,
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = title
    todo.description = description
    todo.completed = completed
    
    await db.commit()
    await db.refresh(todo)
    
    return todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    await db.delete(todo)
    await db.commit()
    
    return {"message": "Todo deleted successfully"}
