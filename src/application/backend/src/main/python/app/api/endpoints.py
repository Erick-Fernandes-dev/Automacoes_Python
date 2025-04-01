from fastapi import APIRouter, Query, Depends
from ..services.search_service import SearchService
from ..repositories.operator_repository import OperatorRepository

router = APIRouter()

def get_search_service():
    service = SearchService()
    try:
        yield service
    finally:
        del service

@router.get("/search")
async def search_operators(
    query: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, gt=0, le=100, description="Limite de resultados"),
    service: SearchService = Depends(get_search_service)
):
    results = service.search_operators(query, limit)
    return {"query": query, "results": results}