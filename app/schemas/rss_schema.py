from pydantic import BaseModel, Field
from typing import List, Optional

class RSSItem(BaseModel):
    title: str = Field(..., description="title of the article")
    link: str = Field(..., description="link to the article")
    description: Optional[str] = Field(None, description="description of the article")
    pubDate: Optional[str] = Field(None, description="publication date of the article")

class RSSFeed(BaseModel):
    items: List[RSSItem] = Field(..., description="rss feed items list")
