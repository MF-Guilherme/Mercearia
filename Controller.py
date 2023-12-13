from Models import Categoria,  Estoque, Produto, Fornecedor, Pessoa, Funcionario, Venda
from DAO import DaoCategoria, DaoEstoque, DaoFornecedor, DaoFuncionario, DaoPessoa, DaoProduto, DaoVenda
from datetime import datetime


class ControllerCategoria:
    def cadastrar_categoria(self, nova_categoria):
        existe = False
        x = DaoCategoria.ler()

        for i in x:
            if i.categoria == nova_categoria:
                existe = True

        if not existe:
            DaoCategoria.salvar(nova_categoria)
            print('Categoria cadastrada com sucesso')
        else:
            print('A categoria que deseja cadastrar já existe')

    def remover_categoria(self, categoria_a_remover):
        x = DaoCategoria.ler()
        cat = list(filter(lambda x: x.categoria == categoria_a_remover, x))

        if len(cat) <= 0:
            print('A categoria que deseja remover não existe')
        else:
            for i in range(len(x)):
                if x[i].categoria == categoria_a_remover:
                    del x[i]
                    break
            print('Categoria removida com sucesso!')
            #TODO: COLOCAR SEM CATEGORIA NO ESTOQUE
            with open('categorias.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

    def alterar_categoria(self, categoria_a_alterar, nova_categoria):
        x = DaoCategoria.ler()

        cat = list(filter(lambda x: x.categoria == categoria_a_alterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == nova_categoria, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categoria(nova_categoria) if (x.categoria == categoria_a_alterar) else (x), x))
                print('A alteração foi efetuada com sucesso')
                #TODO: ALTERAR A CATEGORIA NO ESTOQUE
            else:
                print('A categoria para qual deseja alterar já existe')
        else:
            print('A categoria que deseja alterar não existe')

        with open('categorias.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrar_categoria(self):
        categorias = DaoCategoria.ler()
        if len(categorias) == 0:
            print('Categoria vazia')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')


class ControllerEstoque:
    def cadastrar_produto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0: # se encontrou a categoria
            if len(est) == 0: # se o nome do produto não estiver no estoque
                produto = Produto(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso!')
            else:
                print('Produto já existe no estoque')
        else:
            print('Categoria inexistente')

    def remover_produto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(est) > 0:
            for i in range(len(x)):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('Produto removido com sucesso')
        else:
            print('O produto que deseja remover não existe no estoque')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(f'{i.produto.nome}|{i.produto.preco}|{i.produto.categoria}|{i.quantidade}\n')

    def alterar_produto(self, nome_a_alterar, novo_nome, novo_preco,
                        nova_categoria, nova_quantidade):
        x = DaoEstoque.ler()
        y = DaoCategoria.ler()
        h = list(filter(lambda x: x.categoria == nova_categoria, y))
        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nome_a_alterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novo_nome, x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produto(novo_nome, novo_preco, nova_categoria), nova_quantidade) 
                                 if (x.produto.nome == nome_a_alterar) else (x), x))
                    print('Produto alterado com sucesso')
                else:
                    print(f'Produti {novo_nome} já está cadastrado')
            else:
                print('O produto que deseja alterar não existe')

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(f'{i.produto.nome}|{i.produto.preco}|{i.produto.categoria}|{i.quantidade}\n')
        else:
            print('A categoria informada não existe')

    def mostrar_estoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Estoque vazio')
        else:
            print('==========Produtos==========')
            for i in estoque:
                print(f'Nome: {i.produto.nome}\n'
                      f'Preco: {i.produto.preco}\n'
                      f'Categoria: {i.produto.categoria}\n'
                      f'Quantidade: {i.quantidade}'
                      )
                print('-------------------')


class ControllerVenda:
    def cadastrar_venda(self, nome_produto, vendedor, comprador, quantidade_vendida):

        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe is False:
                if i.produto.nome == nome_produto:
                    existe = True
                    if i.quantidade >= quantidade_vendida:
                        quantidade = True
                        i.quantidade = i.quantidade - quantidade_vendida
                        vendido = Venda(Produto(i.produto.nome, i.produto.preco, i.produto.categoria), vendedor, comprador, quantidade_vendida)
                        valor_compra = quantidade_vendida * i.produto.preco

                        DaoVenda.salvar(vendido)
            temp.append([Produto(i.produto.nome, i.produto.preco, i.produto.categoria), i.quantidade])

        arq = open('estoque.txt', 'w')
        arq.write('')

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(f'{i[0].nome}|{i[0].preco}|{i[0].categoria}|{str(i[1])}\n')
        if existe is False:
            print('O produto não existe')
            return None
        elif not quantidade:
            print('A quantidade vendida não contém em estoque')
            return None
        else:
            print('Venda realizada com sucesso!')
            return valor_compra

    def relatorio_produtos(self):
        vendas = DaoVenda.ler()
        produtos = []
        a = 1

        print('Esses são os produtos mais vendidos\n')

        for i in vendas:
            nome = i.item_vendido.nome
            quantidade = int(i.quantidade_vendida)
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + quantidade}
                                    if (x['produto'] == nome) else(x), produtos))
            else:
                produtos.append({'produto': nome, 'quantidade': quantidade})

        ordenado = sorted(produtos, key=lambda k: k['quantidade'], reverse=True)

        for i in ordenado:
            print(f'==========Produto [{a}]==========')
            print(f"Produto: {i['produto']}\n"
                    f"Quantidade: {i['quantidade']}\n")
            a += 1

    def mostrar_vendas(self, data_inicio, data_termino):
        vendas = DaoVenda.ler()
        data_inicio1 = datetime.strptime(data_inicio, '%d/%m/%Y')
        data_termino1 = datetime.strptime(data_termino, '%d/%m/%Y')

        vendas_selecionadas = list(filter(lambda x: datetime.strptime(x.data, '%d/%m/%Y - %H:%M:%S') >= data_inicio1 
                                          and datetime.strptime(x.data, '%d/%m/%Y - %H:%M:%S') <= data_termino1, vendas))

        cont = 1
        total = 0
        for i in vendas_selecionadas:
            print(f"==========Venda [{cont}]==========")
            print(f"Nome: {i.item_vendido.nome}\n"
                  f"Data: {i.data}\n"
                  f"Quantidade: {i.quantidade_vendida}\n"
                  f"Cliente: {i.comprador}\n"
                  f"Vendedor: {i.vendedor}\n")
            total += int(i.item_vendido.preco) * int(i.quantidade_vendida)
            cont += 1
        print(f"Total vendido: R$ {total:.2f}")


class ControllerFornecedor:
    def cadastrar_fornecedor(self, nome, cnpj, telefone, categoria):
        lista_fornecedores = DaoFornecedor.ler()
        lista_cnpj = list(filter(lambda x: x.cnpj == cnpj, lista_fornecedores))
        lista_telefone = list(filter(lambda x: x.telefone == telefone, lista_fornecedores))
        if len(lista_cnpj) > 0:
            print("O cnpj já existe")
        elif len(lista_telefone) > 0:
            print("O telefone já existe")
        else:
            if len(cnpj) == 14 and len(telefone) <= 11:
                DaoFornecedor.salvar(Fornecedor(nome, cnpj, telefone, categoria))
                print("Fornecedor cadastrado com sucesso!")
            else:
                print("Digite um cnpj ou telefone válido")

    def alterar_fornecedor(self, nome_a_alterar, novo_nome, novo_cnpj, novo_telefone, nova_categoria):
        lista_fornecedores = DaoFornecedor.ler()
        existe = list(filter(lambda x: x.nome == nome_a_alterar, lista_fornecedores))
        if len(existe) > 0:
            existe = list(filter(lambda x: x.cnpj == novo_cnpj, lista_fornecedores))
            if len(existe) == 0:
                lista_fornecedores = list(map(lambda x: Fornecedor(novo_nome, novo_cnpj, novo_telefone, nova_categoria)
                                              if(x.nome == nome_a_alterar) else(x), lista_fornecedores))
            else:
                return print('O CNPJ já existe')
        else:
            return print('O fornecedor que deseja alterar não existe')

        with open('fornecedores.txt', 'w') as arq:
            for fornecedor in lista_fornecedores:
                arq.writelines(f'{fornecedor.nome}|{fornecedor.cnpj}|{fornecedor.telefone}|{fornecedor.categoria}\n')
            print('Fornecedor alterado com sucesso')
    
    def remover_fornecedor(self, nome):
        lista_fornecedores = DaoFornecedor.ler()
        existe = list(filter(lambda x: x.nome == nome, lista_fornecedores))
        if len(existe) > 0:
            for fornecedor in range(len(lista_fornecedores)):
                if lista_fornecedores[fornecedor].nome == nome:
                    del lista_fornecedores[fornecedor]
                    break
        else:
            print("O fornecedor que deseja remover não existe")
            return None

        with open('fornecedores.txt', 'w', encoding='utf-8') as arq:
            for fornecedor in lista_fornecedores:
                arq.writelines(f'{fornecedor.nome}|{fornecedor.cnpj}|{fornecedor.telefone}|{fornecedor.categoria}\n')
            print('Fornecedor removido com sucesso')

    def mostrar_fornecedores(self):
        lista_fornecedores = DaoFornecedor.ler()
        if len(lista_fornecedores) == 0:
            print("Nenhum fornecedor cadastrado")
            return None
        else:
            print("========== Fornecedores ==========")            
            for fornecedor in lista_fornecedores:
                print(f"Categoria fornecida: {fornecedor.categoria}\n"
                      f"Nome: {fornecedor.nome}\n"
                      f"Telefone: {fornecedor.telefone}\n"
                      f"CNPJ: {fornecedor.cnpj}\n")


class ControllerCliente:
    def cadastrar_cliente(self, nome, telefone, cpf, email, endereco):
        lista_clientes = DaoPessoa.ler()
        existe = list(filter(lambda x: x.cpf == cpf, lista_clientes))
        if len(existe) > 0:
            print("O CPF já existe")
            return None
        else:
            if len(cpf) == 11 and len(telefone) <= 11:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print("Cliente cadastrado com sucesso!")
            else:
                print("Digite um CPF válido")
    
    def alterar_cliente(self, cpf_a_alterar, novo_nome, novo_telefone, novo_cpf, novo_email, novo_endereco):
        lista_clientes = DaoPessoa.ler()
        existe = list(filter(lambda x: x.cpf == cpf_a_alterar, lista_clientes))
        if len(existe) > 0:
            if len(novo_cpf) >= 10 and len(novo_cpf) <= 11:
                lista_clientes = list(map(lambda x: Pessoa(novo_nome, novo_telefone, novo_cpf, novo_email, novo_endereco) 
                                        if(x.cpf == cpf_a_alterar) else(x), lista_clientes))
                print("Dados alterados com sucesso!")
            else:
                print("CPF inválido")
                return None
        else:
            print("O CPF informado não existe")
            return None

        with open('pessoas.txt', 'w', encoding='utf-8') as arq:
            for cliente in lista_clientes:
                arq.writelines(f'{cliente.nome}|{cliente.telefone}|{cliente.cpf}|{cliente.email}|{cliente.endereco}\n')

    def remover_cliente(self, cpf_a_remover):
        lista_clientes = DaoPessoa.ler()
        existe = list(filter(lambda x: x.cpf == cpf_a_remover, lista_clientes))
        if len(existe) > 0:
            for i, cliente in enumerate(lista_clientes):
                if cliente.cpf == cpf_a_remover:
                    del lista_clientes[i]
                    print("Cliente removido com sucesso")
                    break
        else:
            print("O CPF que você digitou não existe")

        with open('pessoas.txt', 'w', encoding='utf-8') as arq:
            for cliente in lista_clientes:
                arq.writelines(f'{cliente.nome}|{cliente.telefone}|{cliente.cpf}|{cliente.email}|{cliente.endereco}\n')

    def mostrar_clientes(self):
        lista_clientes = DaoPessoa.ler()

        if len(lista_clientes) == 0:
            print("Nenhum cliente cadastrado")
            return None
        else:
            print("========== Clientes ==========")
            for cliente in lista_clientes:
                print(f"Nome: {cliente.nome}\n"
                      f"Telefone: {cliente.telefone}\n"
                      f"CPF: {cliente.cpf}\n"
                      f"E-mail: {cliente.email}\n"
                      f"Endereço: {cliente.endereco}\n")
