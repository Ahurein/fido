from datetime import datetime
from optparse import Option
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class DocumentBaseModel(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    async def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        await super().save(*args, **kwargs)