from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["Root"])


@router.get(path="/", description="Root endpoint", include_in_schema=False)
def root():
    ascii_art = """
 __          __  _ 
 \ \        / / | |
  \ \  /\  / /__| | ___ ___  _ __ ___   ___
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ 
    \  /\  /  __/ | (_| (_) | | | | | |  __/
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|
                                                                                                                                                                                       
    """
    return PlainTextResponse(content=ascii_art)


@router.get(path="/health", description="Health check")
def health_check():
    return {"status": "OK"}