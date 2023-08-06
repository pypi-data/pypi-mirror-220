import numpy as np
import holoviews as hv
import panel as pn

from holoviews import opts

hv.extension("bokeh")

opts.defaults(opts.Curve(line_width=1))


def fm_modulation(
    f_carrier=220, f_mod=220, mod_index=1, length=0.1, sampleRate=2000
):
    sampleInc = 1.0 / sampleRate
    x = np.arange(0, length, sampleInc)
    y = np.sin(
        2 * np.pi * f_carrier * x + mod_index * np.sin(2 * np.pi * f_mod * x)
    )
    return hv.Curve((x, y), "Time", "Amplitude")


f_carrier = np.linspace(20, 60, 3)
f_mod = np.linspace(20, 100, 5)

curve_dict = {
    (fc, fm): fm_modulation(fc, fm) for fc in f_carrier for fm in f_mod
}

kdims = [
    hv.Dimension(("f_carrier", "Carrier frequency"), default=40),
    hv.Dimension(("f_mod", "Modulation frequency"), default=60),
]
holomap = hv.HoloMap(curve_dict, kdims=kdims)
holomap.opts(opts.Curve(width=600))

layout = hv.Overlay()

layout += holomap.overlay("f_carrier").grid()
layout += holomap.overlay("f_mod").grid()

# layout += layout.Time

print(holomap.kdims)

gv = hv.GridSpace(holomap)
# layout += gv

layout += hv.Table(gv.collapse())

# print()
# grid = hv.GridSpace(holomap)

# ndlayout = hv.NdLayout(grid[20, 20:81])

main = pn.Row(layout)

main.servable()
# main.show()
