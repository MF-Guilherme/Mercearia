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

a = ControllerCategoria()
a.mostrar_categoria()