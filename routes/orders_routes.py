from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.db import pegar_sessao
from schemas.pedido import PedidoSchema
from models.models import Pedido


order_router = APIRouter(prefix='/orders', tags=['Orders'])

@order_router.get('/')
async def orders():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """
    return {'message': 'Você acessou a rota de pedidos'}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do Pedido: {novo_pedido.id}"}