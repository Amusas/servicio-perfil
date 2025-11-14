from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.profile_routes import router as profile_router
from logger.logger import info, error
from datetime import datetime
import os
import time

app = FastAPI(
    title="Servicio de Perfil de Usuario",
    description="Microservicio para gestionar perfiles de usuario",
    version="1.0.0"
)

# Include routers
app.include_router(profile_router)

# Tiempo de inicio y versión
START_TIME = time.time()
VERSION = "1.0.0"

def format_uptime(seconds):
    """Formatea el tiempo de ejecución"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

@app.get("/health")
def health_check():
    """Health check endpoint con formato estándar"""
    uptime_seconds = time.time() - START_TIME
    start_time_iso = datetime.fromtimestamp(START_TIME).isoformat() + "Z"
    
    return {
        "status": "UP",
        "checks": [
            {
                "data": {
                    "from": start_time_iso,
                    "status": "READY"
                },
                "name": "Readiness check",
                "status": "UP"
            },
            {
                "data": {
                    "from": start_time_iso,
                    "status": "ALIVE"
                },
                "name": "Liveness check",
                "status": "UP"
            }
        ],
        "version": VERSION,
        "uptime": format_uptime(uptime_seconds),
        "uptimeSeconds": int(uptime_seconds)
    }

@app.get("/health/ready")
def health_ready():
    """Readiness check endpoint"""
    uptime_seconds = time.time() - START_TIME
    return {
        "status": "READY",
        "version": VERSION,
        "uptime": format_uptime(uptime_seconds),
        "uptimeSeconds": int(uptime_seconds)
    }

@app.get("/health/live")
def health_live():
    """Liveness check endpoint"""
    uptime_seconds = time.time() - START_TIME
    return {
        "status": "ALIVE",
        "version": VERSION,
        "uptime": format_uptime(uptime_seconds),
        "uptimeSeconds": int(uptime_seconds)
    }


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

