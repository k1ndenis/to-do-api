from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import lists, tasks

app = FastAPI(title="To-Do API",
    description="API для управления to-do списками",
    version="1.0.0",
    contact={"name": "Denis", "email": "k1ndenis.dev@gmail.com"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lists.router, prefix="/api", tags=["Lists"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API"}