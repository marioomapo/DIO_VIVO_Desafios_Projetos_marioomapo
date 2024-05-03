# Desafio de Projeto 3. Modelagem do Sistema Bancário em POO** VERSÃO 2
# Autor: Mário Apolinário
# Foi acrescentada a operação referente a Pessoa Jurídica
# Foi adicionado conta Poupança

from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap

# Criando a Classe Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco #self.endereco = str(endereco)
        self.contas = [] # self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta) # adiciona a conta a lista de contas

#Criando a Classe referente a Pessoa Física
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

#Criando a Classe referente a Pessoa Jurídica
class PessoaJuridica(Cliente):
    def __init__(self, cnpj, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cnpj
        self.nome = nome
        self.data_nascimento = data_nascimento

# Criando a Classe Conta
class Conta:    
    def __init__(self, numero, cliente):
        self._saldo = 0 # atributos do tipo privado 
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente #self._cliente = Cliente()
        self._historico = Historico()

    # Criando Método para Cadastrar nova Conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    # Criando Método para Saldo
    @property
    def saldo(self):
        return self._saldo
    
    # Criando Método para Nunero
    @property
    def numero(self):
        return self._numero

    # Criando Método para Agencia
    @property
    def agencia(self):
        return self._agencia

    # Criando Método para Cliente
    @property
    def cliente(self):
        return self._cliente

    # Criando Método para Histórico
    @property
    def historico(self):
        return self._historico
    
    # Criando Método para Sacar
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\n*** Falha na Operação: Você não tem saldo suficiente! ***")
        elif valor > 0:
            self._saldo -= valor
            print("\n **** Saque realizado com sucesso! ****")
            return True # True -> operação ocorreu com sucesso
        else:
            print("\n*** Operação Falhou! Valor informado é inválido. ****")
        return False    # False -> ocorreu erro na operação

    # Criando Método para Depositar ok
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n*** Depósito realizado com sucesso! ***")
        else:
            print("\n*** Operação Falhou! Valor informado é inválido. ****")
            return False    # False -> ocorreu erro na operação
        
        return True # True -> operação ocorreu com sucesso

# Criando a Classe Conta Corrente que é Filha de Conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)   # sobrescrevendo uma implementação
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n*** Operação falhou! O valor do saque excede o limite! ***")
        elif excedeu_saques:
            print("\n*** Operação falhou! Número máximo de saques excedido! ***")
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome} 
        """

# Criando a Classe Histórico    
class Historico:
    def __init__(self):
        self._transacoes = []    # criando uma lista
    
    @property
    def transacoes(self):
        return self._transacoes
    # Criando Método que lista o número de Transações 
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

# Criando a Classe Conta Poupança que é Filha de Conta
class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, limite = 1000, limite_saques = 5):
        super().__init__(numero, cliente)   # sobrescrevendo uma implementação
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n*** Operação falhou! O valor do saque excede o limite! ***")
        elif excedeu_saques:
            print("\n*** Operação falhou! Número máximo de saques excedido! ***")
        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


# Criando uma Classe Transação que é Abstrata
class Transacao(ABC):
    # Criando Método valor
    @property
    @abstractmethod
    def valor(self):
        pass
    
    # Criando Método Registrar que é Abstrato
    @abstractmethod
    def registrar(self, conta):
        pass

# Criando Classe que implementa Operação de Depósito ok
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)    

# Criando Classe que implementa Operação de Saque ok
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Criando Função que Implementa o MENU
def menu():
    menu = """\n
    ================ MENU ================
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [7]\tSair
    => """
    return input(textwrap.dedent(menu))

# Criando Função que Implementa a Filtragem dos Clientes
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Criando Função que Implementa a Recuperação da conta do Clientes
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n*** Cliente não possui conta! ***")
        return
    # FIXME: não permite cliente escolher a conta

    return cliente.contas[0]    # Nota: não permite cliente escolher a conta

# Criando Função que Implementa o Depósito
def depositar(clientes):
    cpf = input("\nInforme o CPF do cliente => ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return

    valor = float(input("\nInforme o valor do depósito => "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Criando Função que Implementa o Saque
def sacar(clientes):
    cpf = input("\nInforme o CPF do cliente => ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque => "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Criando Função que Exibe o Extrato
def exibir_extrato(clientes):
    cpf = input("\nInforme o CPF do cliente => ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# Criando Função que Cadastra o Cliente ("cria" o cliente)
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número) => ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n*** Já existe cliente com esse CPF! ***")
        return

    nome = input("Informe o nome completo => ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa) => ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado) => ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n*** Cliente criado com sucesso! ***")

# Criando Função que Implementa a Criação da Conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente => ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado, fluxo de criação de conta encerrado! ***")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n*** Conta criada com sucesso! ***")

# Criando Função que Lista todas as Contas
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# Define a Função Principal
def main():
    clientes = []
    contas = []

    while True: # LOOP
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)
        
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "5":
            listar_contas(contas)
        
        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "7":
            break

        else:
            print("\n*** Operação inválida, por favor selecione novamente a operação desejada. ***")


main() # << programa inicia aqui
