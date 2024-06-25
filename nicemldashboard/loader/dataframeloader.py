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
    @abstractmethod
    def load_data_frame(self, *args, **kwargs) -> pd.DataFrame:
        """Loading of Data Frames"""


class CacheDataFrameLoader(DataFrameLoader):
    def __init__(
        self, cache_location: Optional[Union[dict, LocationConfig]] = None
    ) -> None:
        super().__init__()
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
