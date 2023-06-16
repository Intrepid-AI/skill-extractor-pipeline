from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health_check"])
async def checkhealth():
    return {"status":200}

@router.get("/", tags=["health_check"])
async def entrypoint():
    return {"message" : "Welcome to Skill Extractor Platform"}