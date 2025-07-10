from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

# Alembic é responsável por fazer as migrates/migrations no fastapi

# Cria a conexão do seu banco
db = create_engine("sqlite:///database/banco.db3")

# Cria a base do seu banco de dados
Base = declarative_base()

# Cria as classes/tabelas do banco
class Usuario(Base):
    # Definir o nome da tabela
    __tablename__ = "usuarios"

    # PRECISAMOS DEFINIR A COLUNA NO BANCO DE DADOS
    # Usamos o Column
    # Passamos como primeiro parâmetro o nome que irá ficar na tabela
    # Logo após passamos o Tipo do dado, depois passamos se ele pode ser nulo ou não
    # ID por padrão geral nos bancos de dados é comum, possuir o primary_key e o autoincrement,
    # Pois ele será um id único e ele se auto incrementará, ou seja, toda vez que surgir um novo usuário
    # Ele vai incrementar +1 no ID  
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    # Aqui no Admin, usamos o parâmetro default=false, pois nesse caso, caso eu não passe no momento
    # Da criação do usuário se o usuário é admin ou não, ele irá criar por padrão com false, ou seja,
    # Não sendo admin
    admin = Column("admin", Boolean, default=False)

    # A função init, como o nome já diz serve pra inicializar, ou seja, toda vez que a clase usuário for
    # Chamada ele chama a função init
    # Passando o parâmetro self, pois está referenciando a própria classe 
    # E após o self, colocar os parâmetros que eu quero obrigar o usuário a passar quando eu for criar um
    # Usuário
    def __init__(self, nome, email, senha, ativo=True, admin=False) -> None:
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin 

class Pedido(Base): 
    __tablename__ = "pedidos"

    """STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO"),
    ) """

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # Pendente, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float, nullable=False)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
# Executa a criação dos metadados do seu banco (Cria efetivamente o banco de dados)