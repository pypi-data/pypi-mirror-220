from abc import ABC, abstractmethod
from io import BytesIO

import requests
from PIL import Image
from pointset import PointSet


class ImageRequester(ABC):
    """
    Abstract base class for requesting images from a server.

    This class defines the interface for requesting images from a server. Subclasses must implement the `request` method.

    Attributes:
        None
    """

    def __init__(self):
        self.request_epsg: int = 25832

    @abstractmethod
    def request(self, pointset: PointSet, width: float, height: float) -> tuple[Image.Image, list[float]]:
        pass


class TIMImageRequester(ImageRequester):
    """
    A class for requesting aerial images from the TIM (Topografische und Informations-Management) server.

    This class inherits from the abstract base class `ImageRequester` and implements the `request` method to request aerial images from the TIM server.

    Attributes:
        None
    """

    def __init__(self):
        super().__init__()
        self.request_epsg = 25832
        self.url = "https://www.wcs.nrw.de/geobasis/wcs_nw_dop?REQUEST=GetCoverage&SERVICE=WCS&VERSION=2.0.1&COVERAGEID=nw_dop&FORMAT=image/jpeg"

    def request(self, pointset: PointSet, width: float, height: float) -> tuple[Image.Image, list]:
        """
        Requests an aerial image from the NRW, Germany WCS server for a given pointset and dimensions.

        Args:
            pointset (PointSet): The pointset to request the image for.
            width (float): The width of the image in meters.
            height (float): The height of the image in meters.

        Returns:
            Image: The requested aerial image.
        """
        pos = pointset.to_epsg(25832)
        extent = [pos.x - (width / 2), pos.x + (width / 2), pos.y - (height / 2), pos.y + (height / 2)]
        subset = f"SUBSET=x({extent[0]},{extent[1]})&SUBSET=y({extent[2]},{extent[3]})&RANGESUBSET=1,2,3"
        uri = f"{self.url}&{subset}"
        response = requests.get(uri)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
        else:
            raise requests.RequestException("Failed to get aerial image! This function only works for NRW, Germany.")
        return img, extent
