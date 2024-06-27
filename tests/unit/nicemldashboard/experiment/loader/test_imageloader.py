import numpy as np
import pytest
from niceml.utilities.fsspec.locationutils import LocationConfig, join_location_w_path
from niceml.utilities.imagesize import ImageSize

from nicemldashboard.loader.imageloader import CacheImageLoader


def test_load_image_from_cache(
    image_loader: CacheImageLoader,
    cached_image_filename: str,
    experiment_location: LocationConfig,
):
    loaded_image = image_loader.load_image(
        file_name=cached_image_filename,
        image_location=join_location_w_path(experiment_location, "images"),
    )
    assert (np.asarray(loaded_image) == 1).all()
    assert loaded_image.size == (256, 256)


def test_load_image(
    image_loader: CacheImageLoader,
    image_filename: str,
    experiment_location: LocationConfig,
):
    loaded_image = image_loader.load_image(
        file_name=image_filename,
        image_location=join_location_w_path(experiment_location, "images"),
    )
    assert (np.asarray(loaded_image) == 0).all()
    assert loaded_image.size == (256, 256)


@pytest.mark.parametrize(
    "target_size",
    [
        ImageSize(width=1024, height=1024),
        ImageSize(width=128, height=128),
        ImageSize(width=256, height=256),
    ],
)
def test_load_image_resize(
    target_size: ImageSize,
    image_loader: CacheImageLoader,
    image_filename: str,
    experiment_location: LocationConfig,
):
    loaded_image = image_loader.load_image(
        file_name=image_filename,
        image_location=join_location_w_path(experiment_location, "images"),
        target_size=target_size,
    )

    assert loaded_image.size == target_size.to_pil_size()
