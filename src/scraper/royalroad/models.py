from datetime import datetime

from pydantic import BaseModel


class RoyalRoadModel(BaseModel):
    """Model representing a RoyalRoad story.

    Attributes
    ----------
    title : str
        The title of the story.
    genres : list[str]
        List of genres associated with the story.
    followers : int
        Number of followers the story has.
    rating : float
        The rating of the story.
    pages : int
        Number of pages in the story.
    view : int
        Number of views the story has.
    chapters : int
        Number of chapters in the story.
    last_updated : datetime
        The last updated datetime of the story.
    description : str
        Description of the story.
    """

    title: str
    genres: list[str]
    followers: int
    rating: float
    pages: int
    view: int
    chapters: int
    last_updated: datetime
    description: str
    new: bool = True
