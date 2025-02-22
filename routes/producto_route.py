from fastapi import APIRouter, HTTPException
from db.db import conn
from models.models import productos
from schemas.producto_schema import Producto

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_productos():

    productos_src = Producto.productos_schemas(
        conn.execute(
            productos.select().where(productos.c.stock > 0).order_by(productos.c.nombre)
        ).fetchall()
    )

    if not productos_src:
        raise HTTPException(status_code=404, detail="No hay productos registrados")

    return productos_src


@router.get("/agotados")
async def get_productos_agotados():

    productos_src = Producto.productos_schemas(
        conn.execute(
            productos.select()
            .where(productos.c.stock == 0)
            .order_by(productos.c.nombre)
        ).fetchall()
    )

    if not productos_src:
        raise HTTPException(status_code=404, detail="No hay productos agotados")

    return productos_src


@router.get("/all")
async def get_all_productos():

    productos_src = Producto.productos_schemas(
        conn.execute(productos.select().order_by(productos.c.nombre)).fetchall()
    )

    if not productos_src:
        raise HTTPException(status_code=404, detail="No hay productos registrados")

    return productos_src


@router.get("/{sku}")
async def get_producto(sku: str):

    try:
        producto_src = Producto.producto_schema(
            conn.execute(productos.select().where(productos.c.sku == sku)).fetchone()
        )
    except:
        producto_src = None

    if not producto_src:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return producto_src


@router.post("/")
async def create_producto(producto: Producto):

    nuevo_producto = Producto.producto_schema_db(producto)
    sku = nuevo_producto["sku"]
    print(sku)
    conn.execute(productos.insert().values(nuevo_producto))
    conn.commit()

    return Producto.producto_schema(
        conn.execute(productos.select().where(productos.c.sku == sku)).first()
    )


@router.put("/{sku}")
async def update_producto(sku: str, producto: Producto):

    producto_src = Producto.get_producto(sku)

    if not producto_src:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_src = Producto.producto_schema_db(producto)

    producto_src["sku"] = sku

    conn.execute(productos.update().values(producto_src).where(productos.c.sku == sku))
    conn.commit()

    return Producto.producto_schema(
        conn.execute(productos.select().where(productos.c.sku == sku)).first()
    )


@router.delete("/{sku}")
async def delete_producto(sku: str):

    try:
        producto_src = Producto.producto_schema_db(Producto.get_producto(sku))
    except:
        producto_src = None

    if not producto_src:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    producto_src["esta_disponible"] = False
    conn.execute(productos.update().values(producto_src).where(productos.c.sku == sku))
    conn.commit()

    return {"message": "Producto eliminada"}


@router.get("/categorias/{id}")
async def get_productos_por_categoria(id: int):

    productos_src = Producto.productos_schemas(
        conn.execute(
            productos.select()
            .where(productos.c.categoria_id == id)
            .order_by(productos.c.nombre)
        ).fetchall()
    )

    if not productos_src:
        raise HTTPException(
            status_code=404, detail="No hay productos registrados en esta categoria"
        )

    return productos_src