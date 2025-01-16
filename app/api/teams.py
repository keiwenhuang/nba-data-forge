from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("team/{team_name}")
def get_team():
    pass
