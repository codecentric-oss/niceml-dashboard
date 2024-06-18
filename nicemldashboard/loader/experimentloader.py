from abc import ABC, abstractmethod
from typing import List, Optional, Union
from nicemldashboard.experiment.experiment import Experiment
from nicemldashboard.experiment.type import ExperimentType
from nicemldashboard.loader.dataframeloader import DataFrameLoader
from nicemldashboard.loader.imageloader import ImageLoader
from niceml.utilities.ioutils import list_dir,read_yaml
from niceml.utilities.fsspec.locationutils import LocationConfig, open_location, join_fs_path
from niceml.experiments.expfilenames import ExperimentFilenames
from niceml.config.envconfig import EXP_NAME_KEY,SHORT_ID_KEY,DESCRIPTION_KEY,RUN_ID_KEY,EXP_TYPE_KEY
from PIL import Image
import pandas as pd

class ExperimentLoader(ABC):

    def __init__(self,image_loader:ImageLoader,data_frame_loader:DataFrameLoader,experiment_location:Union[dict,LocationConfig]) -> None:
        self.image_loader=image_loader
        self.data_frame_loader=data_frame_loader
        self.experiment_location=experiment_location
        
    @abstractmethod
    def load_experiments(self,data_set:Optional[str] = None) -> List[Experiment]:
        '''Loading of experiments'''
        
    def load_image(self,*args,file_path:str,**kwargs) -> Image.Image:
        '''Loading of Images'''    
        return self.image_loader.load_image(*args,file_path=file_path,**kwargs)
        
    def load_data_frame(self,*args,file_path:str,**kwargs) -> pd.DataFrame:
        '''Loading of Data Frames''' 
        return self.data_frame_loader.load_data_frame(*args,file_path=file_path,**kwargs)
    
class  FilesAndFolderLoader(ExperimentLoader):
    
    
    def load_experiments(self,data_set:Optional[str] = None) -> List[Experiment]:
        with open_location(self.experiment_location) as (file_system,root_location):
            experiments_paths = join_fs_path(file_system,root_location,data_set or "")
            experiment_folders = list_dir(path=experiments_paths, file_system=file_system)
            experiments: List[Experiment] = []
            for experexperiment_folder in experiment_folders:
                if file_system.isdir(join_fs_path(file_system,root_location,data_set or "",experexperiment_folder)):
                    experiment_info_path = join_fs_path(file_system,root_location,data_set or "",experexperiment_folder,ExperimentFilenames.EXP_INFO)
                    experiment_info = read_yaml(filepath=experiment_info_path,file_system=file_system)
                    experiments_git_versions_path=join_fs_path(file_system,root_location,data_set or "",experexperiment_folder,ExperimentFilenames.GIT_VERSIONS)
                    experiments_git_versions= read_yaml(filepath=experiments_git_versions_path,file_system=file_system)
                    experiment = Experiment(name = experiment_info[EXP_NAME_KEY],
                                            experiment_type = ExperimentType.from_prefix(prefix=experiment_info[EXP_TYPE_KEY]),
                                            short_id = experiment_info[SHORT_ID_KEY],
                                            description = experiment_info[DESCRIPTION_KEY],
                                            experiment_id = experiment_info[RUN_ID_KEY],
                                            git_version= experiments_git_versions,
                                            data_set = "test_data_set" # TODO : Dataset to experimentset yaml 
                                            )
                    experiments.append(experiment)
        return experiments