import cadquery as cq
from ocp_vscode import show 

def washer (d_o, d_i, t):
    return(
        cq.Workplane("XY")
        .circle(d_o/2)
        .circle(d_i/2)
        .extrude(t)
    )

def bolt (l, d, l_head, d_head, head): 
        bolt=(cq.Workplane("XY")
        .circle(d/2)
        .extrude(l))

        new_plane=bolt.faces(">Z").workplane()

        if head == 'hex': #do we neeed different heads?
            bolt=new_plane.polygon(6, d_head).extrude(l_head)
        else:
            bolt=new_plane.circle(d_head).extrude(l_head)

        return(bolt)

washer_model=washer(4, 3, 2)
cq.exporters.export(washer_model, 'Washer.step')

bolt_model=bolt(20,3,3,5, 'hex')
cq.exporters.export(bolt_model, 'Bolt.step')
