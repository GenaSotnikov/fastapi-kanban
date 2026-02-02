from database.engine import DatabaseConnection
from typing import Annotated
from fastapi import status

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from routers import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

@app.get('/health')
def health_check(session: Annotated[DatabaseConnection, Depends()]):
    is_db_alive = session.health_check()
    if not is_db_alive:
        raise HTTPException(503, { 'status': 'down', 'reason': 'Database is unavailable' })
    return { 'status': 'ok' }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.get("/security/", tags = ['test'])
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/items/", response_model=dict, status_code=status.HTTP_200_OK, tags = ['test'], summary="Create an item123", response_description="The created item")
async def create_item(item: dict):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item