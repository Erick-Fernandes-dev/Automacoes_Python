import Data_transformtion as dt
from pathlib import Path
from loguru import logger as log
import os
from tqdm import tqdm

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
        transformer = dt.ANSDataTransformer(str(pdf_path))
        success = transformer.process("ErickFernandesDeFariasSantos")
        
        if success:
            log.info("Processo concluído com sucesso!")
        else:
            log.error("Ocorreu um erro durante o processamento")
    
    except Exception as e:
        log.error(f"Erro fatal: {str(e)}")