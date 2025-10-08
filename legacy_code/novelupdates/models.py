from datetime import datetime

from pydantic import BaseModel


class NovelUpdatesModel(BaseModel):
    """Model representing a NovelUpdates story.

    Attributes
    ----------
    title : str
        The title of the story.
    genres : list[str]
        List of genres associated with the story.
    readers : int
        Number of readers the story has.
    reviews : int
        Number of reviews the story has.
    rating : float
        The rating of the story.
    chapters : int
        Number of chapters in the story.
    last_updated : datetime
        The last updated datetime of the story.
    update_frequency : float
        Average update frequency in days.
    description : str
        Description of the story.
    """

    title: str
    genres: list[str]
    readers: int
    reviews: int
    rating: float
    chapters: int
    last_updated: datetime
    update_frequency: float
    description: str
    new: bool = True
