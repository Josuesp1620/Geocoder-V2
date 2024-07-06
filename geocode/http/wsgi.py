from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as uvicorn_run
from geocode.config import config, hooks
# from .base import CorsMiddleware

# Inicializar la aplicación FastAPI
app = FastAPI()

# Cargar configuración y registrar middlewares
config.load()
middlewares = [CORSMiddleware(app)]
hooks.register_http_middleware(middlewares)



# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registros de endpoints
hooks.register_http_endpoint(app)

# Definir punto de entrada para servidor
def simple(args):
    print(f"Serving HTTP on {args.host}:{args.port}...")
    uvicorn_run(app, host=args.host, port=int(args.port))

# Entrada principal para ejecutar el servidor
if __name__ == "__main__":
    import sys
    # Establecer host y puerto predeterminados si no se especifican argumentos
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = sys.argv[2] if len(sys.argv) > 2 else "7878"
    simple(args=type('', (), {'host': host, 'port': port})())
