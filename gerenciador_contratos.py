import csv
import pickle
from datetime import datetime, timedelta

class Contrato:
    def __init__(self, descricao, categoria, data_vencimento, fornecedor):
        self.descricao = descricao
        self.categoria = categoria
        self.data_vencimento = data_vencimento
        self.fornecedor = fornecedor

    def __str__(self):
        return f"Descrição: {self.descricao}, Categoria: {self.categoria}, Data Vencimento: {self.data_vencimento}, Fornecedor: {self.fornecedor}"

def importar_contratos_csv(nome_arquivo):
    contratos = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    data_vencimento_obj = datetime.strptime(row['Data de Vencimento'], '%d/%m/%Y')
                    contrato = Contrato(row['Descrição do Contrato'], row['Categoria'], data_vencimento_obj.strftime('%d/%m/%Y'), row['Fornecedor'])
                    contratos.append(contrato)
                except ValueError:
                    print(f"Data inválida para o contrato: {row['Descrição do Contrato']}. Ignorando linha.")
        return contratos
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return []

def calcular_dias_restantes(data_vencimento):
    try:
        data_vencimento_obj = datetime.strptime(data_vencimento, '%d/%m/%Y')
        data_atual = datetime.now()
        dias_restantes = (data_vencimento_obj - data_atual).days
        return max(0, dias_restantes)
    except ValueError:
        print(f"Data inválida: {data_vencimento}")
        return None


def determinar_categoria_prazo(dias_restantes):
    if dias_restantes is None:
        return "Data Inválida"
    if dias_restantes <= 30:
        return "VENCER EM BREVE"
    elif dias_restantes <= 60:
        return "VENCER EM 60 DIAS"
    elif dias_restantes <= 90:
        return "VENCER EM 90 DIAS"
    else:
        return "LONGO PRAZO"

def listar_contratos(contratos):
    if contratos:
        print("\nContratos:")
        for contrato in contratos:
            dias_restantes = calcular_dias_restantes(contrato.data_vencimento)
            categoria_prazo = determinar_categoria_prazo(dias_restantes)
            print(f"{contrato}\nDias Restantes: {dias_restantes} ({categoria_prazo})\n")
    else:
        print("Nenhum contrato cadastrado.")

def listar_contratos_por_prazo(contratos, prazo_dias):
    contratos_prazo = [c for c in contratos if calcular_dias_restantes(c.data_vencimento) <= prazo_dias]
    if contratos_prazo:
        print(f"\nContratos com vencimento em até {prazo_dias} dias:")
        for contrato in contratos_prazo:
            dias_restantes = calcular_dias_restantes(contrato.data_vencimento)
            print(f"{contrato}\nDias restantes: {dias_restantes}\n")
    else:
        print(f"\nNenhum contrato encontrado com vencimento em até {prazo_dias} dias.")


def salvar_contratos(contratos, nome_arquivo='contratos_salvos.pickle'):
    with open(nome_arquivo, 'wb') as f:
        pickle.dump(contratos, f)
    print(f"Contratos salvos em '{nome_arquivo}'")

def carregar_contratos(nome_arquivo='contratos_salvos.pickle'):
    try:
        with open(nome_arquivo, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []


class Tarefa:
    def __init__(self, descricao, tipo_tarefa, contrato_associado=None, data_vencimento=None, prioridade='Média', data_criacao=None):
        self.descricao = descricao
        self.tipo_tarefa = tipo_tarefa
        self.contrato_associado = contrato_associado
        self.data_vencimento = data_vencimento
        self.prioridade = prioridade
        self.data_criacao = data_criacao or datetime.now().strftime('%d/%m/%Y')

    def __str__(self):
        info_adicional = ""
        if self.contrato_associado:
            info_adicional = f" (Contrato: {self.contrato_associado.descricao})"
        if self.data_vencimento:
            info_adicional += f", Vencimento: {self.data_vencimento}"
        return f"Descrição: {self.descricao}, Tipo: {self.tipo_tarefa}{info_adicional}, Prioridade: {self.prioridade}, Criado em: {self.data_criacao}"

def adicionar_tarefa(contratos, tarefas):
    descricao = input("Digite a descrição da tarefa: ")
    while True:
        tipo_tarefa = input("Digite o tipo da tarefa ('Acompanhar Vencimento', 'Abrir Evento Coupa', 'Data Fim Assinatura'): ").title()
        if tipo_tarefa in ['Acompanhar Vencimento', 'Abrir Evento Coupa', 'Data Fim Assinatura']:
            break
        else:
            print("Tipo de tarefa inválido.")

    contrato_associado = None
    data_vencimento = None

    if tipo_tarefa == 'Acompanhar Vencimento':
        contrato_associado = selecionar_contrato_manual(contratos)
        data_vencimento = contrato_associado.data_vencimento if contrato_associado else None
    elif tipo_tarefa in ['Abrir Evento Coupa', 'Data Fim Assinatura']:
        while True:
            try:
                data_vencimento = input("Digite a data de vencimento (DD/MM/AAAA): ")
                datetime.strptime(data_vencimento, '%d/%m/%Y')
                break
            except ValueError:
                print("Formato de data inválido. Use DD/MM/AAAA")
        contrato_associado = selecionar_contrato_manual(contratos)

    while True:
        prioridade = input("Digite a prioridade (Alta, Média, Baixa): ").capitalize()
        if prioridade in ['Alta', 'Média', 'Baixa']:
            break
        else:
            print("Prioridade inválida. Digite Alta, Média ou Baixa.")

    nova_tarefa = Tarefa(descricao, tipo_tarefa, contrato_associado, data_vencimento, prioridade)
    tarefas.append(nova_tarefa)
    print(f'Tarefa "{descricao}" adicionada!')

def selecionar_contrato_manual(contratos):
    if not contratos:
        print("Não há contratos cadastrados.")
        return None
    listar_contratos(contratos)
    while True:
        try:
            indice = int(input("Digite o número do contrato (ou 0 para cancelar): "))
            if 0 < indice <= len(contratos):
                return contratos[indice - 1]
            elif indice == 0:
                return None
            else:
                print("Índice inválido.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def salvar_tarefas_csv(tarefas, nome_arquivo='tarefas.csv'):
    fieldnames = ['Descrição', 'Tipo de Tarefa', 'Contrato Associado', 'Data Vencimento', 'Prioridade', 'Data Criação']
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for tarefa in tarefas:
                contrato_descricao = tarefa.contrato_associado.descricao if tarefa.contrato_associado else ''
                writer.writerow({
                    'Descrição': tarefa.descricao,
                    'Tipo de Tarefa': tarefa.tipo_tarefa,
                    'Contrato Associado': contrato_descricao,
                    'Data Vencimento': tarefa.data_vencimento,
                    'Prioridade': tarefa.prioridade,
                    'Data Criação': tarefa.data_criacao
                })
        print(f"Tarefas salvas em '{nome_arquivo}'")
    except Exception as e:
        print(f"Erro ao salvar tarefas em CSV: {e}")

def carregar_tarefas_csv(nome_arquivo='tarefas.csv', contratos=None):
    tarefas = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                contrato_associado = None
                if row['Contrato Associado']:
                    contrato_associado = buscar_contrato_por_descricao(contratos, row['Contrato Associado'])

                try:
                    nova_tarefa = Tarefa(
                        row['Descrição'],
                        row['Tipo de Tarefa'],
                        contrato_associado,
                        row['Data Vencimento'],
                        row['Prioridade'].capitalize(),
                        row['Data Criação']
                    )
                    tarefas.append(nova_tarefa)
                except ValueError:
                    print(f"Erro ao criar tarefa a partir da linha: {row}. Verifique o formato da data ou prioridade.")

        return tarefas
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return []
    except Exception as e:
        print(f"Erro ao carregar tarefas do CSV: {e}")

def buscar_contrato_por_descricao(contratos, descricao):
    for contrato in contratos:
        if contrato.descricao == descricao:
            return contrato
    return None

def listar_tarefas(tarefas):
    if tarefas:
        print("\nTarefas:")
        for tarefa in tarefas:
            print(tarefa)
    else:
        print("Nenhuma tarefa cadastrada.")

def listar_tarefas_a_vencer(tarefas, prazo_dias):
    hoje = datetime.now()
    tarefas_a_vencer = []
    for tarefa in tarefas:
        if tarefa.data_vencimento:
            try:
                data_vencimento = datetime.strptime(tarefa.data_vencimento, '%d/%m/%Y')
                dias_restantes = (data_vencimento - hoje).days
                if 0 <= dias_restantes <= prazo_dias:
                    tarefas_a_vencer.append(tarefa)
            except ValueError:
                print(f"Data de vencimento inválida para a tarefa: {tarefa.descricao}. Ignorando tarefa.")

    if tarefas_a_vencer:
        print(f"\nTarefas a vencer em até {prazo_dias} dias:")
        for tarefa in tarefas_a_vencer:
            print(tarefa)
            dias_restantes = calcular_dias_restantes(tarefa.data_vencimento)
            print(f"Dias restantes: {dias_restantes}")
    else:
        print(f"Nenhuma tarefa encontrada a vencer em até {prazo_dias} dias.")

def listar_contratos_vencidos(contratos):
    hoje = datetime.now()
    contratos_vencidos = [c for c in contratos if calcular_dias_restantes(c.data_vencimento) < 0]
    if contratos_vencidos:
        print("\nContratos Vencidos:")
        for contrato in contratos_vencidos:
            print(contrato)
    else:
        print("Nenhum contrato vencido.")

def listar_tarefas_vencidas(tarefas):
    hoje = datetime.now()
    tarefas_vencidas = []
    for tarefa in tarefas:
        if tarefa.data_vencimento:
            try:
                data_vencimento = datetime.strptime(tarefa.data_vencimento, '%d/%m/%Y')
                if data_vencimento < hoje:
                    tarefas_vencidas.append(tarefa)
            except ValueError:
                print(f"Data de vencimento inválida para a tarefa: {tarefa.descricao}. Ignorando tarefa.")

    if tarefas_vencidas:
        print("\nTarefas Vencidas:")
        for tarefa in tarefas_vencidas:
            print(tarefa)
    else:
        print("Nenhuma tarefa vencida.")

if __name__ == "__main__":
    contratos = importar_contratos_csv('contratos.csv')
    tarefas = carregar_tarefas_csv(contratos=contratos)

    while True:
        print("\nGerenciador de Contratos e Tarefas")
        print("1. Adicionar Tarefa")
        print("2. Listar Contratos")
        print("3. Listar Contratos por Prazo")
        print("4. Listar Tarefas")
        print("5. Salvar Contratos")
        print("6. Salvar Tarefas")
        print("7. Listar Tarefas a Vencer")
        print("8. Listar Contratos Vencidos")
        print("9. Listar Tarefas Vencidas")
        print("10. Sair")

        escolha = input("Escolha uma opção: ")

        try:
            if escolha == '1':
                adicionar_tarefa(contratos, tarefas)
            elif escolha == '2':
                listar_contratos(contratos)
            elif escolha == '3':
                prazo = int(input("Digite o prazo (em dias): "))
                listar_contratos_por_prazo(contratos, prazo)
            elif escolha == '4':
                listar_tarefas(tarefas)
            elif escolha == '5':
                salvar_contratos(contratos)
            elif escolha == '6':
                salvar_tarefas_csv(tarefas)
            elif escolha == '7':
                prazo = int(input("Digite o prazo (em dias): "))
                listar_tarefas_a_vencer(tarefas, prazo)
            elif escolha == '8':
                listar_contratos_vencidos(contratos)
            elif escolha == '9':
                listar_tarefas_vencidas(tarefas)
            elif escolha == '10':
                break
            else:
                print("Opção inválida.")
        except ValueError as e:
            print(f"Erro: {e}. Por favor, insira um valor válido.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")