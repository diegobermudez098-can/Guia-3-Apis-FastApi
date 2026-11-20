# Guía 3 - APIs con FastAPI: Seguridad

API de una tienda (productos y categorías) a la que se le agregó seguridad: hashing de contraseñas con bcrypt, login con OAuth2 + JWT, protección de endpoints con `Depends` y autorización por roles (admin y cliente). Los datos siguen en memoria.

## Instalación y ejecución

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Luego abrir http://127.0.0.1:8000/docs

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | admin |
| ana | ana123 | cliente |

## Permisos

| Endpoint | Acceso |
|---|---|
| `GET /productos`, `GET /productos/{id}` | Público |
| `GET /categorias`, `GET /categorias/{id}` | Público |
| `POST` y `PUT` de productos y categorías | Usuario autenticado |
| `DELETE` de productos y categorías | Solo rol admin |
| `POST /auth/login` | Público (entrega el token) |
| `POST /auth/registro` | Público (crea usuario con rol cliente) |
| `GET /auth/yo` | Usuario autenticado |

Sin token se responde 401; con token pero sin el rol necesario, 403.

## Estructura

```
main.py
seguridad.py
requirements.txt
routers/
    auth.py
    productos.py
    categorias.py
```
