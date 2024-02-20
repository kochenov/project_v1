from core.database.base_repository import BaseRepository
from modules.parsing_process.models import Proces


class ProcessParsingRepository(BaseRepository):
    model = Proces
