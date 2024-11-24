import csv
import random
from datetime import datetime, timedelta

def gerar_data_vencimento(dias_a_partir_de_hoje):
    """Gera uma data de vencimento aleatória."""
    hoje = datetime.now()
    data_vencimento = hoje + timedelta(days=dias_a_partir_de_hoje)
    return data_vencimento.strftime("%d/%m/%Y") # Formato DD/MM/AAAA


def criar_arquivo_csv(nome_arquivo, num_contratos):
    """Cria um arquivo CSV com dados de contratos."""
    categorias = ["Locação", "Manutenção", "Seguro", "Fornecimento", "Consultoria", "Software"]
    fornecedores = ["A", "B", "C", "D", "E", "F"]
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Descrição do Contrato', 'Categoria', 'Data de Vencimento', 'Fornecedor']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(num_contratos):
            descricao = f"Contrato {i+1} - Descrição exemplo"
            categoria = random.choice(categorias)
            dias = random.randint(30, 365) # Datas de vencimento entre 30 e 365 dias a partir de hoje.
            data_vencimento = gerar_data_vencimento(dias)
            fornecedor = random.choice(fornecedores)
            writer.writerow({'Descrição do Contrato': descricao, 'Categoria': categoria, 'Data de Vencimento': data_vencimento, 'Fornecedor': fornecedor})

# Exemplo de uso:
criar_arquivo_csv('contratos.csv', 100) # Cria um arquivo com 100 contratos
print("Arquivo 'contratos.csv' criado com sucesso!")