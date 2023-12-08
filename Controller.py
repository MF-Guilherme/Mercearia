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
                    x = list(map(lambda x: Estoque(Produto(novo_nome, novo_preco, nova_categoria), nova_quantidade) if (x.produto.nome == nome_a_alterar) else (x), x))
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

# a = ControllerVenda()
# a.cadastrar_venda('abacaxi','Jose', 'Guilherme', 9)

# a = ControllerEstoque()
# a.mostrar_estoque()
# a.cadastrar_produto('abacaxi', 6, 'Frios', 90)

# a = ControllerVenda()
# a.relatorio_produtos()

# a = ControllerVenda()
# a.mostrar_vendas("01/11/2023", "30/12/2023")