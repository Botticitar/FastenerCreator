import cadquery as cq
import pandas as pd
from ocp_vscode import show 

def washer (d_o, d_i, t):
    return(
        cq.Workplane("XY")
        .circle(d_o/2)
        .circle(d_i/2)
        .extrude(t)
    )

def bolt (l, d): 
        
        headsizes ={'thread':  [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                    'head_height': [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                    'head_diameter': [5.5, 7, 8.5, 10, 13, 16, 18, 21, 24, 30, 36]} 
        #data from ISO 4762, these are MAX values possible, ideally this would come in through the .json 
        #and would be validated in validator, but I wanna keep the .json structure as is in the challenge file
        
        headf=pd.DataFrame(headsizes)

        d_head = headf.loc[headf['thread'] == d, 'head_diameter'].item()
        l_head = headf.loc[headf['thread'] == d, 'head_height'].item()

        bolt=(cq.Workplane("XY")
        .circle(d/2)
        .extrude(l))

        new_plane=bolt.faces(">Z").workplane()

        bolt=new_plane.circle(d_head/2).extrude(l_head)

        return(bolt)

        #if head == 'hex': #do we neeed different heads?                 -if head shape is added
        #    bolt=new_plane.polygon(6, d_head).extrude(l_head)
        #else:
        #    bolt=new_plane.circle(d_head).extrude(l_head)
        ##return(bolt)

washer_model=washer(4, 3, 2)
cq.exporters.export(washer_model, 'Washer.step')

bolt_model=bolt(20, 3)
cq.exporters.export(bolt_model, 'Screw.step')
