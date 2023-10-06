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

    def alterar_produto(self, nome_a_alterar, novo_nome, novo_preco, nova_categoria, nova_quantidade):
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

