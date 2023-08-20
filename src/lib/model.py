import logging

from lib.unpack import Unpacker, UnpackerError
from lib.image import ImageProcessor, ImageProcessorError


# Configure logging
logger = logging.getLogger(__name__)


class ModelError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Model:

    def __init__(self, filepath=None):
        self.images = {}
        self.config = {}
        self.filepath = filepath

        if self.filepath:
            self.load(filepath)

    def load(self, file_path=None):
        if file_path:
            self.filepath = file_path
        try:
            up = Unpacker(file_path).unpack()
            self.images = up.images
            self.config = up.config
        except UnpackerError as e:
            logger.error(f"Could not unpack model: {e}")
            return False

        self.extract_image_info()

    def extract_image_info(self):
        try:
            for image in self.images:
                img = ImageProcessor(self.images[image])
                img.validate()

                self.images[image]['info'] = {
                    'resolution_x': img.resolution_x,
                    'resolution_y': img.resolution_y,
                    'aspect_ratio': img.aspect_ratio
                }
            return True
        except ImageProcessorError as e:
            raise ModelError(e)
