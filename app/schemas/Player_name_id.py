from pydantic import BaseModel, ConfigDict


class PlayerNameID(BaseModel):
    player_name: str
    player_id: str

    model_config = ConfigDict(from_attributes=True)
