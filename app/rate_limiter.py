import time
from fastapi import Request, HTTPException, status

class RateLimiter:
    def __init__(self, requests_limit: int = 5, time_window: int = 30):
        """
        :param requests_limit: Cuántas peticiones permitimos.
        :param time_window: En cuántos segundos (ej: 5 peticiones cada 60 seg).
        """
        self.requests_limit = requests_limit
        self.time_window = time_window
        # Diccionario para guardar IPs: { "127.0.0.1": [10:00:01, 10:00:02, ...] }
        self.clients = {}

    async def __call__(self, request: Request):
        """
        Esta función se ejecuta antes que el endpoint.
        FastAPI nos inyecta el objeto 'request' para ver la IP del cliente.
        """
        client_ip = request.client.host
        current_time = time.time()
        
        # 1. Si la IP no existe, la creamos
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        # 2. Limpiamos timestamps viejos (fuera de la ventana de tiempo)
        # Mantenemos solo los que ocurrieron hace menos de 'time_window' segundos
        self.clients[client_ip] = [
            t for t in self.clients[client_ip] 
            if current_time - t < self.time_window
        ]
        
        # 3. Verificamos si superó el límite
        if len(self.clients[client_ip]) >= self.requests_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Has excedido el límite de peticiones. Intenta más tarde."
            )
        
        # 4. Si pasa, registramos la petición actual
        self.clients[client_ip].append(current_time)