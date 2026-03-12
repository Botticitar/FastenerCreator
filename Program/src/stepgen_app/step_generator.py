import cadquery as cq
import pandas as pd
import tempfile
from pathlib import Path

class StepGenerator:            
    @staticmethod
    def washer (data: RequestWasher) -> str:
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
    def screw (data: RequestScrew) -> str:
        headsizes ={'thread':  [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                    'head_height': [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                    'head_diameter': [5.5, 7, 8.5, 10, 13, 16, 18, 21, 24, 30, 36]} 
        #data from ISO 4762, these are MAX values possible, ideally this would come in through the .json 
        #and would be validated in validator, but I wanna keep the .json structure as is in the challenge file    
        headf=pd.DataFrame(headsizes)

        d_head = headf.loc[headf['thread'] == data.d, 'head_diameter'].item()
        l_head = headf.loc[headf['thread'] == data.d, 'head_height'].item()

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
