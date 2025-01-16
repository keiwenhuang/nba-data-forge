from fastapi import FastAPI

app = FastAPI(title="NBA Data Forge", version="0.0.1")


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/player/{str:player_id}")
def get_player(player_id):
    return
