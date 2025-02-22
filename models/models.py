from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date, Time, Float, Boolean, CHAR
from db.db import metadata, engine
from datetime import date

categorias = Table(
    "categorias",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("descripcion", String(255), nullable=True),
)

productos = Table(
    "productos",
    metadata,
    Column("sku", CHAR(19), primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("descripcion", String(255), nullable=True),
    Column("precio", Float, nullable=False),
    Column("stock", Integer, nullable=False),
    Column("imagen", String(255), nullable=True),
    Column("esta_disponible", Boolean, nullable=False, default=True),
    Column("fecha_creacion", Date, nullable=False, default=date.today()),
    Column("categoria_id", Integer, ForeignKey("categorias.id"), nullable=False),
)

usuarios = Table(
    "usuarios",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("contrasena", String(255), nullable=True),
    Column("direccion", String(255), nullable=True),
    Column("telefono", String(255), nullable=True),
    Column("es_admin", Boolean, nullable=False, default=False),
    Column("es_activo", Boolean, nullable=False, default=True),
    Column("fecha_creacion", Date, nullable=False, default=date.today()),
    Column("fecha_actualizacion", Date, nullable=False, default=date.today()),
    Column("acepta_mails", Boolean, nullable=False, default=True),
)

pedidos = Table(
    "pedidos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("fecha", Date, nullable=False),
    Column("total", Float, nullable=False),
)

detalles_pedidos = Table(
    "detalles_pedidos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pedido_id", Integer, ForeignKey("pedidos.id"), nullable=False),
    Column("producto_id", String(10), ForeignKey("productos.sku"), nullable=False),
    Column("cantidad", Integer, nullable=False),
    Column("precio", Float, nullable=False),
)

carritos = Table(
    "carritos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("fecha_creacion", Time, nullable=False),
)

detalles_carrito = Table(
    "detalles_carrito",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("carrito_id", Integer, ForeignKey("carritos.id"), nullable=False),
    Column("producto_id", String(10), ForeignKey("productos.sku"), nullable=False),
    Column("cantidad", Integer, nullable=False),
)

favoritos = Table(
    "favoritos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False),
    Column("producto_id", String(10), ForeignKey("productos.sku"), nullable=False),
)

codigos_descuento = Table(
    "codigos_descuento",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("codigo", String(255), nullable=False),
    Column("descuento", Float, nullable=False),
    Column("fecha_vencimiento", Date, nullable=False),
)

metadata.create_all(engine)
