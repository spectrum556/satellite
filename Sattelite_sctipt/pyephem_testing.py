import ephem

target = ephem.Observer()

target.lon = '-84.39733'
target.lat = '33.775867'
target.elevation = 320

target.date = '1984/5/30 16:22:56'

satel = ephem.FixedBody
v = ephem.Observer(target)
print('%s %s' % (v.alt, v.az))
# 72:19:44.8 134:14:25.3
