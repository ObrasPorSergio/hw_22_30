from pydantic import BaseModel


class BaseRecipie(BaseModel):
    """Schema for Recipie"""
    title: str
    time: int
    count: int
    ingredients: str
    description: str


class RecipieIn(BaseRecipie):
    ...


class RecipieOut(BaseRecipie):
    id: int

    class Config:
        orm_mode = True
