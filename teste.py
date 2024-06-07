import requests
from bs4 import BeautifulSoup
import pandas as pd

def request(url):
    try:
        response = requests.get(url)
        return response
    except ConnectionError:
        print("Erro de conexão. Verifique sua rede e o URL.")
    except TimeoutError:
        print("A solicitação demorou muito tempo para responder. Tente novamente mais tarde.")
    except Exception as ex:
        print(f"Erro inesperado: {ex}")
    
def raspar_dados(response):
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            nomes = []
            precos = []
            links = []
            for product in soup.find_all('div', class_='poly-card poly-card--grid'):
                nome = product.find('a').get_text()
                preco = product.find('span', class_='andes-money-amount__fraction').get_text()
                link = product.select_one('a')['href']
                nomes.append(nome)
                precos.append(preco)
                links.append(link)
            return nomes, precos, links
        else:
            print("Não foi possível acessar o site.")
    except Exception as erro:
            print(f'Erro inesperado {erro}')
              
def fazer_df(nomes, precos, links):
    data = {
                'Produto': nomes,
                'Preços': precos,
                'Links': links
            }
    df = pd.DataFrame(data)
    return df

url = 'https://www.mercadolivre.com.br/'
response = request(url)
nomes, precos, links = raspar_dados(response)
df = fazer_df(nomes, precos, links)
df.to_csv('resultado.csv')
