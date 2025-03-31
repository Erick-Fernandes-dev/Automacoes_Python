from unittest import TestCase as tc
import unittest
from unittest.mock import patch, mock_open, MagicMock
from web_scraping.main import WebScraper as wb
import os

#url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

class TestWebScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
        cls.download_dir = "test_downloads"
        
        # Criar diretório de teste
        os.makedirs(cls.download_dir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Limpar arquivos de teste
        for f in os.listdir(cls.download_dir):
            os.remove(os.path.join(cls.download_dir, f))
        os.rmdir(cls.download_dir)

    def setUp(self):
        self.scraper = wb(self.test_url)
        self.scraper.driver = MagicMock()  # Mock do driver

    def test_init(self):
        """Testa a inicialização da classe"""
        self.assertEqual(self.scraper.url, self.test_url)
        self.assertIsNone(self.scraper.driver)

    @patch('selenium.webdriver.Firefox')
    def test_start_browser_success(self, mock_firefox):
        """Testa o início bem-sucedido do navegador"""
        mock_firefox.return_value.title = "Atualização do Rol de Procedimentos"
        result = self.scraper.start_browser()
        self.assertTrue(result)
        self.assertIsNotNone(self.scraper.driver)

    @patch('selenium.webdriver.Firefox')
    def test_start_browser_failure(self, mock_firefox):
        """Testa falha ao iniciar o navegador"""
        mock_firefox.side_effect = Exception("Erro de conexão")
        result = self.scraper.start_browser()
        self.assertFalse(result)

    
    def test_close_browser(self):
        """Testa o fechamento do navegador"""
        self.scraper.driver.close = MagicMock()
        self.scraper.close_browser()
        self.scraper.driver.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()