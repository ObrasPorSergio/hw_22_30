from typing import List

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import json
from sqlalchemy.future import select
from sqlalchemy import desc

import models
import schemas
from database import engine, session

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.on_event("startup")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.post('/add/', response_model=schemas.RecipieOut)
async def recipies(recipie: schemas.RecipieIn) -> models.Recipie:
    """This endpoint creates new recipie in DB"""
    new_recipie = models.Recipie(**recipie.dict())
    async with session.begin():
        session.add(new_recipie)
    return new_recipie


@app.delete('/delete/{recipie_id}/')
async def recipies(recipie_id) -> json:
    """This endpoint deletes recipie from DB"""
    async with session.begin():
        current_recipie = await session.get(models.Recipie, recipie_id)
        await session.delete(current_recipie)
    return {'message': 'successfully deleted'}


@app.get('/', response_model=List[schemas.RecipieOut])
async def recipies(request: Request) -> templates.TemplateResponse:
    """This endpoint returns list of recipies"""
    res = await session.execute(select(models.Recipie).
                                order_by(desc(models.Recipie.count), models.Recipie.time))
    recipies = res.scalars().all()
    return templates.TemplateResponse('list.html',
                                      {'request': request, 'recipies': recipies})


@app.get('/{recipie_id}/', response_model=List[schemas.RecipieOut])
async def recipies(request: Request, recipie_id) -> templates.TemplateResponse:
    """This endpoint returns detail page of recipie"""
    current_recipie = await session.get(models.Recipie, recipie_id)
    current_recipie.count += 1
    session.add(current_recipie)
    await session.commit()
    return templates.TemplateResponse('detail.html', {'request': request, 'recipie': current_recipie})
