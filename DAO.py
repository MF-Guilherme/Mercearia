from Models import *

class DaoCategoria:
    
    @classmethod
    def salvar(cls, categoria):
        with open('categorias.txt', 'a') as arq:
            arq.writelines(categoria)
            arq.writelines('\n')

    
    @classmethod
    def ler(cls):
        with open('categorias.txt', 'r') as arq:
            cls.categoria = arq.readlines()

        cls.categoria = list(map(lambda x: x.replace('\n', ''), cls.categoria))
        print(cls.categoria)

        cat = []
        for i in cls.categoria:
            cat.append(Categoria(i))
        
        return cat
        
class DaoVenda:

    @classmethod
    def salvar(cls, venda: Venda):
        with open('vendas.txt', 'a') as arq:
            arq.writelines(f'{venda.itemVendido.nome}|{venda.itemVendido.preco}|{venda.itemVendido.categoria}|{venda.vendedor}|{venda.comprador}|{venda.quantidadeVendida}|{venda.data}\n')

    @classmethod
    def ler(cls):
        with open('vendas.txt', 'r') as arq:
            cls.venda = arq.readlines()

        cls.venda = list(map(lambda x: x.replace('\n', ''), cls.venda))
        cls.venda = list(map(lambda x: x.split('|'), cls.venda))
        vend = []
        for i in cls.venda:
            vend.append(Venda(Produto(i[0], i[1], i[2]), i[3], i[4], i[5], i[6]))
        return vend

class DaoEstoque:

    @classmethod
    def salvar(cls, produto: Produto, quantidade):
        with open('estoque.txt', 'a') as arq:
            arq.writelines(f'{produto.nome}|{produto.preco}|{produto.categoria}|{quantidade}\n')
            
        
    @classmethod
    def ler(cls):
        with open('estoque.txt', 'r') as arq:
            cls.estoque = arq.readlines()

        cls.estoque = list(map(lambda x: x.replace('\n', ''), cls.estoque))
        cls.estoque = list(map(lambda x: x.split('|'), cls.estoque))

        estoque = []
        for i in cls.estoque:
            estoque.append(Estoque(Produto(i[0], i[1], i[2]), i[3]))
        return estoque

class DaoFornecedor:

    @classmethod
    def salvar(cls, fornecedor: Fornecedor):
        with open('fornecedores.txt', 'a') as arq:
            arq.writelines(f'{fornecedor.nome}|{fornecedor.cnpj}|{fornecedor.telefone}|{fornecedor.categoria}\n')
    
    @classmethod
    def ler(cls):
        with open('fornecedores.txt', 'r') as arq:
            cls.fornecedores = arq.readlines()

            cls.fornecedores = list(map(lambda x: x.replace('\n', ''), cls.fornecedores))
            cls.fornecedores = list(map(lambda x: x.split('|'), cls.fornecedores))

            fornecedores = []

            for fornecedor in cls.fornecedores:
                fornecedores.append(Fornecedor(fornecedor[0], fornecedor[1], fornecedor[2], fornecedor[3]))
            
            return fornecedores

class DaoProduto:

    @classmethod
    def salvar(cls, produto: Produto):
        with open('produtos.txt', 'a') as arq:
            arq.writelines(f'{produto.nome}|{produto.preco}|{produto.categoria}\n')

    @classmethod
    def ler(cls):
        with open('produtos.txt', 'r') as arq:
            cls.produtos = arq.readlines()

            cls.produtos = list(map(lambda x: x.replace('\n', ''), cls.produtos))
            cls.produtos = list(map(lambda x: x.split('|'), cls.produtos))

            produtos = []
            for produto in cls.produtos:
                produtos.append(Produto(produto[0], produto[1], produto[2]))
            return produtos
