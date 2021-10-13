#Seção dos Imports, neste caso importamos as bibliotecas Mysql Connector, PrettyTable
# e uma biblioteca própria minha(Imports) que possue funções de verificação de CPF
import mysql.connector
from prettytable import PrettyTable
import Imports
import random


#Variáveis Globais
estado = 1
home = 1
user = 0
inicio = 0
area_user = 0
visu = 0
linha = list()
linha_cartao = list()


#Funções e Procedimentos utilizados ao decorrer do Programa
#Procedimento responsável por Fechar o programa
def fechar_programa():
    global home, estado, user
    home, estado, user = 0, 0, 0
    comandosql.close()
    conexao.close()
    print("\n" + "{:>76}".format(43*"-") + "\n" + "{:>74}".format("|Conexão Desfeita - Programa Encerrado|") + "\n" + "{:>76}".format(43 * "-")+"\n")


#Procedimento responsável por Cadastrar o usuário
def cadastro():
    print((50*"-") + "\n{:>33}".format("Área de Cadastro") + "\n" + (50*"-")+"\n")
    #Recebendo os Dados
    try:
        nome = input("Digite seu Nome e Sobrenome: ")
        idade = int(input("Digite sua Idade: "))
        while idade < 0 or idade > 100:
            idade = int(input("Idade inválida, digite sua Idade: "))
        telefone = input("Digite seu Telefone: ")
        email = input("Digite seu Email: ")
        cpf = input("Digite seu CPF: ")
        #Nesse caso uso uma função criada em outro Script, pode ser comentada sem implicações no programa
        while Imports.Valida_CPF(cpf) != "Válido":
            cpf = input("CPF inválido, digite novamente: ")
        senha = input("Digite uma Senha: ")
        senha1 = input("Confirme sua Senha: ")
        while senha != senha1:
            senha = input("As senhas não são iguais, digite uma Senha: ")
            senha1 = input("Confirme sua Senha: ")
        serasaScore = int(input("Digite seu serasaScore: "))
        #Testando a Integridade do Serasa Score
        while serasaScore < 0 or serasaScore > 1000:
            serasaScore = int(input("Serasa Score inválido, digite novamente: "))
        salario = float(input("Digite seu Salário Bruto Mensal: "))
        #Aqui eu Testo se já existe um usuário com esses mesmos Dados já Cadastrados
        comandosql.execute(f"select nome, cpf from tbl_cadastro where cpf = {cpf};")
        select = comandosql.fetchone()
        if select != None:
            print("Um Usuário com esses Dados já existe no Sistema, retornando para o Módulo Principal do Sistema")
        else:
            #Guardando esses Dados com o Execute
            comandosql.execute(f"insert into tbl_cadastro values (0,'{nome}',{idade},'{telefone}','{email}','{cpf}','{senha}','{serasaScore}','{salario}',null);")
            #Guardando esses Dados no Banco pelo Commit
            conexao.commit()
            print("Cadastro Realizado com Sucesso, retornando para o Módulo Principal do Sistema")
    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


#Procedimento reponsável por Logar o Usuário
def login():
    print("\n" + (50 * "-") + "\n{:>33}".format("Área de Login") + "\n" + (50 * "-") + "\n")
    try:
        #Recebendo os Dados
        C = input("Digite seu CPF: ")
        S = input("Digite sua Senha: ")
        #Verifico se os Dados fornecidos existem no BD
        comandosql.execute(f"select * from tbl_cadastro where cpf = '{C}' and senha = '{S}';")
        global linha
        linha = comandosql.fetchone()
        if linha == None:
            print("Usuário ou Senha incorretos, retornando para o Módulo Principal do Sistema")
            linha = ()
        else:
            print(f"Login realizado com sucesso\nBem Vindo {linha[1]}")
            global home,user
            home, user = 0, 1
    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


#Procedimento responsável por exibir todos os Dados de Cadastro do Usuário
def visualizar():
    global visu
    if visu == 0:
        print("\n" + (50 * "-") + "\n{:>40}".format("Área de Vizualização dos Dados") + "\n" + (50 * "-") + "\n")
    try:
        #Criando a variável Grid para armazenar as colunas da Tabela Pretty Table
        grid = PrettyTable(['Nome','Idade','Telefone','E-mail','CPF','Serasa Score','Salário'])
        #Filtrando os resultados da Consulta com o ID do usuário logado
        comandosql.execute(f"select nome, idade, telefone, email, cpf, serasa_score,salario from tbl_cadastro where id_cadastro = {linha[0]};")
        tabela = comandosql.fetchone()
        #Acrescentando a variável Tabela com os Resultados no Grid
        grid.add_row(tabela)
        print(grid)
        visu = 0
    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


#Procedimento responsável por Alterar os Dados do Usuário, só é possível alterar o Telefone, E-mail e a Senha
def alter():
    print("\n" + (50 * "-") + "\n{:>40}".format("Área de Alteração dos Dados") + "\n" + (50 * "-") + "\n")
    global linha, visu
    try:
        #Pergunto se deseja Alterar a Idade
        desejo = int(input("Deseja Alterar[1] a Idade cadastrada ? 1/0: "))
        while desejo != 1 and desejo != 0:
            desejo = int(input("Resposta inválida, deseja Alterar a Idade cadastrada ? 1/0: "))
        if desejo == 1:
            novo_dado = int(input("Digite a nova Idade: "))
            while novo_dado < 0 or novo_dado > 100:
                novo_dado = int(input("Idade inválida, digite sua Idade: "))
            #Alterando a Idade
            comandosql.execute(f"update tbl_cadastro set idade = '{novo_dado}' where id_cadastro = {linha[0]};")
            conexao.commit()
            visu = 1
            print("Idade Alterada com Sucesso")
        #Pergunto se deseja Alterar o Telefone
        desejo = int(input("Deseja Alterar[1] o Telefone cadastrado ? 1/0: "))
        while desejo != 1 and desejo != 0:
            desejo = int(input("Resposta inválida, deseja Alterar o Telefone cadastrado ? 1/0: "))
        if desejo == 1:
            novo_dado = input("Digite o novo Telefone: ")
            #Alterando o Telefone
            comandosql.execute(f"update tbl_cadastro set telefone = '{novo_dado}' where id_cadastro = {linha[0]};")
            conexao.commit()
            visu = 1
            print("Telefone Alterado com Sucesso")
        #Pergunto se deseja Alterar o E-mail
        desejo = int(input("Deseja Alterar[1] o E-mail cadastrado ? 1/0: "))
        while desejo != 1 and desejo != 0:
            desejo = int(input("Resposta inválida, deseja Alterar o E-mail cadastrado ? 1/0: "))
        if desejo == 1:
            novo_dado = input("Digite o novo E-mail: ")
            #Alterando o E-mail
            comandosql.execute(f"update tbl_cadastro set email = '{novo_dado}' where id_cadastro = {linha[0]};")
            conexao.commit()
            visu = 1
            print("E-mail Alterado com Sucesso")
        #Pergunto se deseja Alterar a Senha
        desejo = int(input("Deseja Alterar[1] o Senha cadastrada ? 1/0: "))
        while desejo != 1 and desejo != 0:
            desejo = int(input("Resposta inválida, deseja Alterar a Senha cadastrada ? 1/0: "))
        if desejo == 1:
            #Contador para Verificar a Quantidade de Tentativas sobre a Inserção da Senha
            contador_tentativas = 0
            senha_antiga = input("Digite a Senha Antiga: ")
            #Comparando a Senha digitada com a Senha já existente
            while senha_antiga != linha[6] and contador_tentativas != 3:
                senha_antiga = input("Senha Incorreta, digite a Senha Antiga: ")
                contador_tentativas += 1
            #Caso as Senhas batam, é permitido que o usuário Altere a Senha
            if contador_tentativas != 3:
                novo_dado = input("Digite a Nova Senha: ")
                #Atualizando a Senha
                comandosql.execute(f"update tbl_cadastro set senha = '{novo_dado}' where id_cadastro = {linha[0]};")
                conexao.commit()
                visu = 1
                print("Senha Alterada com Sucesso")
            #Caso ela não batam, a Alteração da Senha é cancelada
            else:
                print("Senha não pode ser Alterada, quantidade limite de Tentativas excedida")
        #Atualizando a Variável Linha
        comandosql.execute(f"select * from tbl_cadastro where id_cadastro = '{linha[0]}';")
        linha = comandosql.fetchone()
        if visu == 1:
            print("Dados atualizados, nova Tabela gerada\n")
        else:
            print("Nenhum dado foi Alterado, retornando para o Módulo Principal do Sistema\n")


    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


#Procedimento responsável por Criar um Cartão no Banco para o usuário, recebe como Parâmetro o id_cadastro do usuário e seu Salário
def criar_cartao():
    print("\n" + (50 * "-") + "\n{:>43}".format("Área de Criação de Cartão de Crédito") + "\n" + (50 * "-") + "\n")
    try:
        global linha
        #Pergunto se o usuário deseja Criar um Cartão
        criar = int(input("Confirme se você deseja Criar um Cartão neste Banco - 1/0: "))
        while criar != 1 and criar != 0:
            criar = int(input("Resposta inválida, confirme se você deseja Criar um Cartão neste Banco - 1 = Sim/0 = Não: "))
        if criar == 1:
            #Duas Variáveis responsáveis por impedir que sejam criados cartões de mesmo número, mesmo que as chances sejam infímas
            numero_cartao = 0
            select_cartao = 0
            while numero_cartao == select_cartao:
                numero_cartao = Imports.Gerar_Numero_Cartao()
                comandosql.execute(f"select * from tbl_cartoes where numero_cartao = '{numero_cartao}';")
                select_cartao = comandosql.fetchall()
            cdg_seguranca = input("Digite um Código de Segurança de 4 Dígitos (Números) para seu Cartão: ")
            while len(cdg_seguranca) != 4 or cdg_seguranca.isnumeric() == False:
                cdg_seguranca = input("Código inválido, digite um Código de Segurança de 4 Dígitos (Números) para seu Cartão: ")
            #Criamos o Cartão Padronizado, Número de 16 Dígitos, Cdg de Segurança de 4 Dígitos, Limite = 1,6 * Salario, Crédito = 3* Salario, Fechamento Fatura entre 20 e 28 e o Vencimento em 3 Anos
            comandosql.execute(f"insert into tbl_cartoes values ('{numero_cartao}','{cdg_seguranca}',{linha[8]*1.6},{linha[8]*3},{random.randrange(20,28)},'{random.randrange(1,13)}/2024');")
            conexao.commit()
            #Atrubuindo esse Cartão ao usuário
            comandosql.execute(f" update tbl_cadastro set numero_cartao = '{numero_cartao}' where id_cadastro = {linha[0]};")
            conexao.commit()
            print("Cartão Cadastrado com Sucesso\nRetornando para o Módulo Principal do Sistema")
            #Atualizando a Variável Linha
            comandosql.execute(f"select * from tbl_cadastro where id_cadastro = '{linha[0]}';")
            linha = comandosql.fetchone()
        #Caso o usuário não deseje Criar, retornamos para o Módulo Principal
        else:
            print("Nenhum Cartão foi Criado, retornando para o Módulo Principal do Sistema")
        #Por se tratar de uma Simulação, imaginariamente atribuimos para o Cartão o valor do Crédito possúido como o salário vezes 3
    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro:{erro}\nNenhum Cartão foi Criado, retornando para o Módulo Principal do Sistema")


#Procedimento responsável por Exibir os Dados do Cartão cadastrado do usuário
def visualizar_cartao():
    print("\n" + (50 * "-") + "\n{:>45}".format("Área de Vizualização dos Dados do Cartão") + "\n" + (50 * "-") + "\n")
    try:
        #Criando a variável Grid para armazenar as colunas da Tabela Pretty Table
        grid = PrettyTable(['Número Cartão', 'Código de Segurança', 'Limite', 'Crédito Atual', 'Fechamento da Fatura (Dia)', 'Data de Vencimento'])
        #Selecionando todos os Dados do Cartão
        comandosql.execute(f"select * from tbl_cartoes where numero_cartao = '{linha[9]}';")
        tabela = comandosql.fetchone()
        #Acrescentando a variável Tabela com os Resultados no Grid
        grid.add_row(tabela)
        print(grid)
    #Exceção de Erro
    except Exception as erro:
        print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


#Módulo Principal do Programa
#Tentando conexão com o Banco de Dado
try:
    #Criando objeto conexao, Obs: No meu caso a senha do MySqlWorkbench foi configurada como 96917581888
    conexao = mysql.connector.Connect(host='localhost',database='Banco',user='root',password='96917581888')
    #Verificando a Conexão
    if conexao.is_connected():
        info = conexao.get_server_info()
        print("{:>76}".format(42*"-") + "\n" + "{:>70}".format("|Banco conectado ao Sistema - Versão:")+"{}|".format(info) + "\n" + "{:>76}".format(42 * "-")+"\n")
        #Criando o Objeto Cursor
        comandosql = conexao.cursor()
    else:
        print("Conexão não Estabelecida")


#Exceção de Erro
except Exception as erro:
    print("{:>140}".format(135 * "-") + "\n" + "{:>50}".format("|Conexão não Estabelecida - Erro:")+"{}|".format(erro) + "\n" + "{:>140}".format(135 * "-"))


#Caso esteja conectado o Banco, o Programa inicia
else:
    #Tela Inicial
    print((55*"=+") + "\n{:>80}".format("Bem Vindo ao Sistema de Atribuição de Crédito dos Bancos") + "\n" + (55*"=+")+"\n")
    while estado == 1:
        #Área Home, onde o usuário Loga ou Cadastra no Sistema
        while home == 1:
            print("\n" + (50 * "-") + "\n{:>30}".format("Área Home") + "\n" + (50 * "-") + "\n")
            try:
                inicio = int(input("Deseja Logar[1] no sistema ou se Cadastrar[2] ou Fechar[3] o programa ?: "))
                while inicio != 1 and inicio != 2 and inicio != 3:
                    inicio = int(input("Digite '1' para Logar, '2' para se Cadastrar no sistema ou '3' para Fechar o programa: "))
                    print("\n")
            except Exception as erro:
                print(f"Ocorreu um Erro: {erro}")

            #Caso a Opção seja o 3, fechamos o Programa
            if inicio == 3:
                fechar_programa()


            #Caso a Opção seja o 2, chamamos o Procedimento Cadatro
            if inicio == 2:
                cadastro()


            #Caso a Opção seja o 1, chamamos o Procedimento Login
            if inicio == 1:
                login()


        #Área do Usuário, onde ele pode Visualizar e Alterar suas Informações, Criar e Visualizar seu Cartão
        while user == 1:
            print("\n" + (50 * "-") + "\n{:>33}".format("Área do Usuário") + "\n" + (50 * "-") + "\n" + "Logado como: {}".format(linha[1]) + "\n")
            try:
                if linha[9] == None:
                    area_user = int(input("Deseja Deslogar[1] no sistema, visualizar seus Dados de Cadastro[2], criar Cartão de Crédito[3] ou Fechar[4] o programa ?: "))
                else:
                    area_user = int(input("Deseja Deslogar[1] no sistema, visualizar seus Dados de Cadastro[2], visualizar seus Dados do Cartão de Crédito[3] ou Fechar[4] o programa ?: "))
                while area_user != 1 and area_user != 2 and area_user != 3 and area_user != 4:
                    if linha[9] == None:
                        area_user = int(input("Digite 1 para Deslogar no sistema, 2 para visualizar seus Dados de Cadastro, 3 para criar Cartão de Crédito ou 4 para Fechar o programa ?: "))
                    else:
                        area_user = int(input("Digite 1 para Deslogar no sistema, 2 para visualizar seus Dados de Cadastro, 3 para visualizar seus Dados do Cartão de Crédito ou 4 para Fechar o programa ?: "))
            except Exception as erro:
                print(f"Ocorreu um Erro: {erro}")


            #Caso a Opção seja o 1, quebramos o While e retornamos para a Área Home
            if area_user == 1:
                linha = ("")
                print("Deslogado do sistema com Sucesso, retornando para a Área Home do sistema")
                user = 0
                home = 1



            #Caso a Opção seja o 2, chamamos o Procedimento Visualizar
            if area_user == 2:
                visualizar()
                #Pergunto ao Usuário se ele deseja alterar seus Dados cadastrados, caso deseje, chamo a função Alter
                try:
                    alterar = int(input("\nDeseja Alterar[1] os Dados cadastrados ? 1 = Sim/0 = Não: "))
                    while alterar != 1 and alterar != 0:
                        alterar = int(input("Resposta inválida, deseja Alterar os Dados cadastrados ? 1 = Sim/0 = Não: "))
                    if alterar == 1:
                        alter()
                        #Variável Visu é responsável por verificar se pelo menos um registro foi Alterado
                        if visu == 1:
                            visualizar()
                except Exception as erro:
                    print(f"Ocorreu um Erro: {erro}")


            #Caso a Opção seja o 3 e o usuário não possua Cartão, chamamos o Procedimento Criar Cartão, caso ele possua, chamamos o Procedimento Visualizar Cartão
            if area_user == 3:
                if linha[9] == None:
                    if linha[2] < 16:
                        print("Sua Idade é inválida para a criação de um Cartão")
                    elif linha[7] < 500:
                        print("Seu Serasa Score não é válido para a criação de um Cartão")
                    else:
                        criar_cartao()
                else:
                    visualizar_cartao()
                    #Pergunto ao usuário se ele deseja Excluir o Cartão já criado
                    deletar = int(input("Deseja Excluir o Cartão criado ? 1/0: "))
                    while deletar != 0 and deletar != 1:
                        deletar = int(input("Resposta Inválida, deseja Excluir o Cartão criado ? 1 = Sim/0 = Não"))
                    #Confirmo com o usuário se ele quer REALMENTE excluir o cartão, aceitando qualquer resposta diferente de 1 como "não"
                    if deletar == 1:
                        deletar = int(input("Tem certeza que deseja Excluir o Cartão criado ? 1/0: "))
                    try:
                        if deletar == 1:
                            #Primeiro atualizamos o Cadastro do usuário e desvinculamos o Cartão
                            comandosql.execute(f"update tbl_cadastro set numero_cartao = null where numero_cartao = '{linha[9]}';")
                            conexao.commit()
                            #Segundo excluimos o Regiistro do Cartão na tabela Cartões
                            comandosql.execute((f"delete from tbl_cartoes where numero_cartao = '{linha[9]}'"))
                            conexao.commit()
                            #Terceiro, atualizamos a Variável Linha
                            comandosql.execute(f"select * from tbl_cadastro where id_cadastro = '{linha[0]}';")
                            linha = comandosql.fetchone()
                            print("Cartão Excluído com Sucesso\nRetornando para o Módulo Principal do Sistema")
                        else:
                            print("O Cartão não foi Excluído\nRetornando para o Módulo Principal do Sistema")
                    #Exceção de Erro
                    except Exception as erro:
                            print(f"Ocorreu um Erro: {erro}\nRetornando para o Módulo Principal do Sistema")


            #Caso a Opção seja o 4, chamamos o Procedimento Fechar Programa
            if area_user == 4:
                fechar_programa()
#Fim do Programa !!! =+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+