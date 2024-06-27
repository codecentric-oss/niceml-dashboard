"""
Module for loading and caching Pandas DataFrames using different file systems and locations.

This module provides an abstract base class `DataFrameLoader` for loading DataFrames 
and a concrete implementation `CacheDataFrameLoader` that supports caching the DataFrames 
to avoid redundant loading operations.
"""

from abc import ABC, abstractmethod
from typing import Optional, Union
import pandas as pd
import os
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    open_location,
    join_fs_path,
)
from niceml.utilities.ioutils import read_parquet, write_parquet


class DataFrameLoader(ABC):
    """
    Abstract base class for loading Pandas DataFrames.

    This class should be subclassed to provide specific implementations of
    the `load_data_frame` method.
    """

    @abstractmethod
    def load_data_frame(self, *args, **kwargs) -> pd.DataFrame:
        """
        Load a Pandas DataFrame.

        This method should be implemented by subclasses to provide the logic for
        loading a DataFrame.

        Returns:
            The loaded DataFrame.
        """

        raise NotImplementedError()


class CacheDataFrameLoader(DataFrameLoader):
    """
    Concrete implementation of `DataFrameLoader` that supports caching.

    This class attempts to load the DataFrame from a cache first. If the DataFrame
    is not found in the cache, it loads the DataFrame from the specified location,
    caches it, and then returns it.

    Attributes:
        cache_location: The location configuration for the cache. If not provided,
                        it defaults to the environment variable `DATAFRAME_CACHE_PATH`
                        or `./dataframe_cache`.

    """

    def __init__(
        self, cache_location: Optional[Union[dict, LocationConfig]] = None
    ) -> None:
        """
        Initialize the CacheDataFrameLoader.

        Args:
            cache_location: The location of the cache. If not provided,
                            it defaults to the environment variable `DATAFRAME_CACHE_PATH`
                            or `./dataframe_cache`.
        """

        self.cache_location = cache_location or {
            "uri": os.getenv("DATAFRAME_CACHE_PATH", "./dataframe_cache")
        }

    def load_data_frame(
        self,
        data_frame_location: Union[dict, LocationConfig],
        file_path: str,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Load a Pandas DataFrame with caching.

        Args:
            data_frame_location: The location of the DataFrame to be loaded.
            file_path: The file path of the DataFrame within the specified location.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            The loaded DataFrame.
        """

        with open_location(self.cache_location) as (
            cache_file_system,
            cache_root_location,
        ):
            cache_file_path = join_fs_path(
                cache_file_system, cache_root_location, file_path
            )
            if cache_file_system.exists(cache_file_path):
                cached_data_frame = read_parquet(
                    filepath=cache_file_path, file_system=cache_file_system
                )
                return cached_data_frame

            with open_location(data_frame_location) as (file_system, root_location):
                file_path = join_fs_path(file_system, root_location, file_path)
                data_frame = read_parquet(filepath=file_path, file_system=file_system)
                write_parquet(
                    data_frame=data_frame,
                    file_path=cache_file_path,
                    file_system=cache_file_system,
                )

                return data_frame
