from pydantic import BaseModel, Field, model_validator
from stepgen_app.data_checks import PhysicalValidator

class ScrewRequest(BaseModel):
    d: float = Field(gt=0, alias="diameter")
    l: float = Field(gt=0, alias="length")
    
    @model_validator(mode='after')
    def validate_physics(self) -> 'ScrewRequest':
        PhysicalValidator.check_screw_integrity(self)
        return self
    
class WasherRequest(BaseModel):
    d_i: float = Field(gt=0, alias="inner_diameter")
    d_o: float = Field(gt=0, alias="outer_diameter")
    t: float = Field(gt=0, alias="thickness")

    @model_validator(mode='after')
    def validate_physics(self) -> 'WasherRequest':
        PhysicalValidator.check_washer_integrity(self)
        return self

    model_config = {
        "populate_by_name": True
    }