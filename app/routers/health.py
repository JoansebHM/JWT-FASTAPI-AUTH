from fastapi import APIRouter, Response, status

router = APIRouter()


@router.get("/health")
async def health_check():
    return Response(status_code=status.HTTP_200_OK)
