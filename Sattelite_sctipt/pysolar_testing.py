import pysolar.solar as ps
import datetime

latitude_deg = 50.387345
longitude_deg = 30.4715298

d = datetime.datetime.now()

altitude_deg = ps.get_altitude(latitude_deg, longitude_deg, d)
azimuth_deg = ps.get_azimuth(latitude_deg, longitude_deg, d)
print(altitude_deg, azimuth_deg)
