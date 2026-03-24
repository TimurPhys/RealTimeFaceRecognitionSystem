import re
from aiogram.filters import Filter
from aiogram.types import Message

class NameLatinitzaFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False
        
        pattern = r"^[A-Z][a-z]+\s+[A-Z][a-z]+$"
        return bool(re.match(pattern, message.text.strip()))