from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import usuario_route, producto_route, categoria_route


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_route.router)
app.include_router(producto_route.router)
app.include_router(usuario_route.router)


@app.get("/")
def main():
    return {"message": "Hello World"}
