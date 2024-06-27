"""
Module for loading and caching images using different file systems and locations.

This module provides an abstract base class `ImageLoader` for loading images
and a concrete implementation `CacheImageLoader` that supports caching the images
to avoid redundant loading operations.
"""

from abc import ABC, abstractmethod
import os
from typing import Optional, Union
from PIL import Image
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_image, write_image


class ImageLoader(ABC):
    """
    Abstract base class for loading images.

    This class should be subclassed to provide specific implementations of
    the `load_image` method.
    """

    @abstractmethod
    def load_image(self, *args, **kwargs) -> Image.Image:
        """
        Load an image.

        This method should be implemented by subclasses to provide the logic for
        loading an image.

        Returns:
            The loaded image.
        """
        raise NotImplementedError()


class CacheImageLoader(ImageLoader):
    """
    Concrete implementation of `ImageLoader` that supports caching.

    This class attempts to load the image from a cache first. If the image
    is not found in the cache, it loads the image from the specified location,
    caches it, and then returns it.

    Attributes:
        cache_location: The location for the cache. If not provided, it defaults to the
                        environment variable `IMAGE_CACHE_PATH` or `./image_cache`.
    """

    def __init__(
        self, cache_location: Optional[Union[dict, LocationConfig]] = None
    ) -> None:
        """
        Initialize the CacheImageLoader.

        Args:
            cache_location: The location for the cache. If not provided, it defaults to the
                            environment variable `IMAGE_CACHE_PATH` or `./image_cache`.
        """

        self.cache_location = cache_location or {
            "uri": os.getenv("IMAGE_CACHE_PATH", "./image_cache")
        }

    def load_image(
        self,
        *args,
        file_name: str,
        image_location: Union[dict, LocationConfig],
        target_size: Optional[ImageSize] = None,
        **kwargs
    ) -> Image.Image:
        """
        Load an image with caching.

        Args:
            file_name: The name of the image file.
            image_location: The location of the image to be loaded.
            target_size: The target size to resize the image to. If None, the image is not resized.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The loaded image.
        """

        with open_location(self.cache_location) as (
            cache_file_system,
            cache_root_location,
        ):
            cache_file_path = join_fs_path(
                cache_file_system, cache_root_location, file_name
            )
            if cache_file_system.exists(cache_file_path):
                cached_image = read_image(
                    filepath=cache_file_path, file_system=cache_file_system
                )
                if target_size is not None:
                    cached_image = cached_image.resize(target_size.to_pil_size())
                return cached_image

            with open_location(image_location) as (file_system, root_location):
                filepath = join_fs_path(file_system, root_location, file_name)
                image = read_image(filepath=filepath, file_system=file_system)
                write_image(
                    image=image,
                    filepath=cache_file_path,
                    file_system=cache_file_system,
                )
                if target_size is not None:
                    image = image.resize(target_size.to_pil_size())

                return image
