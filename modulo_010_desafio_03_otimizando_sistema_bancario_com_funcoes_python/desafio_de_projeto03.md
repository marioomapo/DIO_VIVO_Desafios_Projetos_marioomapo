# **2. DOMINANDO PYTHON E SUAS ESTRUTURAS**
Autor: Mário F. Apolinário

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marioapolinario8a54757712/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marioomapo)
## *Observação:* ⚠️
**Este material foi desenvolvido como objetivo de entender o desafio proposto, que faz referência a otimização de um Sistema Bancário Fictíco em linguagem Python.**
## Objetivo geral 🎯
A partir do **Desafio de Projeto 02**, que consistiu na criação de um sistema bancário com Python. Agora, o **Desafio de Projeto 03** propõe uma otimização deste sistema bancário anterior com novas funcionalidades fazendo uso de funções em Python.

Agora, as funções existentes de Saque, Depósito e Extrato são implementadas como funções em Python. E também, duas novas funções são criadas: Cadastrar Usuário (cliente) e Cadastrar conta Bancária.
## 2.10 Otimizando o Sistema Bancário com Python 
## 2.10.1 Introdução
Precisamos deixar nosso código mais modularizado, para isso vamos criar funções para as operações existentes: sacar, depositar e extrato (visualizar histórico). Além disso, para a versão 2 do nosso sistema precisamos criar duas novas funções: criar usuário (cliente do banco) e criar conta corrente (vincular com usuário).
## b) Separação em Funções
Devemos criar funções para todas as operações do sistema. Para exercitar tudo que aprendemos neste módulo, cada função vai ter uma regra na passagem de argumentos. O retorno e a forma como serão chamadas, pode ser definida por você da forma que achar melhor. 
## c) Operação de Saque
A função Saque deve receber os argumentos apenas por nome (keyword only). Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques. Sugestão de retorno: saldo, extrato e numero de saques.
## d) Operação de Depósito
A função de depósito deve receber os argumentos apenas por posição (positionaly only). Sugestão de argumentos: valor, saldo, extrato. Sugestão de retorno: saldo e extrato. 
## e) Operação de Extrato
A função extrato deve receber os argumentos por posição e nome (positional only e keyword only).

+ Argumentos posicionais: saldo.
+ Argumentos nomeados: extrato.
## f) Novas Funções
Precisamos criar duas novas funções: criar usuário e criar conta corrente. Fique a vontade para adicionar mais funções (exemplo: lista de contas).
## g) Criar Usuário (cliente)
O programa deve armazenar os usuários em uma lista, usuário é composto por: nome, data de nascimento, CPF, e endereço. O endereço é uma string com o o formato: logradouro, nº, bairro, cidade/sigla estado. Deve ser armazenado somente os números do CPF. Não podemos cadastrar (2) dois usuários com o mesmo CPF.
## h) Criar Conta Corrente
O programa deve armazenar contas em uma lista, uma conta é composta por: agência, número da conta e usuário. O número da conta é sequencial, iniciando em 1. O número da agência é fixo: "0001". O usuário pode ter mais de uma conta, mas uma conta pertence somente a (1) um usuário.
## i) Dica
Para vincular um usuário a uma conta, filtre a lista de usuários buscando o número do CPF informado para cada usuário da lista. 

## *Links de Úteis* 🌐

### 1. [Repositório guicarvalho](https://github.com/digitalinnovationone/trilha-python-dio/tree/main)

### 2. [Apresentação](http://academiapme-my.sharepoint.com/:p:/g/personal/kawan_dio_me/Ef-dMEJYq9BPotZQso7LUCwBJd7gDqCC2SYlUYx0ayrGNQ?e=G79e2L)