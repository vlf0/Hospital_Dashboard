ARRIVED = [
            "SELECT * FROM mm.arrived;",
            ['status', 'dept', 'channel', 'patient_type']
]

SIGNOUT = [
            "SELECT dept, status FROM mm.signout;",
            ['dept', 'status']
]

DEADS = [
          "SELECT * FROM mm.deads;",
          ['pat_fio', 'ib_num', 'sex', 'ages', 'arriving_dt', 'state', 'dept', 'days', 'diag_arr', 'diag_dead']

]

OAR_ARRIVED_QUERY = "SELECT * FROM mm.oar_arrived;"
OAR_MOVED_QUERY = "SELECT * FROM mm.oar_moved;"
OAR_CURRENT_QUERY = "SELECT * FROM mm.oar_current;;"


INSERT_QUERY = "INSERT INTO own.arrived (status, dept, channel, patient_type) VALUES (%s, %s, %s, %s);"

