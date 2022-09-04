from database import get_session, create_db_and_tables
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel, Session, select

#from .endpoints.gems import router as gem_router

import endpoints.gems as gem_endpoints
import endpoints.user as user_endpoints


app = FastAPI()

app.include_router(gem_endpoints.router)
app.include_router(user_endpoints.router)

engine = create_engine('sqlite:///database.db', echo=True)


@app.on_event('startup')
async def startup():
    create_db_and_tables()


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
