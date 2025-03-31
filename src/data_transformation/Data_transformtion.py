import os
import pandas as pd
import pdfplumber
import zipfile
from pathlib import Path
from datetime import datetime
from loguru import logger as log
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
import logging

class ANSDataTransformer:
    def __init__(self, pdf_path):
        """Inicializa o transformador com o caminho do PDF"""
        self.pdf_path = str(Path(pdf_path).absolute())
        self.output_dir = str(Path(__file__).parent.parent / "output")
        self.column_mapping = {
            'OD': 'Seg. Odontológica',
            'AMB': 'Seg. Ambulatorial',
            'HCO': 'Seg. Hospitalar Com Obstetrícia',
            'HSO': 'Seg. Hospitalar Sem Obstetrícia',
            'REF': 'Plano Referência',
            'PAC': 'Procedimento Alta Complexidade',
            'DUT': 'Diretriz Utilização'
        }
        
        if not os.path.exists(self.pdf_path):
            available_files = "\n".join(os.listdir(Path(self.pdf_path).parent))
            raise FileNotFoundError(
                f"Arquivo PDF não encontrado em {self.pdf_path}\n"
                f"Arquivos disponíveis:\n{available_files}"
            )

    def extract_tables_from_pdf(self):
        """Extrai tabelas a partir da página 3 do PDF"""
        log.info(f"Iniciando extração de dados do PDF: {self.pdf_path}")
        all_tables = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                with logging_redirect_tqdm():
                    # Processa apenas a partir da página 3 (índice 2)
                    for page in tqdm(pdf.pages[2:], desc="Extraindo páginas", unit="página"):
                        # Configurações aprimoradas para extração de tabelas
                        table_settings = {
                            'vertical_strategy': 'lines',
                            'horizontal_strategy': 'lines',
                            'snap_tolerance': 5,
                            'join_tolerance': 10,
                            'edge_min_length': 15,
                            'text_x_tolerance': 2,
                            'text_y_tolerance': 2
                        }
                        
                        table = page.extract_table(table_settings)
                        
                        if table:
                            # Filtra cabeçalhos repetidos e linhas de legenda
                            if "PROCEDIMENTO" in table[0][0]:
                                header = table[0]
                                all_tables.append(header)
                                all_tables.extend(table[1:])
                            else:
                                all_tables.extend(table)
                            
                            # Adiciona uma linha vazia após cada página
                            empty_row = [''] * len(table[0])
                            all_tables.append(empty_row)
            
            if len(all_tables) > 0:
                log.success(f"Extraídas {len(all_tables)-1} linhas de dados")
                return all_tables
            else:
                log.error("Nenhuma tabela válida encontrada no PDF")
                return None
        
        except Exception as e:
            log.error(f"Erro ao extrair tabelas do PDF: {str(e)}")
            return None
    def clean_and_transform_data(self, raw_data):
        """Limpa e transforma os dados extraídos"""
        log.info("Iniciando transformação dos dados")
        
        try:
            if len(raw_data) < 2:
                raise ValueError("Dados insuficientes para transformação")
            
            # Cria DataFrame mantendo o cabeçalho original
            df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
            
            # Limpeza dos dados
            with logging_redirect_tqdm():
                # Remove linhas completamente vazias
                df = df.dropna(how='all')
                
                # Limpeza de strings e tratamento de multilinha
                for col in tqdm(df.columns, desc="Limpando colunas", leave=False):
                    df[col] = df[col].astype(str).str.strip().str.replace('\n', ' ')
                    df[col] = df[col].replace({'nan': '', 'None': ''})
                
                # Remove linhas com elementos da legenda
                df = df[~df.iloc[:, 0].str.contains('Legenda:|OD:|AMB:|HCO:|HSO:|REF:|PAC:|DUT:', na=False)]
                
                # Remove colunas vazias
                df = df.dropna(axis=1, how='all')
                
                # Renomeia colunas conforme estrutura conhecida
                df.columns = [
                    'PROCEDIMENTO', 
                    'RN_ALTERACAO', 
                    'VIGENCIA', 
                    'OD', 
                    'AMB', 
                    'HCO', 
                    'HSO', 
                    'REF', 
                    'PAC', 
                    'DUT', 
                    'SUBGRUPO', 
                    'GRUPO', 
                    'CAPITULO'
                ]
                
                # Substitui abreviações
                df = self._replace_abbreviations(df)
            
            log.success(f"Dados transformados com sucesso. Shape final: {df.shape}")
            return df
        
        except Exception as e:
            log.error(f"Erro ao transformar dados: {str(e)}")
            return None

    def _replace_abbreviations(self, df):
        """Substitui as abreviações conforme a legenda"""
        for col in self.column_mapping.keys():
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: self.column_mapping[col] if str(x).strip() == 'X' else ''
                )
        return df

    def save_to_csv(self, dataframe, filename="rol_procedimentos.csv"):
        """Salva os dados em arquivo CSV"""
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            csv_path = os.path.join(self.output_dir, filename)
            
            with logging_redirect_tqdm():
                with tqdm(total=100, desc="Salvando CSV") as pbar:
                    dataframe.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';')
                    pbar.update(100)
            
            log.success(f"CSV salvo em: {csv_path}")
            return csv_path
        except Exception as e:
            log.error(f"Erro ao salvar CSV: {str(e)}")
            return None

    def compress_csv(self, csv_path, your_name):
        """Compacta o arquivo CSV em um ZIP"""
        try:
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_path}")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"Teste_{your_name}_{timestamp}.zip"
            zip_path = os.path.join(self.output_dir, zip_filename)
            
            with logging_redirect_tqdm():
                with tqdm(total=100, desc="Compactando arquivo") as pbar:
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipf.write(csv_path, arcname=os.path.basename(csv_path))
                    pbar.update(100)
            
            log.success(f"Arquivo compactado: {zip_path}")
            return zip_path
        except Exception as e:
            log.error(f"Erro ao compactar arquivo: {str(e)}")
            return None

    def process(self, your_name):
        """Executa todo o fluxo de transformação"""
        log.info("Iniciando processo de transformação de dados")
        
        logging.basicConfig(handlers=[logging.StreamHandler()], level=logging.INFO)
        
        with logging_redirect_tqdm():
            with tqdm(total=4, desc="Processo completo") as main_pbar:
                raw_data = self.extract_tables_from_pdf()
                if raw_data is None:
                    return False
                main_pbar.update(1)
                
                df = self.clean_and_transform_data(raw_data)
                if df is None or df.empty:
                    return False
                main_pbar.update(1)
                
                csv_path = self.save_to_csv(df)
                if csv_path is None:
                    return False
                main_pbar.update(1)
                
                zip_path = self.compress_csv(csv_path, your_name)
                if zip_path is None:
                    return False
                main_pbar.update(1)
                
                return True


if __name__ == "__main__":
    try:
        log.remove()
        log.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
        
        project_root = Path(__file__).parent.parent
        pdf_path = project_root / "web_scraping" / "downloads" / "Anexo_I.pdf"
        
        if not pdf_path.exists():
            log.error(f"Arquivo PDF não encontrado em: {pdf_path}")
            exit(1)
        
        log.info(f"Iniciando processamento do arquivo: {pdf_path}")
        transformer = ANSDataTransformer(str(pdf_path))
        success = transformer.process("ErickFernandesDeFariasSantos")
        
        if success:
            log.info("Processo concluído com sucesso!")
        else:
            log.error("Ocorreu um erro durante o processamento")
    
    except Exception as e:
        log.error(f"Erro fatal: {str(e)}")