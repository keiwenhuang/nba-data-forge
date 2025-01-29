from pydantic import BaseModel, ConfigDict


class TeamNames(BaseModel):
    team: str

    model_config = ConfigDict(from_attributes=True)
