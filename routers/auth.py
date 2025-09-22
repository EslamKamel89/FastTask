from fastapi import APIRouter, FastAPI  # type: ignore

router = APIRouter()
@router.get('/auth')
async def get_user() :
    return {'user':'user authenticated'}