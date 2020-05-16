import enum

Weather = enum.Enum(
    value="Weather",
    names=[
        ("No additional Atmospheric Conditions", 0),
        ("Clear", 1),
        ("Rain", 2),
        ("Sleet, Hail", 3),  # 2010-2012: Sleet, Hait (Freezing Rain or Drizzle)
        ("Snow", 4),
        ("Fog, Smog, Smoke", 5),
        ("Severe Crosswinds", 6),
        ("Blowing Sand, Soil, Dirt", 7),
        ("Other", 8),
        ("Cloudy", 10),
        ("Blowing Snow", 11),
        ("Freezing Rain or Dizzle", 12),  # Since 2013
    ]
)
