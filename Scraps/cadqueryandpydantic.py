from pydantic import BaseModel, Field, model_validator
import cadquery as cq
import pandas as pd

class ScrewRequest(BaseModel):
    d: float = 5
    l: float = 60
    
    
class WasherRequest(BaseModel):
    d_i: float = 5
    d_o: float = 8
    t: float = 1

class GeoCreator:
    @staticmethod
    def washer (data: WasherRequest):
            return(
                cq.Workplane("XY")
                .circle(data.d_o/2)
                .circle(data.d_i/2)
                .extrude(data.t)
                )

    @staticmethod
    def bolt (data: ScrewRequest): 
            
            headsizes ={'thread':  [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                        'head_height': [3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24],
                        'head_diameter': [5.5, 7, 8.5, 10, 13, 16, 18, 21, 24, 30, 36]} 
            #data from ISO 4762, these are MAX values possible, ideally this would come in through the .json 
            #and would be validated in validator, but I wanna keep the .json structure as is in the challenge file
            
            headf=pd.DataFrame(headsizes)

            d_head = headf.loc[headf['thread'] == data.d, 'head_diameter'].item()
            l_head = headf.loc[headf['thread'] == data.d, 'head_height'].item()

            bolt=(cq.Workplane("XY")
            .circle(data.d/2)
            .extrude(data.l))

            new_plane=bolt.faces(">Z").workplane()

            bolt_fin=new_plane.circle(d_head/2).extrude(l_head)

            cq.exporters.export(bolt_fin, 'BoltWV.step')
            return 'BoltWV.step'

            #if head == 'hex': #do we neeed different heads?                 -if head shape is added
            #    bolt=new_plane.polygon(6, d_head).extrude(l_head)
            #else:
            #    bolt=new_plane.circle(d_head).extrude(l_head)
            ##return(bolt)

    #washer_model=washer(WasherRequest)
    #cq.exporters.export(washer_model, 'Washer.step')

    #bolt_model=bolt(ScrewRequest)
    #cq.exporters.export(bolt_model, 'Screw.step')
    # 1. Create the data objects (Pydantic will use your defaults: d=5, l=60)
my_screw_data = ScrewRequest() 
my_washer_data = WasherRequest()

# 2. Call the static methods using the Class name
# This will actually run the code and save the .step files
bolt_file = GeoCreator.bolt(my_screw_data)
washer_obj = GeoCreator.washer(my_washer_data)

# The washer function returns the CAD object, so we export it here
#cq.exporters.export(washer_obj, 'WasherWV.step')

#rint(f"Success! Files generated: {bolt_file} and WasherWV.step")