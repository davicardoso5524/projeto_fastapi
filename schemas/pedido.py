from pydantic import BaseModel


class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        from_attributes = True