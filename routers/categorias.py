from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

router = APIRouter(prefix="/categorias", tags=["Categorias"])


class CategoriaEntrada(BaseModel):
    nombre: str
    descripcion: str


categorias = [
    {"id": 1, "nombre": "Ropa", "descripcion": "Prendas de vestir"},
    {"id": 2, "nombre": "Accesorios", "descripcion": "Gorras, bolsos y mas"},
]


def buscar_categoria(categoria_id: int):
    for c in categorias:
        if c["id"] == categoria_id:
            return c
    return None


# LISTAR: publico
@router.get("")
def listar_categorias():
    return categorias


# OBTENER UNA: publico
@router.get("/{categoria_id}")
def obtener_categoria(categoria_id: int):
    categoria = buscar_categoria(categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


# CREAR: requiere estar autenticado
@router.post("", status_code=201)
def crear_categoria(datos: CategoriaEntrada,
                    usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    nuevo_id = max([c["id"] for c in categorias], default=0) + 1
    nueva = {"id": nuevo_id, **datos.model_dump()}
    categorias.append(nueva)
    return {"mensaje": "Categoria creada", "categoria": nueva,
            "creado_por": usuario["username"]}


# ACTUALIZAR: requiere estar autenticado
@router.put("/{categoria_id}")
def actualizar_categoria(categoria_id: int, datos: CategoriaEntrada,
                         usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    categoria = buscar_categoria(categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    categoria.update(datos.model_dump())
    return {"mensaje": "Categoria actualizada", "categoria": categoria}


# BORRAR: requiere rol admin
@router.delete("/{categoria_id}")
def eliminar_categoria(categoria_id: int,
                       admin: dict = Depends(seguridad.requerir_admin)):
    categoria = buscar_categoria(categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    categorias.remove(categoria)
    return {"mensaje": "Categoria eliminada"}
