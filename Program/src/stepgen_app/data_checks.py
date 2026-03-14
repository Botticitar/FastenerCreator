from pydantic import field_validator
from stepgen_app.standards import Standards

class PhysicalValidator:
    @staticmethod
    def check_screw_diameter(screw):
        if screw.d not in Standards.standards['diameter'].values:
            raise ValueError("Non-standard screw diameter!")
        return True
    
    @staticmethod
    def check_screw_length(screw):
        l_min = Standards.standards.loc[Standards.standards['diameter'] == screw.d, 'shank_length_minimum'].item()
        l_max = Standards.standards.loc[Standards.standards['diameter'] == screw.d, 'shank_length_maximum'].item()
        if screw.l < l_min:
            raise ValueError("Length below minimum for standard!")
        elif screw.l > l_max:
            raise ValueError("Length exceeds maximum for standard!")
        return True

    @staticmethod
    def check_washer_integrity(washer):
        if washer.d_i >= washer.d_o:
            raise ValueError("Inner diameter must be smaller than outer!")
        return True
    
    @staticmethod
    def check_compatibility(screw, washer):
        if washer.d_i < screw.d:
            raise ValueError("Washer inner diameter is smaller than screw shank diameter!")
        return True

#This class can be expanded with many other different checks
#(ie. a d_i of washer must be smaller than the screw head's diameter) 