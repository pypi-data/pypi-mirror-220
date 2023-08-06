import math

class Position:
    def __init__(self, azimuth, altitude):
        self.azimuth = azimuth
        self.altitude = altitude

class SunPositionCalculator:
    def __init__(self):
        self.MILLISECONDS_PER_DAY = 1000 * 60 * 60 * 24
        self.J0 = 0.0009
        self.J1970 = 2440588
        self.J2000 = 2451545
        self.TO_RAD = math.pi / 180.0
        self.OBLIQUITY_OF_EARTH = 23.4397 * self.TO_RAD
        self.PERIHELION_OF_EARTH = 102.9372 * self.TO_RAD

    def to_julian(self, unixtime_in_ms):
        return unixtime_in_ms / self.MILLISECONDS_PER_DAY - 0.5 + self.J1970

    def from_julian(self, j):
        return round((j + 0.5 - self.J1970) * self.MILLISECONDS_PER_DAY)

    def to_days(self, unixtime_in_ms):
        return self.to_julian(unixtime_in_ms) - self.J2000

    def right_ascension(self, l, b):
        return math.atan2(math.sin(l) * math.cos(self.OBLIQUITY_OF_EARTH) - math.tan(b) * math.sin(self.OBLIQUITY_OF_EARTH), math.cos(l))

    def declination(self, l, b):
        return math.asin(math.sin(b) * math.cos(self.OBLIQUITY_OF_EARTH) + math.cos(b) * math.sin(self.OBLIQUITY_OF_EARTH) * math.sin(l))

    def azimuth(self, h, phi, dec):
        return math.atan2(math.sin(h), math.cos(h) * math.sin(phi) - math.tan(dec) * math.cos(phi)) + math.pi

    def altitude(self, h, phi, dec):
        return math.asin(math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(h))

    def sidereal_time(self, d, lw):
        return math.radians(280.16 + 360.9856235 * d) - lw

    def solar_mean_anomaly(self, d):
        return math.radians(357.5291 + 0.98560028 * d)

    def equation_of_center(self, m):
        return math.radians(1.9148 * math.sin(1.0 * m) + 0.02 * math.sin(2.0 * m) + 0.0003 * math.sin(3.0 * m))

    def ecliptic_longitude(self, m):
        return m + self.equation_of_center(m) + self.PERIHELION_OF_EARTH + math.pi

    def pos(self, unixtime_in_ms, lat, lon):
        lw = -math.radians(lon)
        phi = math.radians(lat)
        d = self.to_days(unixtime_in_ms)
        m = self.solar_mean_anomaly(d)
        l = self.ecliptic_longitude(m)
        dec = self.declination(l, 0.0)
        ra = self.right_ascension(l, 0.0)
        h = self.sidereal_time(d, lw) - ra

        return Position(self.azimuth(h, phi, dec), self.altitude(h, phi, dec))

    def julian_cycle(self, d, lw):
        return round(d - self.J0 - lw / (2.0 * math.pi))

    def approx_transit(self, ht, lw, n):
        return self.J0 + (ht + lw) / (2.0 * math.pi) + n

    def solar_transit_j(self, ds, m, l):
        return self.J2000 + ds + 0.0053 * math.sin(m) - 0.0069 * math.sin(2.0 * l)

    def hour_angle(self, h, phi, d):
        return math.acos((math.sin(h) - math.sin(phi) * math.sin(d)) / (math.cos(phi) * math.cos(d)))

    def observer_angle(self, height):
        return -2.076 * math.sqrt(height) / 60.0

    def get_set_j(self, h, lw, phi, dec, n, m, l):
        w = self.hour_angle(h, phi, dec)
        a = self.approx_transit(w, lw, n)
        return self.solar_transit_j(a, m, l)

    def time_at_phase(self, date, sun_phase, lat, lon, height):
        lw = -math.radians(lon)
        phi = math.radians(lat)
        dh = self.observer_angle(height)

        d = self.to_days(date)
        n = self.julian_cycle(d, lw)
        ds = self.approx_transit(0.0, lw, n)

        m = self.solar_mean_anomaly(ds)
        l = self.ecliptic_longitude(m)
        dec = self.declination(l, 0.0)

        j_noon = self.solar_transit_j(ds, m, l)

        h0 = math.radians(sun_phase.angle_deg + dh)
        j_set = self.get_set_j(h0, lw, phi, dec, n, m, l)

        if sun_phase.is_rise:
            j_rise = j_noon - (j_set - j_noon)
            return self.from_julian(j_rise)
        else:
            return self.from_julian(j_set)

# Test example
if __name__ == "__main__":
    unixtime = 1362441600000
    lat = 48.0
    lon = 9.0

    calculator = SunPositionCalculator()
    pos = calculator.pos(unixtime, lat, lon)
    az = math.degrees(pos.azimuth)
    alt = math.degrees(pos.altitude)

    print(f"The position of the sun is {az}/{alt}")