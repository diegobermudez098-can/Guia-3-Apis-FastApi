from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import seguridad

router = APIRouter(prefix="/productos", tags=["Productos"])


class ProductoEntrada(BaseModel):
    nombre: str
    precio: float
    stock: int


productos = [
    {"id": 1, "nombre": "Camiseta", "precio": 35000, "stock": 20},
    {"id": 2, "nombre": "Gorra", "precio": 25000, "stock": 15},
]


def buscar_producto(producto_id: int):
    for p in productos:
        if p["id"] == producto_id:
            return p
    return None


# LISTAR: publico
@router.get("")
def listar_productos():
    return productos


# OBTENER UNO: publico
@router.get("/{producto_id}")
def obtener_producto(producto_id: int):
    producto = buscar_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


# CREAR: requiere estar autenticado
@router.post("", status_code=201)
def crear_producto(datos: ProductoEntrada,
                   usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    nuevo_id = max([p["id"] for p in productos], default=0) + 1
    nuevo = {"id": nuevo_id, **datos.model_dump()}
    productos.append(nuevo)
    return {"mensaje": "Producto creado", "producto": nuevo,
            "creado_por": usuario["username"]}


# ACTUALIZAR: requiere estar autenticado
@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, datos: ProductoEntrada,
                        usuario: dict = Depends(seguridad.obtener_usuario_actual)):
    producto = buscar_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.update(datos.model_dump())
    return {"mensaje": "Producto actualizado", "producto": producto}


# BORRAR: requiere rol admin
@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int,
                      admin: dict = Depends(seguridad.requerir_admin)):
    producto = buscar_producto(producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    productos.remove(producto)
    return {"mensaje": "Producto eliminado"}
