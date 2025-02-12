from typing import Union

from fastapi import APIRouter

router = APIRouter( prefix="/products",
                    tags=["products"],
                    responses={404: {"description": "Not found"}})


products_list = ["mochila", "zapatilla", "poleras", "straps"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]