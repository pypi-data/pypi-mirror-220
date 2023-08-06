importScripts("https://cdn.jsdelivr.net/pyodide/v0.23.0/full/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide!");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded!");
  await self.pyodide.loadPackage("micropip");
  const env_spec = ['https://cdn.holoviz.org/panel/1.2.0/dist/wheels/bokeh-3.2.0-py3-none-any.whl', 'https://cdn.holoviz.org/panel/1.2.0/dist/wheels/panel-1.2.0-py3-none-any.whl', 'pyodide-http==0.2.1', 'holoviews', 'numpy']
  for (const pkg of env_spec) {
    let pkg_name;
    if (pkg.endsWith('.whl')) {
      pkg_name = pkg.split('/').slice(-1)[0].split('-')[0]
    } else {
      pkg_name = pkg
    }
    self.postMessage({type: 'status', msg: `Installing ${pkg_name}`})
    try {
      await self.pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${pkg}');
      `);
    } catch(e) {
      console.log(e)
      self.postMessage({
	type: 'status',
	msg: `Error while installing ${pkg_name}`
      });
    }
  }
  console.log("Packages loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  const code = `
  
import asyncio

from panel.io.pyodide import init_doc, write_doc

init_doc()

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


await write_doc()
  `

  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(code)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.globals.set('patch', msg.patch)
    self.pyodide.runPythonAsync(`
    state.curdoc.apply_json_patch(patch.to_py(), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.globals.set('location', msg.location)
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads(location)
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()