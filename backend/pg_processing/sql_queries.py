"""This module defines class responsible for giving whole query set of separated queries."""


class QuerySets:
    """
    QuerySets class.

    Contains each specific database query and the columns for that query data in a list as class attributes.
    Also has method for creating common list of these queries.
    """

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
    OAR_ARRIVED_QUERY = [
        "SELECT pat_fio, ib_num, ages, dept, doc_fio, diag_start FROM mm.oar_arrived;",
        ['pat_fio', 'ib_num', 'ages', 'dept', 'doc_fio', 'diag_start']
    ]

    OAR_MOVED_QUERY = [
        "SELECT pat_fio, ib_num, ages, dept, doc_fio, move_date, from_dept, diag_start FROM mm.oar_moved;",
        ['pat_fio', 'ib_num', 'ages', 'dept', 'doc_fio', 'move_date', 'from_dept', 'diag_start']
    ]
    OAR_CURRENT_QUERY = [
        "SELECT pat_fio, ib_num, ages, dept, doc_fio, days, diag_start FROM mm.oar_current;",
        ['pat_fio', 'ib_num', 'ages', 'dept', 'doc_fio', 'days', 'diag_start']

    ]
    DMK_INSERT_QUERY = "INSERT INTO own.arrived (status, dept, channel, patient_type) VALUES (%s, %s, %s, %s);"

    def get_ready_queryset(self):
        """
        Create list of lists queries from class attributes.

        :return: List of lists.
        """
        result = [self.ARRIVED, self.SIGNOUT, self.DEADS,
                  self.OAR_ARRIVED_QUERY, self.OAR_CURRENT_QUERY, self.OAR_MOVED_QUERY]
        return result








