from sqlalchemy.orm import Session
from ..models.operator import Operator
from ..database import SessionLocal, engine
import csv
from pathlib import Path

# Cria as tabelas no banco de dados
Operator.metadata.create_all(bind=engine)

class OperatorRepository:
    def __init__(self):
        self.db = SessionLocal()
        self.load_data()
    
    def load_data(self):
        # Verifica se já existem dados para não duplicar
        if self.db.query(Operator).count() == 0:
            csv_path = Path(__file__).parent.parent.parent.parent / "resources" / "operadoras.csv"
            with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    try:
                        operator_data = {
                            'registro_ans': row['Registro_ANS'],
                            'cnpj': row['CNPJ'],
                            'razao_social': row['Razao_Social'],
                            'nome_fantasia': row['Nome_Fantasia'] if row['Nome_Fantasia'] else None,
                            'modalidade': row['Modalidade'],
                            'logradouro': row['Logradouro'],
                            'numero': row['Numero'],
                            'complemento': row['Complemento'] if row['Complemento'] else None,
                            'bairro': row['Bairro'],
                            'cidade': row['Cidade'],
                            'uf': row['UF'],
                            'cep': row['CEP'],
                            'ddd': row['DDD'] if row['DDD'] else None,
                            'telefone': row['Telefone'] if row['Telefone'] else None,
                            'fax': row['Fax'] if row['Fax'] else None,
                            'endereco_eletronico': row['Endereco_eletronico'] if row['Endereco_eletronico'] else None,
                            'representante': row['Representante'] if row['Representante'] else None,
                            'cargo_representante': row['Cargo_Representante'] if row['Cargo_Representante'] else None,
                            'regiao_de_comercializacao': row['Regiao_de_Comercializacao'] if row['Regiao_de_Comercializacao'] else None,
                            'data_registro_ans': row['Data_Registro_ANS']
                        }
                        operator = Operator(**operator_data)
                        self.db.add(operator)
                    except Exception as e:
                        print(f"Error processing row: {row}. Error: {e}")
                self.db.commit()
    
    def get_all_operators(self):
        return self.db.query(Operator).all()
    
    def search_operators(self, query: str, limit: int = 10):
        return self.db.query(Operator).filter(
            Operator.razao_social.ilike(f"%{query}%") |
            Operator.nome_fantasia.ilike(f"%{query}%") |
            Operator.cidade.ilike(f"%{query}%")
        ).limit(limit).all()
    
    def close(self):
        self.db.close()