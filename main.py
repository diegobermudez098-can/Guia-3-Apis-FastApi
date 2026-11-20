from fastapi import FastAPI
from routers import auth, productos, categorias

app = FastAPI(title="API Tienda - Guia 3 (Seguridad)")

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(categorias.router)
