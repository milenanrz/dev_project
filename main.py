
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Form, UploadFile, Depends, File
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from models import PhotographerSQL, PortfolioSQL
from terms import Nationality, PhotographicStyle, Genre
from database_connection import init_db, get_session
import operations as crud


@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
#app.mount("/photographer_images", StaticFiles(directory="photographer_images"), name="photographer_images")


@app.get("/")
async def root():
    return {"message": "Hello Photographers World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/error")
async def raise_exception():
    raise HTTPException(status_code=400)


#add photographers
@app.post("/photographers", response_model=PhotographerSQL, tags=["PHOTOGRAPHERS"])
async def add_photographer_img(name: str = Form(...),
                      genre: Optional[Genre] = Form(None),
                      nationality: Optional[Nationality] = Form(None),
                      photographic_style_name: Optional[PhotographicStyle] = Form(None),
                      is_alive:Optional[bool] = Form(None),
                      #photographer_image:Optional[UploadFile] = File(None),
                      session: Session = Depends(get_session)
                    ):

    #image_url = await upload_img_supabase(image)

    photographer_data=PhotographerSQL(
        name=name,
        genre=genre,
        nationality=nationality,
        photographic_style_name=photographic_style_name,
        is_alive=is_alive,
        #image_path=image_url
    )
    photographer = await crud.create_photographer(session, photographer_data)
    session.add(photographer)
    await session.commit()
    await session.refresh(photographer)
    return photographer

#show one photographer by id
@app.get("/photographers/{photographer_id}", response_model=PhotographerSQL, tags=["PHOTOGRAPHERS"])
async def read_photographer_img(photographer_id:int, session:Session = Depends(get_session)):
    photographer = await crud.get_photographer(session=session, photographer_id=photographer_id)
    if photographer is None:
        raise HTTPException(
            status_code=404,
            detail="Photographer not found"
        )
    return photographer

#Get all photographers
@app.get("/all_photographers", response_model=list[PhotographerSQL], tags=["PHOTOGRAPHERS"])
async def read_photographers_img(session:Session = Depends(get_session)):
    photographers = await crud.get_all_photographers(session=session)
    return photographers

#Update one photographer
@app.patch("/photographers/{photographer_id}", response_model=PhotographerSQL, tags=["PHOTOGRAPHERS"])
async def update_photographer_img(photographer_id:int, photographer_update:PhotographerSQL, session:Session=Depends(get_session)):
    photographer = await crud.update_photographer(session, photographer_id, photographer_update.dict(exclude_unset=True))
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found to update")
    return photographer

#photographer state
@app.patch("/photographer_state/{photographer_id}", response_model=PhotographerSQL, tags=["PHOTOGRAPHERS"])
async def change_state(photographer_id:int, session:Session=Depends(get_session)):
    photographer = await crud.mark_photographer_inactive(session, photographer_id)
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer

#filter genre
@app.get("/photographers_genre_filter/{photographer_genre}", response_model=list[PhotographerSQL], tags=["PHOTOGRAPHERS"])
async def get_photographer_genre(photographer_genre:Genre, session:Session=Depends(get_session)):
    photographer = await crud.filter_genre(session, photographer_genre)
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer


#filter nationality
@app.get("/photographers_nationality_filter/{photographer_nationality}", response_model=list[PhotographerSQL], tags=["PHOTOGRAPHERS"])
async def get_photographer_nationality(photographer_nationality:Nationality, session:Session=Depends(get_session)):
    photographer = await crud.filter_nationality(session, photographer_nationality)
    if photographer is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer


#add portfolio
@app.post("/portfolios", response_model=PortfolioSQL, tags=["PORTFOLIOS"])
async def add_portfolio_img(photographer_name: str = Form(...),
                      title: Optional[str] = Form(None),
                      category: Optional[PhotographicStyle] = Form(None),
                      created_at:Optional[int] = Form(None),
                      #photographer_image:Optional[UploadFile] = File(None),
                      session: Session = Depends(get_session)
                    ):

    #image_url = await upload_img_supabase(image)

    portfolio_data=PortfolioSQL(
        photographer_name=photographer_name,
        title=title,
        category=category,
        created_at=created_at,
        #image_path=image_url
    )
    portfolio = await crud.create_portfolio(session, portfolio_data)
    session.add(portfolio)
    await session.commit()
    await session.refresh(portfolio)
    return portfolio

#show one portfolio by id
@app.get("/portfolios/{portfolio_id}", response_model=PortfolioSQL, tags=["PORTFOLIOS"])
async def read_portfolio_img(portfolio_id:int, session:Session = Depends(get_session)):
    portfolio = await crud.get_portfolio(session=session, portfolio_id=portfolio_id)
    if portfolio is None:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )
    return portfolio

#Get all portfolios
@app.get("/all_portfolios", response_model=list[PortfolioSQL], tags=["PORTFOLIOS"])
async def read_portfolios_img(session:Session = Depends(get_session)):
    portfolios = await crud.get_all_portfolios(session=session)
    return portfolios

#Update one portfolio
@app.patch("/portfolios/{portfolio_id}", response_model=PortfolioSQL, tags=["PORTFOLIOS"])
async def update_portfolio_img(portfolio_id:int, portfolio_update:PortfolioSQL, session:Session=Depends(get_session)):
    portfolio = await crud.update_portfolio(session, portfolio_id, portfolio_update.dict(exclude_unset=True))
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found to update")
    return portfolio

@app.get("/portfolios_filter/{select_category}", response_model=list[PortfolioSQL], tags=["PORTFOLIOS"])
async def get_photographers_portfolios(select_category:PhotographicStyle, session:Session=Depends(get_session)):
    portfolio_category = await crud.filter_photographer_portfolio(session, select_category)
    if portfolio_category is None:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return portfolio_category