import cadquery as cq
import pandas as pd
import tempfile
from pathlib import Path
from stepgen_app.standards import Standards

class StepGenerator:            
    @staticmethod
    def washer (data) -> str:
        washer = (
            cq.Workplane("XY")
            .circle(data.d_o/2)
            .circle(data.d_i/2)
            .extrude(data.t)
        )
    
        path=Path(tempfile.gettempdir()) / 'Washer.step'
        cq.exporters.export(washer, str(path))
        return str(path)

    @staticmethod
    def screw (data) -> str:

        d_head = Standards.standards.loc[Standards.standards['diameter'] == data.d, 'head_diameter'].item()
        l_head = Standards.standards.loc[Standards.standards['diameter'] == data.d, 'head_height'].item()

        screw=(cq.Workplane("XY")
            .circle(data.d/2)
            .extrude(data.l))

        new_plane=screw.faces(">Z").workplane()

        screw=new_plane.circle(d_head/2).extrude(l_head)


        #if head == 'hex': #do we neeed different heads?                 -if head shape is added
        #    bolt=new_plane.polygon(6, d_head).extrude(l_head)
        #else:
        #    bolt=new_plane.circle(d_head).extrude(l_head)
        ##return(bolt)
            
        path=Path(tempfile.gettempdir()) / 'Screw.step'
        cq.exporters.export(screw, str(path))
        return str(path)
