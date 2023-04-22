from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import users, mailboxes, Letters
from core.database import Base, engine
import uvicorn
from starlette.middleware.cors import CORSMiddleware as CORSMiddleware


app = FastAPI()
app.router.redirect_slashes = False
'''
CORS
'''
origins = [
    "*",
    "http://localhost:4000",
    "http://ec2-54-180-142-127.ap-northeast-2.compute.amazonaws.com:4000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"],
)


app.include_router(users.router)
app.include_router(mailboxes.router)
app.include_router(Letters.router)

@app.get("/database",
         description = "This is a database creation confirmation API. \
             If there is no database table that references the model, it is created."
         )
async def root():
    Base.metadata.create_all(bind=engine)
    return {"message" : "find database"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
