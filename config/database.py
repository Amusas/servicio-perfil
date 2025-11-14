import os
import psycopg2
from psycopg2 import pool
from logger.logger import info, error, warn
import time


class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "database")
        self.port = os.getenv("DB_PORT", "5432")
        self.user = os.getenv("DB_USER", "admin_user")
        self.password = os.getenv("DB_PASSWORD", "supersecurepassword")
        self.database = os.getenv("DB_NAME", "usuariosdb")
        
        self.connection_pool = None
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize connection pool with retry logic"""
        max_retries = 5
        delay = 5
        
        for attempt in range(1, max_retries + 1):
            try:
                self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                    1, 20,
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                info("Database", "✅ Conectado con PostgreSQL", {
                    "host": self.host,
                    "db": self.database
                })
                return
            except Exception as err:
                error("Database", f"❌ Intento {attempt} fallido", {"error": str(err)})
                
                if attempt < max_retries:
                    warn("Database", f"🔄 Reintentando conexión en {delay} segundos...", {"attempt": attempt})
                    time.sleep(delay)
                else:
                    error("Database", "❌ Todos los intentos fallidos. Cerrando aplicación...")
                    raise
    
    def get_connection(self):
        """Get a connection from the pool"""
        if self.connection_pool:
            return self.connection_pool.getconn()
        raise Exception("Connection pool not initialized")
    
    def return_connection(self, conn):
        """Return a connection to the pool"""
        if self.connection_pool:
            self.connection_pool.putconn(conn)
    
    def close_all_connections(self):
        """Close all connections in the pool"""
        if self.connection_pool:
            self.connection_pool.closeall()


# Global database instance
db_config = DatabaseConfig()

