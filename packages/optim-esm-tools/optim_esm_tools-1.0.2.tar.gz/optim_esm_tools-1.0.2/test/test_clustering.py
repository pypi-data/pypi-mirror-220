import xarray as xr
import numpy as np
import optim_esm_tools._test_utils
import optim_esm_tools.analyze.clustering as clustering


def test_clustering_empty():
    ds = optim_esm_tools._test_utils.minimal_xr_ds().copy()
    ds['var'] = (ds['var'].dims, np.zeros_like(ds['var']))
    ds = ds.isel(time=0)
    assert np.all(np.shape(ds['var']) > np.array([2, 2]))

    clusters, masks = clustering.build_cluster_mask(
        ds['var'] > 0,
        ds['lat'],
        ds['lon'],
    )
    assert len(clusters) == len(masks) == 0


def test_clustering_mesh():
    return test_clustering_double_blob(use_mesh=True)


def test_clustering_double_blob(npoints=100, res_x=3, res_y=3, use_mesh=False):
    ds = optim_esm_tools._test_utils.minimal_xr_ds().copy()
    ds = ds.isel(time=0)

    arr = np.zeros_like(ds['var'])
    len_lat, len_lon = arr.shape[0:]
    y0, x0, y1, x1 = len_lat // 4, len_lon // 4, len_lat // 2, len_lon - len_lon // 4

    for x, y in [x0, y0], [x1, y1]:
        for x_i, y_i in zip(
            np.clip(np.random.normal(x, res_x, npoints).astype(int), 0, len_lat),
            np.clip(np.random.normal(y, res_y, npoints).astype(int), 0, len_lon),
        ):
            arr[y_i][x_i] += 1

    assert np.sum(arr) == 2 * npoints
    ds['var'] = (ds['var'].dims, arr)

    assert np.all(np.shape(ds['var']) > np.array([2, 2]))
    lat, lon = np.meshgrid(ds['lat'], ds['lon'])
    if use_mesh:
        lat, lon = np.meshgrid(ds['lat'], ds['lon'])
        clusters, masks = clustering.build_cluster_mask(
            ds['var'] > 1,
            lat.T,
            lon.T,
            max_distance_km=1000,
            min_samples=2,
        )
    else:
        clusters, masks = clustering.build_cluster_mask(
            ds['var'] > 1,
            ds['lat'].values,
            ds['lon'].values,
            max_distance_km=1000,
            min_samples=2,
        )
    assert len(clusters) == len(masks)
    assert len(clusters) == 2


def test_geopy_alternative():
    xs, ys = np.random.rand(1, 4).reshape(2, 2)
    xs *= 360
    ys = ys * 180 - 90
    # LAT:LON!
    coords = np.array([ys, xs]).T
    flat_coord = coords.flatten()
    print(coords, flat_coord)
    assert np.isclose(
        clustering._distance_bf_coord(*flat_coord),
        clustering._distance(coords),
        rtol=0.1,
    )
