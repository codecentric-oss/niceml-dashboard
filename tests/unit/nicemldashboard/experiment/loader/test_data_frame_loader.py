from niceml.utilities.fsspec.locationutils import join_location_w_path, LocationConfig

from nicemldashboard.loader.dataframeloader import CacheDataFrameLoader


def test_load_data_frame_from_cache(
    data_frame_loader: CacheDataFrameLoader,
    cached_data_frame_filename: str,
    experiment_location: LocationConfig,
):
    loaded_data_frame = data_frame_loader.load_data_frame(
        file_path=cached_data_frame_filename,
        data_frame_location=join_location_w_path(experiment_location, "data_frames"),
    )
    assert len(loaded_data_frame) == 2
    assert all(loaded_data_frame["test_colum_b"] == "test_cache")


def test_load_data_frame(
    data_frame_loader: CacheDataFrameLoader,
    data_frame_filename: str,
    experiment_location: LocationConfig,
):
    loaded_data_frame = data_frame_loader.load_data_frame(
        file_path=data_frame_filename,
        data_frame_location=join_location_w_path(experiment_location, "data_frames"),
    )
    assert len(loaded_data_frame) == 2
    assert all(loaded_data_frame["test_colum_b"] == "test")
