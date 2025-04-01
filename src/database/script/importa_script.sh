#!/usr/bin/env bash
# importa_script.sh - Script de importação de dados para PostgreSQL
#
# Site: https://github.com/Erick-Fernandes-dev
# Autor: Erick Farias
# Manutenção: Erick Farias
#
# ------------------------------------------------------------------------ #
# Este script realiza a importação de dados para o PostgreSQL a partir de arquivos CSV
# seguindo a estrutura de diretórios pré-definida. Os dados incluem:
# - Cadastro de operadoras de saúde ativas
# - Demonstrações contábeis dos anos de 2023 e 2024
#
# Exemplo de uso:
#     $ ./importa_script.sh
#     Inicia o processo de importação dos dados para o banco PostgreSQL
#
# ------------------------------------------------------------------------ #
# Histórico:
# 
#    v1.0 31/03/2025, Erick Farias:
#       - Versão inicial do script de importação
#       - Implementação das funções básicas de importação
#
# ------------------------------------------------------------------------ #
# Testado em:
#   - bash 4.4.19
#   - PostgreSQL 13+
#   - Ubuntu 20.04 LTS
#
# ------------------------------------------------------------------------ #

# ------------------------------- VARIÁVEIS ----------------------------------------- #
# Configurações de diretórios e banco de dados
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/../../.." && pwd)
DATA_DIR="${PROJECT_ROOT}/src/database/arquivos"
DB_NAME="my_pgdb"
DB_USER="postgres"

# ------------------------------------------------------------------------ #

# ------------------------------- TESTES ----------------------------------------- #
# Configurações de tratamento de erros
set -e  # Encerra execução em caso de erro
set -u  # Verifica variáveis não definidas

# ------------------------------------------------------------------------ #

# ------------------------------- FUNÇÕES ----------------------------------------- #

# Verifica a estrutura de diretórios e arquivos necessários
verify_directories() {
    local required_dirs=(
        "${DATA_DIR}/2023"
        "${DATA_DIR}/2024"
    )
    
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            echo "Erro: Diretório não encontrado: $dir"
            exit 1
        fi
    done
    
    if [ ! -f "${DATA_DIR}/operadoras.csv" ]; then
        echo "Erro: Arquivo operadoras.csv não encontrado em ${DATA_DIR}"
        exit 1
    fi
}

# ------------------------------------------------------------------------ #

# ------------------------------- EXECUÇÃO ----------------------------------------- #
# Função principal que orquestra o processo de importação
main() {
    echo "Iniciando importação de dados..."
    echo "Diretório base: ${PROJECT_ROOT}"
    
    verify_directories

    # Importa dados cadastrais das operadoras
    echo "Importando dados das operadoras..."
    psql -U "${DB_USER}" -d "${DB_NAME}" -c "\copy operadoras FROM '${DATA_DIR}/operadoras.csv' DELIMITER ';' CSV HEADER ENCODING 'UTF8'"

    # Processa arquivos contábeis por ano
    for year in 2023 2024; do
        echo "Processando ano: ${year}..."
        for file in "${DATA_DIR}/${year}/"*.csv; do
            if [ -f "$file" ]; then
                echo "Importando: $(basename "$file")"
                psql -U "${DB_USER}" -d "${DB_NAME}" -c "\copy demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) FROM '${file}' DELIMITER ';' CSV HEADER ENCODING 'UTF8'"
            else
                echo "Aviso: Nenhum arquivo CSV encontrado em ${DATA_DIR}/${year}"
            fi
        done
    done

    echo "Importação concluída com sucesso!"
}

# Inicia execução do script
main

# ------------------------------------------------------------------------ #