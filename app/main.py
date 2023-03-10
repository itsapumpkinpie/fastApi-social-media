from fastapi import FastAPI
import uvicorn
from app.db import models
from app.db.сonnection import engine
from app.routers import post, user, auth
from app.config import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
