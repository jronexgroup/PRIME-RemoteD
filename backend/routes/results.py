from fastapi import APIRouter, Request
from services.command_queue import device_manager, CommandResult
import logging

logger = logging.getLogger("backend.results")
router = APIRouter()


@router.post("/result")
async def receive_result(request: Request):
    data = await request.json()
    result = CommandResult(**data)
    device_manager.store_result(result)
    logger.info(f"Received result for command {result.id}: {result.status}")
    return {"ok": True}
