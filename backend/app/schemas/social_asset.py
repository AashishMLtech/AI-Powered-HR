from pydantic import BaseModel


class SocialAssetResponse(BaseModel):
    id: str
    platform: str
    caption: str
    groups: str
    visual_path: str

    model_config = {"from_attributes": True}
