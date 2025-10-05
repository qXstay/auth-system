from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.resource_router import router as resource_router
from routes.user_router import router as user_router
from middlewares.auth_middleware import AuthMiddleware
from database.db import Base, engine
import models.user
import models.role
import models.product
import models.access_roles_rules
from fastapi.openapi.utils import get_openapi

# создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth System Project")
app.add_middleware(AuthMiddleware)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(resource_router, prefix="/resource", tags=["Resource"])

@app.get("/")
def read_root():
    return {"message": "Auth System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Auth System Project",
        version="1.0.0",
        description="Custom authentication system",
        routes=app.routes,
    )

    # Добавляем схему аутентификации
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Добавляем требования безопасности ко всем защищенным путям
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi