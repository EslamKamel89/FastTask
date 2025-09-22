from fastapi import APIRouter, FastAPI  # type: ignore

router = APIRouter(prefix='/auth' , tags=['auth'])
@router.get('/')
async def get_user() :
    return {'user':'user authenticated'}