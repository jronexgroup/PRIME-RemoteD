import httpx
from config import config


class API:
    def __init__(self):
        self.base_url = config.backend_url.rstrip("/")
        self.headers = {"X-API-Key": config.api_key}
        self.client = httpx.AsyncClient(timeout=60, headers=self.headers)

    async def register(self) -> bool:
        try:
            resp = await self.client.post(
                f"{self.base_url}/register",
                json={
                    "device_id": config.device_id,
                    "device_name": config.device_name,
                },
            )
            return resp.status_code == 200
        except Exception:
            return False

    async def poll_commands(self, timeout: int = 30) -> list[dict]:
        try:
            resp = await self.client.get(
                f"{self.base_url}/commands",
                params={"device_id": config.device_id, "timeout": timeout, "api_key": config.api_key},
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("commands", [])
            return []
        except Exception:
            return []

    async def send_result(self, command_id: str, status: str, message: str, data: dict = None) -> bool:
        try:
            resp = await self.client.post(
                f"{self.base_url}/result",
                json={
                    "id": command_id,
                    "status": status,
                    "message": message,
                    "data": data or {},
                },
            )
            return resp.status_code == 200
        except Exception:
            return False

    async def upload_file(self, file_path: str, filename: str, file_type: str = "screenshot") -> bool:
        try:
            with open(file_path, "rb") as f:
                resp = await self.client.post(
                    f"{self.base_url}/upload",
                    files={"file": (filename, f, "image/png")},
                    data={"device_id": config.device_id, "file_type": file_type},
                )
            return resp.status_code == 200
        except Exception:
            return False

    async def health_check(self) -> bool:
        try:
            resp = await self.client.get(f"{self.base_url}/health")
            return resp.status_code == 200
        except Exception:
            return False

    async def close(self):
        await self.client.aclose()


api = API()
