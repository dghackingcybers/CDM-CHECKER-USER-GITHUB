import random
import requests
import time
import string
from concurrent.futures import ThreadPoolExecutor

# Função para gerar nome aleatório com 3 ou 4 caracteres
def gerar_nome_aleatorio():
    tamanho = random.choice([3, 4])  # Escolhe aleatoriamente entre 3 ou 4 caracteres
    nome = ''.join(random.choices(string.ascii_lowercase, k=tamanho))  # Gera o nome aleatório com letras minúsculas
    return nome

# Função para verificar a disponibilidade do nome no GitHub
def verificar_disponibilidade(nome):
    url = f"https://github.com/{nome}"
    try:
        response = requests.get(url, timeout=5)  # Timeout de 5 segundos para evitar travamentos
        # Se o status for 404, significa que o nome não existe, logo está disponível
        if response.status_code == 404:
            return nome, True
        else:
            return nome, False
    except requests.RequestException as e:
        # Em caso de erro (timeout, falha de conexão, etc.), retorna o nome com indisponível
        return nome, False

# Função para gerar e verificar múltiplos nomes em paralelo
def gerar_nomes_e_checkar(quantidade=4000):
    nomes_disponiveis = []
    
    # Usando ThreadPoolExecutor para execução paralela das verificações
    with ThreadPoolExecutor(max_workers=10) as executor:  # Usando até 10 threads simultâneas
        futures = []
        
        # Gerando nomes aleatórios e passando para o executor
        for i in range(quantidade):
            nome_gerado = gerar_nome_aleatorio()
            futures.append(executor.submit(verificar_disponibilidade, nome_gerado))
        
        # Aguardando os resultados das requisições
        for future in futures:
            nome, disponivel = future.result()
            if disponivel:
                nomes_disponiveis.append(nome)
                print(f"Disponível: {nome}")
            else:
                print(f"Indisponível: {nome}")
    
    return nomes_disponiveis

if __name__ == "__main__":
    quantidade = 4000  # Número de nomes que você quer gerar e verificar
    nomes_disponiveis = gerar_nomes_e_checkar(quantidade)
    
    print("\nNomes disponíveis:")
    for nome in nomes_disponiveis:
        print(nome)
