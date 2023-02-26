from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import users, mailboxes
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base, engine
import uvicorn

app = FastAPI()
app.router.redirect_slashes = False
'''
CORS
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]
)


app.include_router(users.router)
# 수훈 작업 라우터
app.include_router(mailboxes.router)

@app.get("/database",
         description = "This is a database creation confirmation API. \
             If there is no database table that references the model, it is created."
         )
async def root():
    Base.metadata.create_all(bind=engine)
    return {"message" : "find database"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)