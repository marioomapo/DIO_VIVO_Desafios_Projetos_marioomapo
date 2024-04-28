# Desafio de Projeto 2. Criando um Sistema Bancário em Python**
# Autor: Mário Apolinário
menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """
saldo = 0
extrato = ""
numero_saques = 0
LIMITE = 500
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)
    if opcao == "1":    #Depósito
        valor = float(input("Quanto você deseja Depositar R$:"))
        if valor > 0:  #++
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Informe valores maiores que 0!")
    elif opcao == "2":  #Saque
        if (numero_saques + 1) <= LIMITE_SAQUES:
            valor = float(input("Quanto você deseja Sacar R$:"))
            if valor <= saldo and valor <= LIMITE and valor > 0:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
            elif valor > saldo:
                print("Não será possivel sacar o dinheiro por falta de saldo!")
            else:
                print("Erro! Valor não permitido para Saque!")
        else:
            print(f"São permitidos {LIMITE_SAQUES} saques diários apenas!")
    elif opcao == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
    elif opcao == "4":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")