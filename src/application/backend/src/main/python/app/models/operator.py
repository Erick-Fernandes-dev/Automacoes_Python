from sqlalchemy import Column, String, Integer
from ..database import Base

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, index=True)
    registro_ans = Column(String, unique=True, index=True)
    cnpj = Column(String, unique=True)
    razao_social = Column(String)
    nome_fantasia = Column(String, nullable=True)
    modalidade = Column(String)
    logradouro = Column(String)
    numero = Column(String)
    complemento = Column(String, nullable=True)
    bairro = Column(String)
    cidade = Column(String)
    uf = Column(String)
    cep = Column(String)
    ddd = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    endereco_eletronico = Column(String, nullable=True)
    representante = Column(String, nullable=True)
    cargo_representante = Column(String, nullable=True)
    regiao_de_comercializacao = Column(String, nullable=True)
    data_registro_ans = Column(String)