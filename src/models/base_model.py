from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentBaseModel(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    async def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        await super().save(*args, **kwargs)