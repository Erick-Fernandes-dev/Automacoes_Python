from selenium import webdriver as wb
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger as log
import os
from urllib.request import urlretrieve
import zipfile
from datetime import datetime as dt


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        
    
    # Essa função aqui vai iniciar o navegador
    # e acessar a URL desejada
    def start_browser(self):
        try:
            log.info("Iniciando o navegador")
            options = wb.FirefoxOptions()
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.dir", "/home/wolf/Downloads")
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
            
            log.info("Iniciando o navegador Firefox com configurações de download")
            self.driver = wb.Firefox(options=options)
            
            self.driver.get(self.url)
            log.info(f"Acessando a URL: {self.url}")

            #self.driver.maximize_window()
            #log.info("Maximizando a tela")
            
            #log.info(f"Título atual: {self.driver.title}")
            #log.info(f"URL atual: {self.driver.current_url}")


            # Fazendo uma verificação mais robusta do título da página
            WebDriverWait(self.driver, 10).until(
                EC.title_contains("Atualização do Rol de Procedimentos")
            )
            log.debug("Título da página verificado com sucesso")

            log.debug("Função executada com sucesso")
            #self.driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/main/div[2]/div/div/div/div/div[2]/div/ol/li[1]/a[1]").click()

        except Exception as e:
            log.error(f"Erro ao iniciar o navegador: {str(e)}")
            if self.driver:
                self.driver.quit()
            return False

    def get_anexos(self, download_dir="downloads"):
        """Baixa os anexos usando urllib (biblioteca padrão)"""
        try:
            os.makedirs(download_dir, exist_ok=True)
            
            # Localiza os links dos anexos
            anexo_i = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Anexo I') and contains(@href, '.pdf')]"))
            )
            anexo_ii = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(., 'Anexo II') and contains(@href, '.pdf')]"))
            )

            # Obtém URLs
            url_i = anexo_i.get_attribute('href')
            url_ii = anexo_ii.get_attribute('href')

            # Faz o download
            urlretrieve(url_i, os.path.join(download_dir, "Anexo_I.pdf"))
            urlretrieve(url_ii, os.path.join(download_dir, "Anexo_II.pdf"))
            
            return True

        except Exception as e:
            log.error(f"Erro ao baixar anexos: {str(e)}")
            return False

    
    def close_browser(self):
        log.info("Fechando o navegador")
        if self.driver:
            self.driver.close()
            log.debug("Navegador fechado com sucesso")

    # Função que vaI ZIPAR os anexos
    def zip_anexos(self, download_dir="downloads", output_dir="output"):

        try:
            # Cria diretório de saída se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            # Verifica se os anexos existem
            anexo_i_path = os.path.join(download_dir, "Anexo_I.pdf")
            anexo_ii_path = os.path.join(download_dir, "Anexo_II.pdf")
            
            if not all([os.path.exists(anexo_i_path), os.path.exists(anexo_ii_path)]):
                log.error("Arquivos dos anexos não encontrados para compactação")
                return None
            
            # Nome do arquivo ZIP com timestamp
            timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"Teste_ErickFernandesDeFariasSantos_{timestamp}.zip"
            zip_path = os.path.join(output_dir, zip_filename)
            
            # Cria o arquivo ZIP
            log.info(f"Criando arquivo ZIP: {zip_path}")
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(anexo_i_path, arcname="Anexo_I.pdf")
                zipf.write(anexo_ii_path, arcname="Anexo_II.pdf")
                log.success(f"Adicionados Anexo_I.pdf e Anexo_II.pdf ao ZIP")
            
            log.success(f"Compactação concluída: {zip_path}")
            return zip_path
            
        except Exception as e:
            log.error(f"Erro ao compactar anexos: {str(e)}")
            return None
    


if __name__ == "__main__":
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    scraper = WebScraper(url)

    try:
        scraper.start_browser()
        scraper.get_anexos()
        scraper.zip_anexos()
    except Exception as e:
        log.error(f"Erro durante a execução: {str(e)}")
    finally:
        scraper.close_browser()
        log.success("Execução finalizada com sucesso")
