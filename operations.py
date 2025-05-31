from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from typing import Dict, Any
from models import PhotographerSQL, PortfolioSQL
from terms import Genre, PhotographicStyle, Nationality


#Creation of one photographer in DB
async def create_photographer(session: Session, photographer:PhotographerSQL):
    db_photographer = PhotographerSQL.model_validate(photographer, from_attributes=True)
    db_photographer.created_at = datetime.now() #new

    session.add(db_photographer)
    await session.commit()
    await session.refresh(db_photographer)

    return db_photographer

#Get photographer by the id
async def get_photographer(session:Session, photographer_id:int):
    return await session.get(PhotographerSQL, photographer_id)


#Get all photographers of the list
async def get_all_photographers(session:Session):
    query = select(PhotographerSQL)
    results = await session.exec(query)
    photographers = results.all()
    return photographers

#update photographer
async def update_photographer(session:Session, photographer_id:int, photographer_update:Dict[str, Any]):
    photographer = await session.get(PhotographerSQL, photographer_id)
    if photographer is None:
        return None

    photographer_data = photographer.dict()
    for key, value in photographer_update.items():
        if value is not None:
            photographer_data[key]=value

    photographer_data["updated_at"] = datetime.now() #new


    for key, value in photographer_data.items():
        setattr(photographer, key, value)

    session.add(photographer)
    await session.commit()
    await session.refresh(photographer)

    return photographer

#Modify photographer status.
async def mark_photographer_inactive(session:Session, photographer_id:int):
    return await update_photographer(session, photographer_id, {"is_alive":False})

#filter by genre
async def filter_genre(session:Session, photographer_genre:Genre):
    query = (select(PhotographerSQL).where(PhotographerSQL.genre == photographer_genre))
    result = await session.execute(query)

    genre = result.scalars().all()

    return genre

#filter by nacionality
async def filter_nationality(session:Session, photographer_nationality:Nationality):
    query = (select(PhotographerSQL).where(PhotographerSQL.nationality == photographer_nationality))
    result = await session.execute(query)
    nationality = result.scalars().all()
    return nationality


#Creation of one portfolio in DB
async def create_portfolio(session: Session, portfolio:PortfolioSQL):
    db_portfolio = PortfolioSQL.model_validate(portfolio, from_attributes=True)
    db_portfolio.created_at = datetime.now() #new

    session.add(db_portfolio)
    await session.commit()
    await session.refresh(db_portfolio)

    return db_portfolio

#Get portfolio by the id
async def get_portfolio(session:Session, portfolio_id:int):
    return await session.get(PortfolioSQL, portfolio_id)


#Get all portfolios of the list
async def get_all_portfolios(session:Session):
    query = select(PortfolioSQL)
    results = await session.exec(query)
    portfolios = results.all()
    return portfolios

#update portfolio
async def update_portfolio(session:Session, portfolio_id:int, portfolio_update:Dict[str, Any]):
    portfolio = await session.get(PortfolioSQL, portfolio_id)
    if portfolio is None:
        return None

    portfolio_data = portfolio.dict()
    for key, value in portfolio_update.items():
        if value is not None:
            portfolio_data[key]=value

    portfolio_data["updated_at"] = datetime.now()  # new

    for key, value in portfolio_data.items():
        setattr(portfolio, key, value)

    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)

    return portfolio


async def filter_photographer_portfolio(session:Session, select_category:PhotographicStyle):
    query = (select(PortfolioSQL).where(PortfolioSQL.category == select_category))
    result = await session.execute(query)
    portfolio_category = result.scalars().all()

    return portfolio_category