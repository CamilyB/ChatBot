import os
import time
import re
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By

ARQUIVO_PROVIMENTO = "ultimo_provimento.txt"

# Configurações do Selenium
def configurar_navegador():
    pasta_download = os.getcwd()
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": pasta_download,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=options)

# Busca o link do PDF no site
def pegar_link_pdf():
    navegador = configurar_navegador()
    navegador.get("https://www.tjsc.jus.br/web/extrajudicial/normas-e-orientacoes")
    time.sleep(5)

    listas = navegador.find_elements(By.CLASS_NAME, "tjsc-style-unordered-list")

    link_pdf = None
    for lista in listas:
        itens = lista.find_elements(By.TAG_NAME, "li")
        for item in itens:
            if "Versão PDF para impressão" in item.text:
                link_pdf = item.find_element(By.TAG_NAME, "a").get_attribute("href")
                break

    navegador.quit()
    return link_pdf

# Faz o download e retorna o caminho do último PDF salvo
def baixar_pdf_com_selenium(url):
    pasta_download = os.getcwd()
    antes = set(os.listdir(pasta_download))

    navegador = configurar_navegador()
    navegador.get(url)
    time.sleep(10)  # espera o download terminar
    navegador.quit()

    depois = set(os.listdir(pasta_download))
    novos_arquivos = list(depois - antes)

    # procura pelo PDF novo
    pdfs = [f for f in novos_arquivos if f.lower().endswith(".pdf")]
    if not pdfs:
        print("❌ Nenhum PDF encontrado após o download.")
        return None

    nome_pdf = pdfs[0]
    print(f"✅ PDF baixado: {nome_pdf}")
    return os.path.join(pasta_download, nome_pdf)

# Extrai os provimentos da página 3 do PDF
def extrair_provimentos(arquivo_pdf):
    provimentos = []
    with pdfplumber.open(arquivo_pdf) as pdf:
        if len(pdf.pages) >= 3: # Cuidar quando o texto passar para a pag. 4, alterar para >= 3:
            pagina3 = pdf.pages[2] # Cuidar quando o texto passar para a pag. 4 (indice 3), alterar para [2,3]
            texto = pagina3.extract_text()
            if texto:
                provimentos = re.findall(r"Provimento n\. ?\d+", texto)

    numeros = [int(re.search(r"\d+", p).group()) for p in provimentos]
    return numeros

# Extrai quais artigos foram alterados pelo provimento
def extrair_artigos_alterados(arquivo_pdf, numero_provimento):
    artigos_encontrados = []

    padrao = re.compile(rf"Provimento n\. ?{numero_provimento}(.*?)(?=Provimento n\.|\Z)", re.DOTALL)

    with pdfplumber.open(arquivo_pdf) as pdf:
        texto_completo = ""
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() or ""

        trecho = padrao.search(texto_completo)
        if trecho:
            # procura por "art." ou "arts." dentro do trecho
            artigos = re.findall(r"art\. ?\d+", trecho.group(1))
            artigos_encontrados = artigos

    return artigos_encontrados

# Verifica se existe um provimento novo
def verificar_provimento_novo(provimentos, arquivo_pdf):
    if not provimentos:
        print("⚠ Nenhum provimento encontrado na página 3.")
        return

    ultimo_detectado = max(provimentos)
    print(f"📑 Último provimento no PDF: {ultimo_detectado}")

    if not os.path.exists(ARQUIVO_PROVIMENTO):
        with open(ARQUIVO_PROVIMENTO, "w") as f:
            f.write(str(ultimo_detectado))
        print("✅ Primeiro registro salvo.")
    else:
        with open(ARQUIVO_PROVIMENTO, "r") as f:
            ultimo_salvo = int(f.read().strip())

        if ultimo_detectado > ultimo_salvo:
            print(f"🚨 Novo provimento encontrado: {ultimo_detectado} (antes era {ultimo_salvo})")

            artigos = extrair_artigos_alterados(arquivo_pdf, ultimo_detectado)
            if artigos:
                print(f"📌 Artigos alterados pelo Provimento {ultimo_detectado}: {', '.join(artigos)}")
            else:
                print("⚠ Nenhum artigo encontrado para esse provimento.")

            with open(ARQUIVO_PROVIMENTO, "w") as f:
                f.write(str(ultimo_detectado))
        else:
            print("✅ Nenhum provimento novo.")

    # remove o PDF para não acumular
    os.remove(arquivo_pdf)
    print("🗑️ Arquivo PDF excluído após o processamento.")


# Fluxo principal

if __name__ == "__main__":
    print("🔎 Buscando link do PDF no site...")
    link_pdf = pegar_link_pdf()
    print("🔗 Link do PDF:", link_pdf)

    print("⬇ Baixando PDF com Selenium...")
    arquivo_pdf = baixar_pdf_com_selenium(link_pdf)

    if arquivo_pdf:
        print("📖 Lendo PDF e extraindo provimentos...")
        provimentos = extrair_provimentos(arquivo_pdf)
        print("📋 Todos os provimentos encontrados:", provimentos)
        verificar_provimento_novo(provimentos, arquivo_pdf)
