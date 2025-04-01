from ..repositories.operator_repository import OperatorRepository

class SearchService:
    def __init__(self):
        self.repo = OperatorRepository()
    
    def search_operators(self, query: str, limit: int = 10):
        return self.repo.search_operators(query, limit)
    
    def __del__(self):
        self.repo.close()