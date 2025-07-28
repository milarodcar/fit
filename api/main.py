from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.endpoints import clients, home, options

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(home.router, prefix="")
app.include_router(clients.router, prefix="/clients", tags= ["clients"])
app.include_router(options.router, prefix="/options")

@app.on_event("startup")
async def print_routes():
    print("\nRegistered Routes:")
    for route in app.routes:
        if hasattr(route, "methods"):
            print(f"Path: {route.path}, Methods: {route.methods}")
        elif hasattr(route, "routes"):  # For mounted apps
            for subroute in route.routes:
                if hasattr(subroute, "methods"):
                    print(f"Path: {route.path}{subroute.path}, Methods: {subroute.methods}")
    print("\n")