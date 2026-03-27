import os

class Config:
    API_KEY = os.getenv("AF_API_KEY", "aa7c90660a38281a3d37c6538a9cc760")
    BASE_URL = "https://v3.football.api-sports.io"
    LOG_LEVEL = "INFO"
