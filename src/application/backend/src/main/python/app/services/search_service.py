from fuzzywuzzy import fuzz
from ..models.operator import Operator

class SearchService:
    def __init__(self, operator_repository):
        self.repo = operator_repository
    
    def search_operators(self, query: str, limit: int = 10):
        operators = self.repo.get_all_operators()
        
        # Aplica busca fuzzy nos campos relevantes
        scored_operators = []
        for op in operators:
            name_score = fuzz.token_set_ratio(query, op.razao_social)
            fantasy_score = fuzz.token_set_ratio(query, op.nome_fantasia or "")
            city_score = fuzz.token_set_ratio(query, op.cidade or "")
            
            max_score = max(name_score, fantasy_score, city_score)
            if max_score > 50:  # Limiar mínimo de relevância
                scored_operators.append((max_score, op))
        
        # Ordena por score e limita resultados
        scored_operators.sort(key=lambda x: x[0], reverse=True)
        return [op for score, op in scored_operators[:limit]]