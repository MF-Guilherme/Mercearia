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