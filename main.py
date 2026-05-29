from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import lists, tasks
from app.core.database import lifespan

app = FastAPI(
    title="To-Do API",
    description="API для управления to-do списками",
    version="1.0.0",
    contact={"name": "Denis", "email": "k1ndenis.dev@gmail.com"},
    lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lists.router, prefix="/api", tags=["Lists"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API"}