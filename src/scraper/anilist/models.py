from pydantic import BaseModel


class AniListModel(BaseModel):
    """Represents an AniList media item.

    Attributes
    ----------
    title : str
        The title of the media.
    genres : list[str]
        List of genres associated with the media.
    popularity : int
        Popularity score of the media.
    favorites : int
        Number of users who have favorited the media.
    rating : float
        Average rating of the media.
    status : str
        Current status of the media.
    description : str
        Description or synopsis of the media.
    new : bool, optional
        Indicates if the media is new (default is True).
    """

    title: str
    genres: list[str]
    popularity: int
    favorites: int
    rating: float
    status: str
    description: str
    new: bool = True
