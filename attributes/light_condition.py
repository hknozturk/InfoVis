import enum

LightCondition = enum.Enum(
    value="LightCondition",
    names=[
        ("Daylight", 1),
        ("Dark - Not Lighted", 2),
        ("Dark - Lighted", 3),
        ("Dawn", 4),
        ("Dusk", 5),
        ("Dark - Unknown Lighting", 6),
        ("Other", 7)
    ]
)
