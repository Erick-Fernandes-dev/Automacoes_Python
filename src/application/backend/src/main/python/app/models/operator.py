from pydantic import BaseModel

class Operator(BaseModel):
    registro_ans: str
    cnpj: str
    razao_social: str
    nome_fantasia: str | None
    modalidade: str
    logradouro: str
    numero: str
    complemento: str | None
    bairro: str
    cidade: str
    uf: str
    cep: str
    ddd: str | None
    telefone: str | None
    fax: str | None
    endereco_eletronico: str | None
    representante: str | None
    cargo_representante: str | None
    regiao_de_comercializacao: str | None
    data_registro_ans: str