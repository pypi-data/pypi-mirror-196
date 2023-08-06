#!/usr/bin/python
import os, shutil
import os
from jupyter_client.kernelspec import KernelSpecManager
json ="""{"argv":["python","-m","jansevakernel", "-f", "{connection_file}"],
 "display_name":"eva"
}"""

svg = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   id="Hexels SVG Export"
   version="1.1"
   viewBox="0 0 300 300"
   xml:space="preserve"
   sodipodi:docname="logo-svg.svg"
   width="300"
   height="300"
   inkscape:version="1.2.2 (732a01da63, 2022-12-09)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"><defs
   id="defs25" /><sodipodi:namedview
   id="namedview23"
   pagecolor="#505050"
   bordercolor="#ffffff"
   borderopacity="1"
   inkscape:showpageshadow="0"
   inkscape:pageopacity="0"
   inkscape:pagecheckerboard="1"
   inkscape:deskcolor="#505050"
   showgrid="false"
   inkscape:zoom="1.7766058"
   inkscape:cx="113.41852"
   inkscape:cy="127.20886"
   inkscape:window-width="1920"
   inkscape:window-height="1009"
   inkscape:window-x="-8"
   inkscape:window-y="-8"
   inkscape:window-maximized="1"
   inkscape:current-layer="Hexels SVG Export" />
<g
   id="Root"
   transform="matrix(0.69801785,0,0,0.69801785,-478.21607,-226.92964)">
<g
   id="Layer 1">

<path
   d="m 780,330 -60,30 180,90 180,-90 -60,-30 -120,60 z"
   style="fill:#b6a995;fill-opacity:1"
   id="path4" />
<path
   d="m 720,360 v 60 l 120,60 v 60 L 720,480 v 60 l 120,60 v 60 L 720,600 v 60 l 180,90 V 450 Z"
   style="fill:#f7f3ee;fill-opacity:1"
   id="path6" />
<path
   d="m 1080,360 -180,90 v 300 l 60,-30 V 600 l 60,-30 v 120 l 60,-30 z m -120,120 60,-30 v 60 l -60,30 z"
   style="fill:#625b50;fill-opacity:1"
   id="path8" />
<path
   d="m 780,450 -60,30 120,60 v -60 z"
   style="fill:#b6a995;fill-opacity:1"
   id="path10" />
<path
   d="m 1020,450 -60,30 60,30 z"
   style="fill:#f7f3ee;fill-opacity:1"
   id="path12" />
<path
   d="m 960,480 v 60 l 60,-30 z"
   style="fill:#b6a995;fill-opacity:1"
   id="path14" />
<path
   d="m 780,570 -60,30 120,60 v -60 z"
   style="fill:#b6a995;fill-opacity:1"
   id="path16" />
<path
   d="m 1020,570 -60,30 v 60 l 60,30 z"
   style="fill:#f7f3ee;fill-opacity:1"
   id="path18" />
</g>
</g></svg>
"""

def install_kernelspec():
    kerneldir = "/tmp/jansevakernel/"
    print('Creating tmp files...', end="")
    os.mkdir(kerneldir)

    with open(kerneldir + "kernel.json", "w") as f:
        f.write(json)

    with open(kerneldir + "logo-svg.svg", "w") as f:
        f.write(svg)
        
    print(' Done!')
    print('Installing Jupyter kernel...', end="")
    
    ksm = KernelSpecManager()
    ksm.install_kernel_spec(kerneldir, 'jansevakernel', user=os.getenv('USER'))
    
    print(' Done!')
    print('Cleaning up tmp files...', end="")
    
    shutil.rmtree(kerneldir)
    
    print(' Done!')
    print('For uninstall use: jupyter kernelspec uninstall jansevakernel')