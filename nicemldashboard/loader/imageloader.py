from abc import ABC, abstractmethod
import os
from typing import Optional, Union
from PIL import Image
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location, join_fs_path
from niceml.utilities.ioutils import read_image,write_image

class ImageLoader(ABC):    

    @abstractmethod
    def load_image(self,*args,file_path:str,**kwargs) -> Image.Image:
        '''Loading of Images'''
        


class CacheImageLoader(ImageLoader):
    
    def __init__(self,cache_location:Optional[dict] = None) -> None:
        super().__init__()
        self.cache_location=cache_location or {"uri":os.getenv("IMAGE_CACHE_PATH","./image_cache")}
    
    def load_image(self,file_path:str,image_location:Union[dict,LocationConfig],target_size: Optional[ImageSize] = None) -> Image.Image:
        with open_location(self.cache_location) as (cache_file_system,cache_root_location):
            cache_file_path = join_fs_path(cache_file_system,cache_root_location,file_path)
            if cache_file_system.exists(cache_file_path):
                cached_image = read_image(file_path=cache_file_path,file_system=cache_file_system)
                if  target_size is not None:
                    cached_image = cached_image.resize(target_size.to_pil_size())
                return cached_image

            with open_location(image_location) as (file_system,root_location): 
                file_path = join_fs_path(file_system,root_location,file_path)
                image = read_image(file_path=file_path,file_system=file_system)
                write_image(image=image,file_path=cache_file_path,file_system=cache_file_system)
                if  target_size is not None:
                    image = image.resize(target_size.to_pil_size())

                return image
        
    