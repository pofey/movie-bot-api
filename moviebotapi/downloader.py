from moviebotapi.core.basemodel import BaseModel


class ClientTorrent(BaseModel):
    hash: str
    name: str
    save_path: str
    content_path: str
    size: int
    size_str: str
    dl_speed: int
    dl_speed_str: str
    up_speed: int
    up_speed_str: str
    progress: float
    uploaded: int
    uploaded_str: str
    downloaded: int
    downloaded_str: str
    seeding_time: int
    ratio: float
    tracker: str
