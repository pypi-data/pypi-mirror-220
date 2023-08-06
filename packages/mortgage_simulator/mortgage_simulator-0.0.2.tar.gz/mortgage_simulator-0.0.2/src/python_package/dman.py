import numpy as np
import holoviews as hv
import panel as pn

# hv.extension('matplotlib')


xvals = np.linspace(-4, 0, 202)
yvals = np.linspace(4, 0, 202)
xs, ys = np.meshgrid(xvals, yvals)


def waves_image(alpha, beta):
    return hv.Image(np.sin(((ys / alpha) ** alpha + beta) * xs))


main = pn.Row()


# dmap = hv.DynamicMap(waves_image, kdims=["alpha", "beta"])

# dmap = dmap.redim.range(alpha=(1, 5.0), beta=(1, 6.0))


def shapes(N, radius=0.5):  # Positional keyword arguments are fine
    paths = [
        hv.Path(
            [
                [
                    (radius * np.sin(a), radius * np.cos(a))
                    for a in np.linspace(-np.pi, np.pi, n + 2)
                ]
            ],
            extents=(-1, -1, 1, 1),
        )
        for n in range(N, N + 3)
    ]
    return hv.Overlay(paths)


holomap = hv.HoloMap(
    {(N, r): shapes(N, r) for N in [3, 4, 5] for r in [0.5, 0.75]},
    kdims=["N", "radius"],
)
dmap = hv.DynamicMap(shapes, kdims=["N", "radius"])
# holomap + dmap


def spiral_equation(f, ph, ph2):
    r = np.arange(0, 1, 0.005)
    xs, ys = (
        r * fn(f * np.pi * np.sin(r + ph) + ph2) for fn in (np.cos, np.sin)
    )
    return hv.Path((xs, ys))


spiral_dmap = hv.DynamicMap(spiral_equation, kdims=["f", "ph", "ph2"])
spiral_dmap = spiral_dmap.redim.values(
    f=np.linspace(1, 10, 10),
    ph=np.linspace(0, np.pi, 10),
    ph2=np.linspace(0, np.pi, 4),
)


# main.append(hv.HoloMap(dmap[{2, 3}, {0.5, 1}]))

# main.append(spiral_dmap)

main.append(spiral_dmap.grid(["f", "ph"]))

# main.append(waves_image(1, 0))

# main.append(holomap + dmap)

main.show()
