CREATE TABLE operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(50) NOT NULL,
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf CHAR(2) CHECK (uf IN ('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO')),
    cep VARCHAR(8),
    ddd CHAR(2),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    regiao_comercializacao VARCHAR(100),
    data_registro_ans DATE NOT NULL
);

COMMENT ON TABLE operadoras IS 'Dados cadastrais das operadoras de saúde ativas';


CREATE TABLE demonstracoes_contabeis (
    data DATE NOT NULL,
    reg_ans VARCHAR(20) NOT NULL REFERENCES operadoras(registro_ans),
    cd_conta_contabil VARCHAR(20) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    vl_saldo_inicial NUMERIC(15,2) NOT NULL,
    vl_saldo_final NUMERIC(15,2) NOT NULL,
    ano INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM data)) STORED,
    mes INT GENERATED ALWAYS AS (EXTRACT(MONTH FROM data)) STORED,
    PRIMARY KEY (data, reg_ans, cd_conta_contabil)
);

CREATE INDEX ON demonstracoes_contabeis(reg_ans);
CREATE INDEX ON demonstracoes_contabeis(data);