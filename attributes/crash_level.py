import enum

CrashLevel = enum.Enum(
    value="CrashLevel",
    names=[
        ("None", 0),
        ("Inadequate Warning of Exits, Lanes Narrowing, Traffic Controls etc.", 1),
        ("Shoulder Related", 2),
        ("Other Maintenance or Construction-Created Condition", 3),
        ("No or Obscured Pavement Marking", 4),
        ("Surface Under Water", 5),
        ("Inadequate Construction or Poor Design of Roadway, Bridge, etc.", 6),
        ("Surface Washed Out (Caved in, Road Slippage)", 7),
        ("Distracted Driver of a Non-Contact Vehicle", 12),
        ("Aggressive Driving/Road Rage by Non-Contact Vehicle Driver", 13),
        ("Motor Vehicle (In Transport 1983-2004) Struck By Falling Cargo or Something That Came Loose From or Something That Was Set in Motion By a Vehicle", 14),
        ("Non-Occupant Struck By Falling Cargo, or Something Came Loose From or Something That Was Set In Motion By A Vehicle", 15),
        ("Non-Occupant Struck Vehicle", 16),
        ("Vehicle Set In Motion By Non-Driver", 17),
        ("Date of Crash and Date of EMS Notification Were Not Same Day", 18),
        ("Recent Previous Crash Scene Nearby", 19),
        ("Police-Pursuit-Involved", 20),
        ("Within Designated School Zone", 21),
        ("Speed Limit Is a Statutory Limit as Recorded or Was Determined as This State’s 'Basic Rule'", 22),
        ("Indication of a Stalled/Disabled Vehicle", 23),
        ("Unstabilized Situation Began and All Harmful Events Occurred Off of the Roadway", 24),
        # Toll Plaza Related - 2012 Only rest of the years as is.
        ("Toll Booth/Plaza Related", 25),
        # Since 2013
        ("Backup Due to Prior Non-Recurring Incident", 26),
        ("Backup Due to Prior Crash", 27),
        ("Backup Due to Regular Congestion", 28),
        # 99 or -- is unknown.
    ]
)
