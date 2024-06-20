"""This module defines class responsible for giving whole query set of separated queries."""
from datetime import date
from typing import Union


class QuerySets:
    """
    QuerySets class.

    Contains specific database queries and columns for receiving data from that queries as class attributes,
    as well as filter words, column sets as dicts for mapping, and serializer keywords.
    Also has method for creating common list of these queries.
    """

    today = date.today

    KIS_PROFILES = """
                   SELECT id, name
                   FROM mm.profile_med;
                   """

    ARRIVED = """
              SELECT 
              ar.status,
              ar.dept,
              ar.channel,
              ar.patient_type 
              FROM mm.arrived ar
              WHERE dates BETWEEN CURRENT_DATE - INTERVAL '18 hours' and CURRENT_DATE + INTERVAL '6 hours';
              """

    DEPT_HOSP = """
                SELECT profile_id, amount FROM mm.dept_hosp
                WHERE dates BETWEEN CURRENT_DATE - INTERVAL '18 hours' and CURRENT_DATE + INTERVAL '6 hours';
                """

    SIGNOUT = """
              SELECT 
              sg.dept,
              sg.status
              FROM mm.signout sg
              WHERE dates BETWEEN CURRENT_DATE - INTERVAL '18 hours' and CURRENT_DATE + INTERVAL '6 hours';
              """

    DEADS = """
            SELECT 
            dd.pat_fio,
            dd.ib_num,
            dd.sex,
            dd.agee,
            dd.arriving_dt,
            dd.state,
            dd.dept,
            dd.days,
            dd.diag_arr,
            dd.diag_dead
            FROM mm.deads dd
            WHERE dates BETWEEN CURRENT_DATE - INTERVAL '18 hours' and CURRENT_DATE + INTERVAL '6 hours';
            """

    OAR_ARRIVED_QUERY = """
                        SELECT 
                        pat_fio,
                        ib_num, 
                        ages, 
                        dept,
                        doc_fio, 
                        diag_start FROM mm.oar_arrived
                        WHERE dates BETWEEN CURRENT_DATE - INTERVAL '18 hours' and CURRENT_DATE + INTERVAL '6 hours';
                        """

    OAR_MOVED_QUERY = """SELECT pat_fio, ib_num, ages, dept, doc_fio, move_date, from_dept, diag_start
                         FROM mm.oar_moved;"""

    OAR_CURRENT_QUERY = """SELECT pat_fio, ib_num, ages, dept, doc_fio, days, diag_start FROM mm.oar_current;"""

    # Each string of this list is a keyword of dict where value is a serialized data.
    DICT_KEYWORDS = ['arrived', 'signout', 'deads', 'oar_deads',
                     'oar_arrived', 'oar_moved', 'oar_current', 'oar_numbers']

    # Lists of columns for mapping with values to creating CleanData class instances.
    COLUMNS = {
        'arrived': ['ch103', 'clinic_only', 'ch103_clinic', 'singly', 'plan',
                    'ZL', 'foreign', 'nr', 'nil', 'dms', 'undefined'],
        'signout': ['deads', 'moved', 'signout'],
        'deads_t': ['pat_fio', 'ib_num', 'sex', 'age', 'arriving_dt', 'state', 'dept', 'days', 'diag_arr', 'diag_dead'],
        'oar_arrived_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'diag_start'],
        'oar_moved_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'move_date', 'from_dept', 'diag_start'],
        'oar_current_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'days', 'diag_start'],
        'oar_amounts': ['oar1', 'oar2', 'oar3']
    }

    DMK_COLUMNS = ['arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']
    DMK_DETAILS_COLUMNS = ('registered',)

    # Filter-words for filter_dataset method of DataProcessing class.
    # If needed to add something more - "aapend" it, e.g. insert at the end of existing matched list.
    channels = ['103', 'Поликлиника', '103 Поликлиника', 'самотек', 'план']
    statuses = ['ЗЛ', 'Иногородний', 'НР', 'НИЛ', 'ДМС', 'Не указано']
    signout = ['Умер', 'Переведен', 'Выписан']
    oar_depts = ['ОРИТ №1', 'ОРИТ №2', 'ОРИТ №3']

    # Dict for mapping columns on russian language with serializer fields (relates to "выписанные по отделениям" table).
    # All english names is fields of serializer.
    depts_mapping = {
        'ОРИТ №1': 'oar1_d',
        'ОРИТ №2': 'oar2_d',
        'ОРИТ №3': 'oar3_d',
        'Кардиологическое отделение': 'cardio_d',
        'Хирургическое отделение': 'surgery_d',
        'Терапевтическое отделение': 'therapy_d'
    }

    def queryset_for_dmk(self) -> list[str]:
        """
        Create list of lists queries from class attributes needed for data to DMK DB.

        :return: List of lists.
        """
        result = [self.ARRIVED, self.SIGNOUT, self.OAR_ARRIVED_QUERY, self.DEPT_HOSP]
        return result

    def queryset_for_kis(self) -> list[str]:
        """
        Create list of lists queries from class attributes needed for data to front-end.

        :return: *list*: List of lists.
        """
        dmk_queries = self.queryset_for_dmk()[:-1]
        dmk_queries.insert(-1, self.DEADS)
        result = dmk_queries + [self.OAR_MOVED_QUERY, self.OAR_CURRENT_QUERY]
        return result

    @staticmethod
    def chosen_date_query(queryset: Union[str, list], chosen_date: str) -> list:
        """
        Replace date in the given query to passed and return query with needed date.

        :param queryset: *str*: Original class attribute query contains today date filter.
        :param chosen_date: Date for filtering that was chose users.
        :return: *str*: Changed query contains actual chosen date.
        """
        if type(queryset) is list:
            new_query = [query.replace('CURRENT_DATE', f'DATE \'{chosen_date}\'') for query in queryset]
            return new_query
        new_query = queryset.replace('CURRENT_DATE', f'DATE \'{chosen_date}\'')
        return [new_query]

    @staticmethod
    def insert_accum_query(dataset, dates, id_cnt) -> str:
        profile_id, number = dataset[0], dataset[1]
        raw_query = f"""
                     INSERT INTO public.data_accumulationofincoming (id, dates, number, profile_id) 
                     VALUES 
                     ({id_cnt}, '{dates}', {number}, '{profile_id}');
                     """
        return raw_query


class EmergencyQueries:

    WAITINGS = """
               SELECT pat_fio, ib_num, dept, waiting_time, doc_fio from mm.waitings;
               """

    TOTAL_REFUSE = """
                   SELECT doc_fio, total_refuse FROM mm.total_refuse;
                   """

    __DETAIL_REFUSE = """
                      SELECT pat_fio, ib_num, diag, refuse_reason, refuse_date, doc_fio
                      FROM mm.refuse WHERE doc_fio = 'passed_doc_fio';
                      """

    COLUMNS = {
        'total_refuse': ['doc_fio', 'refuses_amount'],
        'detail_refuse': ['pat_fio', 'ib_num', 'diag', 'refuse_reason', 'refuse_date', 'doc_fio'],
        'waitings': ['pat_fio', 'ib_num', 'dept', 'waiting_time', 'doc_fio'],
    }

    def get_emergency_queries(self) -> list[str]:
        queries_list = [self.WAITINGS, self.TOTAL_REFUSE]
        return queries_list

    def get_detail_refuse_query(self, doc_names: list) -> list[str]:
        refuse_query = [self.__DETAIL_REFUSE.replace('passed_doc_fio', f'{name}') for name in doc_names]
        return refuse_query


class PlanHospitalizationQueries:

    PLAN_HOSP = """SELECT week, dates, dept, cnt_plan FROM mm.plan_hosp ORDER BY dates asc;"""

    COLUMNS = {
        'common_field': ['week', 'dates', 'dept', 'cnt_plan']
    }

    def get_plan_hosp_query(self) -> list[str]:
        return [self.PLAN_HOSP]



