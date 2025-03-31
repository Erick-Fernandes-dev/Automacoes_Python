from fastapi import APIRouter, Query
from ..services.search_service import SearchService
from ..repositories.operator_repository import OperatorRepository

router = APIRouter()
repo = OperatorRepository()
search_service = SearchService(repo)

@router.get("/search")
async def search_operators(
    query: str = Query(..., min_length=2, description="Termo de busca"),
    limit: int = Query(10, gt=0, le=100, description="Limite de resultados")
):
    results = search_service.search_operators(query, limit)
    return {"query": query, "results": results}