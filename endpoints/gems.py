from fastapi import APIRouter, Depends, HTTPException, status
from database import get_session
from sqlmodel import Session, select
import models.gems as gems


router = APIRouter()


@router.get("/gems")
async def get_gems(session: Session = Depends(get_session)):
    query = select(gems.Gem)
    result = session.exec(query)
    return result.all()


@router.get("/gems/{id}")
async def get_gem(id: int, session: Session = Depends(get_session)):
    try:
        query = session.get(gems.Gem, id)
        return query
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/gems", response_model=gems.GemOut)
async def add_gem(gem: gems.GemCreate, session: Session = Depends(get_session)):
    new_gem = gems.Gem(**gem.dict())
    session.add(new_gem)
    session.commit()
    session.refresh(new_gem)
    session.close()
    return new_gem


@router.patch("/gems{id}", response_model=gems.GemOut)
async def update_gem(id: int, gem: gems.GemUpdate, session: Session = Depends(get_session)):
    try:
        query = session.get(gems.Gem, id)
        gem_data = gem.dict(exclude_unset=True)
        for key, value in gem_data.items():
            setattr(query, key, value)
        session.add(query)
        session.commit()
        session.refresh(query)
        return query
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/gems/{id}")
async def delete_gem(id: int, session: Session = Depends(get_session)):
    try:
        query = session.get(gems.Gem, id)
        session.delete(query)
        session.commit()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
