from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from sqlalchemy.orm import Session
from dependencies.db import pegar_sessao
from dependencies.token import verificar_token
from app.main import bcrypt_context, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas.usuario import UsuarioSchema
from schemas.login import LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix='/auth', tags=['Auth'])

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False 
    
    return usuario 


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
    
# login -> email e senha -> token JWT (JSON WEB TOKEN)
@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    
    else: 
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.post('/login-form')
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    
    else: 
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    
@auth_router.post('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    
    return {
            "access_token": access_token,   
            "token_type": "Bearer"
        }