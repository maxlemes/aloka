import yfinance as yf
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import json
import os

def capturar_dados_fundo(link: str):
    url = f"https://statusinvest.com.br/fundos-de-investimento/{link}"

    xpath_nome = "/html/body/main/header/div[2]/div/div[1]/h1"
    xpath_cota = "/html/body/main/div[2]/div/div/div[6]/div/div/strong"
    xpath_cnpj = "/html/body/main/div[4]/div/div[1]/div/div/div[1]/h5[2]"


    # Configura o Firefox em modo headless (sem abrir a janela)
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)

    driver.get(url)

    # Aguarda carregar (você pode ajustar com waits explícitos depois)
    time.sleep(5)

    # Exemplo: pegar nome do fundo
    nome = driver.find_element(By.XPATH, xpath_nome).text
    cota = driver.find_element(By.XPATH, xpath_cota).text
    cnpj = driver.find_element(By.XPATH, xpath_cnpj).text

    # Converte a cota de string para número, substituindo a vírgula por ponto
    cota = float(cota.replace(',', '.'))

    dados = {
        "link": link,
        "nome": nome,
        "cnpj": cnpj,
        "valor": cota
    }

    # Cria a pasta 'data' se não existir
    os.makedirs("data", exist_ok=True)

    # Caminho do arquivo JSON
    caminho_arquivo = os.path.join("data", f"{link}.json")

    # Salva os dados em formato JSON
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print(f"Dados salvos em: {caminho_arquivo}")

def atualizar_cota(dados_principais, pasta="data"):
    # Caminho para o diretório onde os arquivos JSON estão armazenados
    for fundo in dados_principais:
        arquivo_json = os.path.join(pasta, f"{fundo['link']}.json")
        
        # Verifica se o arquivo existe
        if os.path.exists(arquivo_json):
            # Abre o arquivo do fundo
            with open(arquivo_json, "r", encoding="utf-8") as f:
                dados_fundo = json.load(f)

            # Pega o valor de cota e adiciona ao dado principal
            fundo["valor"] = dados_fundo.get("valor")
            
            # Após a atualização das cotas, exclui o arquivo
            os.remove(arquivo_json)
            
        else:
            print(f"Arquivo {arquivo_json} não encontrado!")
    
    return dados_principais

def salvar_dados(dados_principais, caminho_arquivo):
    # Salva os dados atualizados de volta no arquivo JSON
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados_principais, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos no arquivo {caminho_arquivo}")

# Função principal para ler o arquivo pgbl.json
def ler_dados_principais(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados

# Exemplo de como usar
if __name__ == "__main__":

    fundos = ["sf2-tropico-cash-fim", 
             "real-investor-70-previdencia-fim",
             "sul-america-prev-fic-fi-rf-cp",
             "verde-am-icatu-prev-fic-fim-prev",
             "acs-mag-prev-cash-fundo-de-investimento-em-cotas-de-fundo-de-investimento-renda-fixa"
              ]
    
    # Configura o Firefox em modo headless (sem abrir a janela)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    
    # Captura os dados de todos os fundos
    for fundo in fundos:
        capturar_dados_fundo(fundo)

    driver.quit()
    
    arquivos = ["data/rendafixa.json", "data/pgbl.json"]

    for caminho_arquivo in arquivos:
    
        # Lê os dados principais do arquivo pgbl.json
        dados_principais = ler_dados_principais(caminho_arquivo)
        
        # Atualiza os dados principais com o valor de cota
        dados_atualizados = atualizar_cota(dados_principais)

        # Salva os dados atualizados no arquivo
        salvar_dados(dados_atualizados, caminho_arquivo)

        # Imprime os dados atualizados
        for fundo in dados_atualizados:
            print(json.dumps(fundo, indent=4, ensure_ascii=False))