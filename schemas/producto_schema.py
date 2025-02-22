from pydantic import BaseModel
from random import choice
import string
from .categoria_schema import Categoria
from db.db import conn
from models.models import productos
from datetime import date


class Producto(BaseModel):
    sku: str | None = None
    nombre: str
    descripcion: str
    precio: float
    imagen: str
    stock: int
    esta_disponible: bool = True
    fecha_creacion: date = date.today()
    categoria_id: int

    def generar_sku(self) -> str:
        letras = "".join(choice(string.ascii_uppercase) for _ in range(3))
        numeros = "".join(choice(string.digits) for _ in range(4))
        return f"{letras}-{numeros}"

    def __init__(self, **data):
        super().__init__(**data)
        if self.sku is None:
            self.sku = self.generar_sku()

    def producto_schema(producto) -> dict:
        categoria = Categoria.get_categoria(producto.categoria_id)
        return {
            "sku": producto.sku,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "imagen": producto.imagen,
            "stock": producto.stock,
            "categoria": categoria,
        }

    def productos_schemas(productos) -> list:
        return [Producto.producto_schema(producto) for producto in productos]

    def producto_schema_db(producto) -> dict:
        return {
            "sku": producto.sku,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "imagen": producto.imagen,
            "stock": producto.stock,
            "categoria_id": producto.categoria_id,
        }

    def productos_schemas_db(productos) -> list:
        return [Producto.producto_schema_db(producto) for producto in productos]

    def get_producto(sku: str) -> dict:
        query = productos.select().where(productos.c.sku == sku)
        return Producto.producto_schema(conn.execute(query).first())
