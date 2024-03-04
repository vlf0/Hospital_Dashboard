"""This module defines class responsible for giving whole query set of separated queries."""


class QuerySets:
    """
    QuerySets class.

    Contains specific database queries and columns for receiving data from that queries as class attributes,
    as well as filter words, column sets as dicts for mapping, and serializer keywords.
    Also has method for creating common list of these queries.
    """

    ARRIVED = "SELECT * FROM mm.arrived;"

    DEPT_HOSP = "SELECT med_profile, amount FROM mm.dept_hosp;"

    SIGNOUT = "SELECT dept, status FROM mm.signout;"

    DEADS = "SELECT pat_fio, ib_num, sex, agee, arriving_dt, state, dept, days, diag_arr, diag_dead FROM mm.deads;"

    OAR_ARRIVED_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, diag_start FROM mm.oar_arrived;"

    OAR_MOVED_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, move_date, from_dept, diag_start FROM mm.oar_moved;"

    OAR_CURRENT_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, days, diag_start FROM mm.oar_current;"

    # Each string of this list is a keyword of dict where value is a serialized data.
    DICT_KEYWORDS = ['arrived', 'signout', 'deads',
                     'oar_arrived', 'oar_moved', 'oar_current', 'oar_numbers']

    # Lists of columns for mapping with values to creating CleanData class instances.
    COLUMNS = {
        'arrived': ['ch103', 'clinic_only', 'ch103_clinic', 'singly', 'ZL', 'foreign', 'moscow', 'undefined'],
        'signout': ['deads', 'moved', 'signout'],
        'deads_t': ['pat_fio', 'ib_num', 'sex', 'age', 'arriving_dt', 'state', 'dept', 'days', 'diag_arr', 'diag_dead'],
        'oar_arrived_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'diag_start'],
        'oar_moved_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'move_date', 'from_dept', 'diag_start'],
        'oar_current_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'days', 'diag_start'],
        'oar_amounts': ['oar1', 'oar2', 'oar3']
    }

    DMK_COLUMNS = ['arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']

    # Filter-words for filter_dataset method of DataProcessing class.
    channels = ['103', 'Поликлиника', '103 Поликлиника', 'Самотек']
    statuses = ['ЗЛ', 'Иногородние', 'Москвичи', 'не указано']
    signout = ['Умер', 'Переведен', 'Выписан']

    # Dict for mapping with serializer fields (relates to "план/факт по профилям" table).
    # All english names is fields of serializer.
    profiles_mapping = {
        'Терапия': 'therapy',
        'Хирургия': 'surgery',
        'Кардиология': 'cardiology',
        'Урология': 'urology',
        'Неврология': 'neurology'
    }

    # Dict for mapping columns on russian language with serializer fields (relates to "выписанные по отделениям" table).
    # All english names is fields of serializer.
    depts_mapping = {
        'ОРИТ №1': 'oar1',
        'ОРИТ №2': 'oar2',
        'ОРИТ №3': 'oar3',
        'Кардиологическое отделение': 'cardio_d',
        'Хирургическое отделение': 'surgery_d',
        'Терапевтическое отделение': 'therapy_d'
    }

    def queryset_for_dmk(self):
        """
        Create list of lists queries from class attributes needed for data to DMK DB.

        :return: List of lists.
        """
        result = [self.ARRIVED, self.SIGNOUT, self.OAR_ARRIVED_QUERY, self.DEPT_HOSP]
        return result

    def queryset_for_kis(self):
        """
        Create list of lists queries from class attributes needed for data to front-end.

        :return: List of lists.
        """
        dmk_queries = self.queryset_for_dmk()[:-1]
        dmk_queries.insert(-1, self.DEADS)
        result = dmk_queries + [self.OAR_MOVED_QUERY, self.OAR_CURRENT_QUERY]
        return result
