from fastapi import APIRouter

order_router = APIRouter(prefix='/orders', tags=['Orders'])

@order_router.get('/')
async def orders():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """
    return {'message': 'Você acessou a rota de pedidos'}