from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db


DbDep = Annotated[Session, Depends(get_db)]
