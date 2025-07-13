from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from sqlalchemy.orm import Session
from dependencies.db import pegar_sessao
from app.main import bcrypt_context
from schemas.usuario import UsuarioSchema


auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota de autenticação"}

@auth_router.post('/criar_conta')
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):  
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
            usuario_schema.nome, 
            usuario_schema.email, 
            senha_criptografada, 
            usuario_schema.ativo, 
            usuario_schema.admin
        )

        session.add(novo_usuario)                                                                   
        session.commit()
        
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}