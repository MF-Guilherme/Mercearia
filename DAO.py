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

        categorias = []
        for i in cls.categoria:
            categorias.append(Categoria(i))
        
        return categorias


class DaoVenda:

    @classmethod
    def salvar(cls, venda: Venda):
        with open('vendas.txt', 'a') as arq:
            arq.writelines(f'{venda.item_vendido.nome}|{venda.item_vendido.preco}|{venda.item_vendido.categoria}|{venda.vendedor}|{venda.comprador}|{venda.quantidade_vendida}|{venda.data}\n')

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

        est = []
        if len(cls.estoque) > 0:
            for i in cls.estoque:
                est.append(Estoque(Produto(i[0], i[1], i[2]), int(i[3])))
        return est


class DaoFornecedor:

    @classmethod
    def salvar(cls, fornecedor: Fornecedor):
        with open('fornecedores.txt', 'a', encoding="utf-8") as arq:
            arq.writelines(f'{fornecedor.nome}|{fornecedor.cnpj}|{fornecedor.telefone}|{fornecedor.categoria}\n')
    
    @classmethod
    def ler(cls):
        with open('fornecedores.txt', 'r', encoding='utf-8') as arq:
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


class DaoPessoa:

    @classmethod
    def salvar(cls, pessoa: Pessoa):
        with open('pessoas.txt', 'a', encoding='utf-8') as arq:
            arq.writelines(f'{pessoa.nome}|{pessoa.telefone}|{pessoa.cpf}|{pessoa.email}|{pessoa.endereco}\n')

    @classmethod
    def ler(cls):
        with open('pessoas.txt', 'r', encoding='utf-8') as arq:
            cls.pessoas = arq.readlines()

            cls.pessoas = list(map(lambda x: x.replace('\n', ''), cls.pessoas))
            cls.pessoas = list(map(lambda x: x.split('|'), cls.pessoas))

            pessoas = []

            for pessoa in cls.pessoas:
                pessoas.append(Pessoa(pessoa[0], pessoa[1], pessoa[2], pessoa[3], pessoa[4]))
            return pessoas


class DaoFuncionario:

    @classmethod
    def salvar(cls, funcionario: Funcionario):
        with open('funcionarios.txt', 'a') as arq:
            arq.writelines(f'{funcionario.clt}|{funcionario.nome}|{funcionario.telefone}|{funcionario.cpf}|{funcionario.email}|{funcionario.endereco}\n')

    @classmethod
    def ler(cls):
        with open('funcionarios.txt', 'r') as arq:
            cls.funcionarios = arq.readlines()
            
            cls.funcionarios = list(map(lambda x: x.replace('\n', ''), cls.funcionarios))
            cls.funcionarios = list(map(lambda x: x.split('|'), cls.funcionarios))

            funcionarios = []

            for funcionario in cls.funcionarios:
                funcionarios.append(Funcionario(funcionario[0],funcionario[1],funcionario[2],funcionario[3],funcionario[4],funcionario[5]))
            return funcionarios
