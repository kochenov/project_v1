from core.database.base_repository import BaseRepository
from modules.links.models import Link


class LinkRepository(BaseRepository):
    model = Link
