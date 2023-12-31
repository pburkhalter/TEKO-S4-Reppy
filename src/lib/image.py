import logging
from PIL import Image, UnidentifiedImageError, ImageOps
from settings import settings_dict

# Configure logging
logger = logging.getLogger(__name__)

"""
This module provides a class for image processing tasks.
It uses the PIL library for image operations and settings_dict for machine-specific settings.
"""


class ImageProcessorError(Exception):
    """
    Custom exception for image processing errors.
    """

    def __init__(self, message):
        super().__init__(message)


class ImageProcessor:
    """
    Class for image processing tasks.
    """
    __machine_resolution_x = None
    __machine_resolution_y = None
    __machine_aspect_ratio = None

    file = None
    image = None

    resolution_x = None
    resolution_y = None
    aspect_ratio = None

    def __init__(self, file_path=None):
        """
        Initialize the ImageProcessor instance with machine resolution and aspect ratio.

        Parameters:
            file_path (str, optional): The path to the image file.
        """
        self.__machine_resolution_x = settings_dict['machine']['resolution']['x']
        self.__machine_resolution_y = settings_dict['machine']['resolution']['y']
        self.__machine_aspect_ratio = self.__machine_resolution_x / self.__machine_resolution_y

        if file_path:
            self.file = file_path
            self.open()
            self.extract_properties()

    def open(self, file_path=None):
        """
        Open the image and load it into memory.

        Parameters:
            file_path (str, optional): The path to the image file.

        Raises:
            ImageProcessorError: If the image cannot be opened.
        """
        if file_path:
            self.file = file_path
        try:
            self.image = Image.open(self.file)
            self.image.load()  # force pillow to load the image into memory
        except (FileNotFoundError, PermissionError, UnidentifiedImageError) as e:
            raise ImageProcessorError(f"Error opening the image at '{self.file}': {e}")

    def extract_properties(self):
        """
        Extract image properties like resolution and aspect ratio.
        """
        width, height = self.image.size
        self.resolution_x = width
        self.resolution_y = height
        self.aspect_ratio = self.resolution_x / self.resolution_y

    def grayscale(self):
        """
        Convert the image to grayscale.
        """
        grayscale_image = ImageOps.grayscale(self.image)
        if not self.image == grayscale_image:
            self.image = grayscale_image

    def validate(self, to_grayscale=True):
        """
        Validate image properties and optionally convert to grayscale.

        Parameters:
            to_grayscale (bool, optional): Whether to convert the image to grayscale.

        Raises:
            ImageProcessorError: If the image properties are invalid.
        """
        if not self.resolution_x == self.__machine_resolution_x:
            logger.error("Image resolution width (x) does not match.")
            raise ImageProcessorError("Image resolution width (x) does not match.")
        if not self.resolution_y == self.__machine_resolution_y:
            logger.error("Image resolution height (y) does not match.")
            raise ImageProcessorError("Image resolution height (y) does not match.")
        if not self.aspect_ratio == self.__machine_aspect_ratio:
            logger.error("Could not extract properties.")
            raise ImageProcessorError("Could not extract properties.")

        if to_grayscale:
            self.grayscale()
