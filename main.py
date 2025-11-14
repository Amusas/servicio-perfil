from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.profile_routes import router as profile_router
from logger.logger import info, error
from datetime import datetime
import os

app = FastAPI(
    title="Servicio de Perfil de Usuario",
    description="Microservicio para gestionar perfiles de usuario",
    version="1.0.0"
)

# Include routers
app.include_router(profile_router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "profile-service"}


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    """Global exception handler"""
    error("[FastAPI]", "Error no manejado", {
        "path": str(request.url),
        "error": str(exc)
    })
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8087"))
    info("[Main]", "Iniciando servicio de perfil", {"port": port})
    uvicorn.run(app, host="0.0.0.0", port=port)

