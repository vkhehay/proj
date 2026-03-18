import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import Base
from .database import engine
from .routers import posts, auth, votes, users


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)


@app.get('/')
def root():
    return {"message": "Hello, pushing to ubuntu"}


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True)
