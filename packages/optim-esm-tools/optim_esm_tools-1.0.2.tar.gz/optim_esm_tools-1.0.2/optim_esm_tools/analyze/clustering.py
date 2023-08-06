import numpy as np
from optim_esm_tools.utils import tqdm, timed
from optim_esm_tools.config import get_logger
import typing as ty
from warnings import warn
import numba
from math import sin, cos, sqrt, atan2, radians
import xarray as xr


@timed()
def build_clusters(
    coordinates_deg: np.ndarray,
    weights: ty.Optional[np.ndarray] = None,
    max_distance_km: ty.Union[float, int] = 750,
    only_core: bool = True,
    min_samples: int = 10,
    cluster_opts: ty.Optional[dict] = None,
) -> ty.List[np.ndarray]:
    """Build clusters based on a list of coordinates, use halfsine metric for spherical spatiol data

    Args:
        coordinates_deg (np.ndarray): set of xy coordinates in degrees
        weights (ty.Optional[np.ndarray], optional): weights (in the range [0,1]) corresponding to each coordinate
        max_distance_km (ty.Union[float, int], optional): max distance to other points to consider part of
            cluster (see DBSCAN(eps=<..>)). Defaults to 750.
        only_core (bool, optional): Use only core samples. Defaults to True.
        min_samples (int): Minimum number of samples in cluster. Defaults to 20.
        cluster_opts (ty.Optional[dict], optional): Additional options passed to sklearn.cluster.DBSCAN. Defaults to None.

    Returns:
        ty.List[np.ndarray]: list of clustered points (in radians)
    """
    cluster_opts = cluster_opts or dict()
    for class_label, v in dict(algorithm='ball_tree', metric='haversine').items():
        cluster_opts.setdefault(class_label, v)
    cluster_opts['min_samples'] = min_samples

    from sklearn.cluster import DBSCAN
    import numpy as np

    coordinates_rad = np.radians(coordinates_deg).T

    # TODO use a more up to date version:
    #  https://scikit-learn.org/stable/auto_examples/cluster/plot_hdbscan.html#sphx-glr-auto-examples-cluster-plot-hdbscan-py
    #  https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html#sklearn.cluster.HDBSCAN
    # Thanks https://stackoverflow.com/a/38731787/18280620!
    try:
        db_fit = DBSCAN(eps=max_distance_km / 6371.0, **cluster_opts).fit(
            X=coordinates_rad, sample_weight=weights
        )
    except ValueError as e:
        raise ValueError(
            f'With {coordinates_rad.shape} and {getattr(weights, "shape", None)} {coordinates_rad}, {weights}'
        ) from e

    labels = db_fit.labels_

    unique_labels = sorted(set(labels))
    is_core_sample = np.zeros_like(labels, dtype=bool)
    is_core_sample[db_fit.core_sample_indices_] = True

    return_masks = []

    for class_label in unique_labels:
        is_noise = class_label == -1
        if is_noise:
            continue

        is_class_member = labels == class_label
        coord_mask = is_class_member
        if only_core:
            coord_mask &= is_core_sample

        masked_points = coordinates_rad[coord_mask]
        return_masks.append(masked_points)

    return return_masks


@timed()
def build_cluster_mask(
    global_mask: np.ndarray,
    lat_coord: np.array,
    lon_coord: np.array,
    show_tqdm: bool = False,
    max_distance_km: ty.Union[str, float, int] = 'infer',
    **kw,
) -> ty.Tuple[ty.List[np.ndarray], ty.List[np.ndarray]]:
    """Build set of clusters and masks based on the global mask, basically a utility wrapper arround build_clusters'

    Args:
        global_mask (np.ndarray): full 2d mask of the data
        lon_coord (np.array): all longitude values
        lat_coord (np.array): all latitude values
        show_tqdm (bool, optional): use verboose progressbar. Defaults to False.
        max_distance_km (ty.Union[str, float, int]): find an appropriate distance
            threshold for build_clusters' max_distance_km argument. If nothing is
            provided, make a guess based on the distance between grid cells.
            Defaults to 'infer'.

    Returns:
        ty.List[ty.List[np.ndarray], ty.List[np.ndarray]]: Return two lists, containing the masks, and clusters respectively.
    """
    if max_distance_km == 'infer':
        max_distance_km = _infer_max_step_size(lat_coord, lon_coord)
    lat, lon = _check_input(
        global_mask,
        lat_coord,
        lon_coord,
    )
    xy_data = np.array([lat[global_mask], lon[global_mask]])

    if len(xy_data.T) <= 2:
        get_logger().info(f'No data from this mask {xy_data}!')
        return [], []

    masks, clusters = _build_cluster_with_kw(
        lat=lat,
        lon=lon,
        coordinates_deg=xy_data,
        show_tqdm=show_tqdm,
        max_distance_km=max_distance_km,
        **kw,
    )

    return masks, clusters


@timed()
def build_weighted_cluster(
    weights: np.ndarray,
    lat_coord: np.array,
    lon_coord: np.array,
    show_tqdm: bool = False,
    threshold: ty.Optional[float] = 0.99,
    max_distance_km: ty.Union[str, float, int] = 'infer',
    **kw,
) -> ty.Tuple[ty.List[np.ndarray], ty.List[np.ndarray]]:
    """Build set of clusters and masks based on the weights (which should be a grid)'

    Args:
        weights (np.ndarray): normalized score data (values in [0,1])
        lon_coord (np.array): all longitude values
        lat_coord (np.array): all latitude values
        max_distance_km (ty.Union[str, float, int]): find an appropriate distance
            threshold for build_clusters' max_distance_km argument. If nothing is
            provided, make a guess based on the distance between grid cells.
            Defaults to 'infer'.
        show_tqdm (bool, optional): use verboose progressbar. Defaults to False.
        threshold: float, min value of the passed weights. Defaults to 0.99.

    Returns:
        ty.List[ty.List[np.ndarray], ty.List[np.ndarray]]: Return two lists, containing the masks, and clusters respectively.
    """
    if max_distance_km == 'infer':
        max_distance_km = _infer_max_step_size(lat_coord, lon_coord)

    lat, lon = _check_input(weights, lat_coord, lon_coord)
    xy_data = np.array([lat.flatten(), lon.flatten()])

    flat_weights = weights.flatten()
    mask = flat_weights > threshold
    masks, clusters = _build_cluster_with_kw(
        lat=lat,
        lon=lon,
        coordinates_deg=xy_data[:, mask],
        weights=flat_weights[mask],
        show_tqdm=show_tqdm,
        max_distance_km=max_distance_km,
        **kw,
    )

    return masks, clusters


def _check_input(data, lat_coord, lon_coord):
    """Check for consistancy and if we need to convert the lon/lat coordinates to a meshgrid"""
    if len(lon_coord.shape) <= 1:
        lon, lat = np.meshgrid(lon_coord, lat_coord)
    else:
        # In an older version, this would have been the default.
        lat, lon = lat_coord, lon_coord

    if data.shape != lon.shape or data.shape != lat.shape:
        message = f'Wrong input {data.shape} != {lon.shape, lat.shape}'
        raise ValueError(message)
    return lat, lon


def _build_cluster_with_kw(lat, lon, show_tqdm=False, **cluster_kw):
    """Overlapping logic between functions to get the masks and clusters"""
    masks = []
    clusters = [np.rad2deg(cluster) for cluster in build_clusters(**cluster_kw)]
    if lat.shape != lon.shape:
        raise ValueError(f'Got inconsistent input {lat.shape} != {lon.shape}')
    for cluster in clusters:
        mask = np.zeros(lat.shape, np.bool_)
        for coord_lat, coord_lon in tqdm(
            cluster, desc='fill_mask', disable=not show_tqdm
        ):
            # This is a bit blunt, but it's fast enough to regain the indexes such that we can build a 2d masked array.
            mask_x = np.isclose(lon, coord_lon)
            mask_y = np.isclose(lat, coord_lat)
            mask |= mask_x & mask_y
        masks.append(mask)
    return masks, clusters


def _infer_max_step_size(lat, lon, off_by_factor=1.1):
    if len(lat.shape) == 1:
        return np.max(calculate_distance_map(lat, lon)) * off_by_factor
    lat = lat[lat > 0]
    coords = [
        [[lat[0], lon[0]], [lat[0], lon[1]]],
        [[lat[0], lon[0]], [lat[1], lon[0]]],
    ]
    # Return 2x the distance between grid cells
    return 2 * max(_distance(c) for c in coords)


def calculate_distance_map(lat, lon):
    """For each point in a spanned lat lon grid, calculate the distance to the neighbouring points"""
    if isinstance(lat, xr.DataArray):
        lat = lat.values
        lon = lon.values
    return _calculate_distance_map(lat, lon)


@numba.njit
def _calculate_distance_map(lat, lon):
    n_lat = len(lat)
    n_lon = len(lon)
    distances = np.zeros((n_lat, n_lon))

    shift_by_index = np.array(
        [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (1, -1), (-1, 1)]
    )
    neighbourgs = np.zeros(len(shift_by_index), dtype=np.float64)
    for lon_i in range(n_lon):
        for lat_i in range(n_lat):
            neighbourgs[:] = 0
            current = (lat[lat_i], lon[lon_i])
            for i, (x, y) in enumerate(shift_by_index):
                alt_lon = np.mod(lon_i + x, n_lon)
                alt_lat = lat_i + y
                if alt_lat == n_lat or alt_lat < 0:
                    continue
                alt_coord = (lat[alt_lat], lon[alt_lon])
                if alt_coord == current:
                    continue
                neighbourgs[i] = _distance_bf_coord(*current, *alt_coord)
            distances[lat_i][lon_i] = np.max(neighbourgs)
    return distances


def _distance(coords, force_math=False):
    """Wrapper for if geopy is not installed"""
    if not force_math:
        try:
            from geopy.distance import geodesic

            return geodesic(*coords).km
        except (ImportError, ModuleNotFoundError):
            pass
    if len(coords) != 4:
        coords = [c for cc in coords for c in cc]
    return _distance_bf_coord(*coords)


@numba.njit
def _distance_bf_coord(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    return _distance_bf(lat1, lon1, lat2, lon2)


@numba.njit
def _distance_bf(lat1, lon1, lat2, lon2):
    # https://stackoverflow.com/a/19412565/18280620

    # Approximate radius of earth in km
    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
