# Desafio de Projeto 3. Otimizando um Sistema Bancário com Python**
# Autor: Mário Apolinário

############### Função para a Tela do Menu ###############
import textwrap
def menu():
    menu = """
    ================ MENU ================
    [1] Cadastrar Usuário
    [2] Cadastrar Conta Bancária
    [3] Lista de Contas
    [4] Depositar
    [5] Sacar
    [6] Extrato
    [7] Sair
    Escolha uma Opção:
    => """
    return input(textwrap.dedent(menu))

############### Função para a operação de Saque ###############
def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    if (numero_saques + 1) <= limite_saques:    # verifica se a quantidade de saques diário foi alcançada 
        valor = float(input("\nQuanto você deseja Sacar R$ => "))
        if valor <= saldo and valor <= limite and valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        elif valor > saldo:
            print("\nNão será possivel sacar o dinheiro por falta de saldo!")
        else:
            print("\nErro! Valor não permitido para Saque!")
    else:
        print(f"\nSão permitidos {limite_saques} saques diários apenas!")
    return saldo, extrato, numero_saques

############### Função para a operação de Depósito ###############
def depositar(saldo, extrato, /):
    valor = float(input("\nQuanto você deseja Depositar R$ =>"))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("\nInforme valores maiores que Zero (0)!")
    return saldo, extrato

############### Função para a operação de Extrato ###############
def visualiza_extrato(saldo, /, *, extrato):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
    
############### Função para a operação de Criar Usuário ###############
def criar_usuario(usuarios):
    cpf = input("\nDigite o seu número de CPF => ")
    if int(cpf) <= 0 or len(cpf) > 11:   # verifica se não foram digitados numeros negativos ou contendo mais de 11 digitos
        print("\nErro! Número de CPF inválido!")
    elif len(cpf) < 11: # verife se o numero de CPF contém menos de 11 digitos
        print("\nNúmero de CPF incompleto!")
    else:   # condição para número de CPF válido

        usuario = filtrar_usuario(cpf, usuarios)    #verifica se o usuário já foi cadastrado anteriormente

        if usuario: 
            print("\n Já existe usuário com esse CPF cadastrado!")
            return
    
        nome = input("Informe o nome completo => ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa) => ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado) => ")
        usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
        print(" *** Usuário cadastrado com sucesso! *** \n")
    return

############### Função para verificar Usuário cadastrado ###############
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

############### Função para a operação de Criar Conta ###############
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário => ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n *** Conta criada com sucesso! *** ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n Usuário não encontrado, fluxo de criação de conta encerrado!\n")

############### Função para listar todas as Conta Criadas ###############
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

############### FUNÇAO PROGRAMA PRINCIPAL ###############
def main():
    
    usuarios = []
    contas = []
    saldo = 0
    extrato = ""
    numero_saques = 0
    LIMITE = 500
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    while True:
        opcao = menu()
        if opcao == "1":    # Cadastrar Usuário
            criar_usuario(usuarios)
        
        elif opcao == "2":  # Cadastrar Conta Bancária
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)        
        
        elif opcao == "3":
            listar_contas(contas)

        elif opcao == "4":    # Depósito
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "5":  # Saque
            saldo, extrato, numero_saques = sacar(saldo = saldo,
                extrato = extrato,
                limite = LIMITE,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES
            )

        elif opcao == "6":  # Extrato
            visualiza_extrato(saldo, extrato = extrato)

        elif opcao == "7":  # Sair
            break
        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")

main()  # executa programa principal