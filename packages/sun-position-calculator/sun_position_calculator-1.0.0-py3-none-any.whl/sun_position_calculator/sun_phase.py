class SunPhase:
    def __init__(self, angle_deg, is_rise):
        self.angle_deg = angle_deg
        self.is_rise = is_rise

    @classmethod
    def sunrise(cls):
        return cls(-0.833, True)

    @classmethod
    def sunset(cls):
        return cls(-0.833, False)

    @classmethod
    def sunrise_end(cls):
        return cls(-0.5, True)

    @classmethod
    def sunset_start(cls):
        return cls(-0.5, False)

    @classmethod
    def dawn(cls):
        return cls(-6.0, True)

    @classmethod
    def dusk(cls):
        return cls(-6.0, False)

    @classmethod
    def nautical_dawn(cls):
        return cls(-12.0, True)

    @classmethod
    def nautical_dusk(cls):
        return cls(-12.0, False)

    @classmethod
    def night_end(cls):
        return cls(-18.0, True)

    @classmethod
    def night(cls):
        return cls(-18.0, False)

    @classmethod
    def golden_hour_end(cls):
        return cls(6.0, True)

    @classmethod
    def golden_hour(cls):
        return cls(6.0, False)

    @classmethod
    def civil_dawn(cls):
        return cls(-6.0, True)

    @classmethod
    def civil_dusk(cls):
        return cls(-6.0, False)

    @classmethod
    def astronomical_dawn(cls):
        return cls(-18.0, True)

    @classmethod
    def astronomical_dusk(cls):
        return cls(-18.0, False)

    @classmethod
    def morning_golden_hour(cls):
        return cls(4.0, True)

    @classmethod
    def evening_golden_hour(cls):
        return cls(4.0, False)

    @classmethod
    def blue_hour_morning(cls):
        return cls(-4.0, True)

    @classmethod
    def blue_hour_evening(cls):
        return cls(-4.0, False)

    def zenith(cls):
        return cls(0.0, True)

    def nadir(cls):
        return cls(180.0, False)

    @classmethod
    def afternoon_golden_hour(cls):
        return cls(4.0, False)

    @classmethod
    def custom(cls, angle_deg, is_rise):
        return cls(angle_deg, is_rise)