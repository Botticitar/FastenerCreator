class PhysicalValidator:
    @staticmethod
    def check_screw_integrity(screw):
        if screw.l > screw.d * 10:
            raise ValueError("Screw is too long and thin; it will bend!")
        return True

    @staticmethod
    def check_washer_integrity(washer):
        if washer.d_i >= washer.d_o:
            raise ValueError("Inner diameter must be smaller than outer.")
        return True