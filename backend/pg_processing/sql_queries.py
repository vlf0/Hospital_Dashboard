"""This module defines class responsible for giving whole query set of separated queries."""


class QuerySets:
    """
    QuerySets class.

    Contains each specific database query and the columns for that query data in a list as class attributes,
    as well as filter words, column sets, and serializer keywords.
    Also has method for creating common list of these queries.
    """

    ARRIVED = "SELECT * FROM mm.arrived;",

    DEPT_HOSP = "SELECT med_profile, amount FROM mm.dept_hosp;",

    SIGNOUT = "SELECT dept, status FROM mm.signout;",

    DEADS = "SELECT * FROM mm.deads;",

    OAR_ARRIVED_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, diag_start FROM mm.oar_arrived;",

    OAR_MOVED_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, move_date, from_dept, diag_start FROM mm.oar_moved;",

    OAR_CURRENT_QUERY = "SELECT pat_fio, ib_num, ages, dept, doc_fio, days, diag_start FROM mm.oar_current;",

    DMK_INSERT_QUERY = "INSERT INTO own.arrived (arrived, hosp, refused, signout, deads, reanimation)" \
                       " VALUES (%s, %s, %s, %s);"

    # Each string of this list is a keyword of dict where value is a serialized data.
    DICT_KEYWORDS = ['arrived', 'dept_hosp', 'signout']

    # Lists of columns for mapping with values to creating CleanData class instances.
    COLUMNS = {
        'arrived': ['ch103', 'clinic_only', 'ch103_clinic', 'singly', 'ZL', 'foreign', 'moscow', 'undefined'],
        'signout': ['deads', 'moved', 'signout']
    }

    # Filter-words for filter_dataset method of DataProcessing class.
    channels = ['103', 'Поликлиника', '103 Поликлиника', 'Самотек']
    statuses = ['ЗЛ', 'Иногородние', 'Москвичи', 'не указано']
    signout = ['Умер', 'Переведен', 'Выписан']

    profiles_mapping = {
        'Терапия': 'therapy',
        'Хирургия': 'surgery',
        'Кардиология': 'cardiology',
        'Урология': 'urology',
        'Неврология': 'neurology'
    }

    depts_mapping = {
        'ОРИТ №1': 'oar1',
        'ОРИТ №2': 'oar2',
        'Кардиологическое отделение': 'cardio_d',
        'Хирургическое отделение': 'surgery_d',
        'Терапевтическое отделение': 'therapy_d'
    }

    def queryset_for_dmk(self):
        """
        Create list of lists queries from class attributes needed for data to DMK DB.

        :return: List of lists.
        """
        result = [self.ARRIVED, self.SIGNOUT, self.OAR_ARRIVED_QUERY]
        return result

    def queryset_for_kis(self):
        """
        Create list of lists queries from class attributes needed for data to front-end.

        :return: List of lists.
        """
        dmk_queries = self.queryset_for_dmk()
        dmk_queries.insert(2, self.DEADS)
        dmk_queries.insert(1, self.DEPT_HOSP)
        result = dmk_queries + [self.OAR_CURRENT_QUERY, self.OAR_MOVED_QUERY]
        return result

