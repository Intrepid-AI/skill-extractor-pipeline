from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Check health"])
async def checkhealth():
    return {"status":200}

@router.get("/", tags=["Skills Extraction"])
async def entrypoint():
    return {"message" : "Welcome to Skill Extractor Platform"}