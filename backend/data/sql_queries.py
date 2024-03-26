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

    ARRIVED = f"""
               SELECT
               	  1 AS Госпитизировано,
               	  mm.dept_get_name(h.dept_id) AS Отделение,
               	  ect.dzm56 AS Канал_госпитализации,
               		CASE h.patienttype
               			WHEN '0' THEN 'ЗЛ'
               			WHEN '1' THEN 'Иногородний'
               			WHEN '2' THEN 'НР'
               			WHEN '3' THEN 'НИЛ'
               			WHEN '4' THEN 'Контрагент'
               			WHEN '5' THEN 'ДМС'
               			WHEN '-1' THEN 'Не указано'
               		ELSE h.patienttype::TEXT
               		END AS Тип_пациента
               
               FROM mm.mdoc m
               JOIN mm.hospdoc h ON h.mdoc_id = m.id
               JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id
               JOIN mm.ehr_case_title ect ON ect.caseid  = ec.id 
               
               WHERE ec.create_dt BETWEEN DATE('{today()}') - INTERVAL '1 day, -6 hours' AND DATE('{today()}') - INTERVAL '-6 hours'
               
               UNION ALL 									
               
               SELECT 
                      0 AS отказано,
               	   'Приемное' AS Отделение,
               	    ect2.dzm56 AS Канал_госпитализации,
               		  CASE a.patienttype
               			WHEN '0' THEN 'ЗЛ'
               			WHEN '1' THEN 'Иногородний'
               			WHEN '2' THEN 'НР'
               			WHEN '3' THEN 'НИЛ'
               			WHEN '4' THEN 'Контрагент'
               			WHEN '5' THEN 'ДМС'
               			WHEN '-1' THEN 'Не указано'
               		ELSE a.patienttype::TEXT
               		END AS Тип_пациента
               		FROM mm.ambticket a
                    JOIN mm.ehr_case ec ON a.ehr_case_id = ec.id
               		JOIN mm.hosp_refuse hr ON hr.ambticket_id = a.id 
               		JOIN mm.ehr_case_title ect2 ON ect2.caseid  = a.ehr_case_id
               
               WHERE ec.create_dt BETWEEN DATE('{today()}') - INTERVAL '1 day, -6 hours' AND DATE('{today()}') - INTERVAL '-6 hours';
               """

    DEPT_HOSP = f"""
                 SELECT 
                 CASE pm.name
                 	WHEN  'акушерству и гинекологии (за исключением использования вспомогательных репродуктивных технологий)' THEN 'Гинекология'
                 	ELSE pm.name
                 END AS профиль,
                 count (m.id) AS cnt

                 FROM mm.mdoc m
                 JOIN mm.hospdoc h ON h.mdoc_id = m.id
                 JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id
                 JOIN mm.ehr_case_title ect ON ect.caseid  = ec.id 
                 JOIN mm.dept d ON d.id = h.dept_id
                 JOIN mm.profile_med pm ON pm.id = d.profile_med_id 

                 WHERE ec.create_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'

                 GROUP BY d.name, pm.name
                 ORDER BY cnt DESC;
                 """

    SIGNOUT = f"""
               SELECT mm.dept_get_name(h.dept_id) AS Отделение,
                CASE h.hosp_outcome_id
            		WHEN '5' THEN 'Умер в стационаре'
            		WHEN '4' THEN 'Переведён в другую МО из стационара'
            	ELSE 'Выписан'
            	END AS Исход
 
               FROM mm.mdoc m
               JOIN mm.hospdoc h ON h.mdoc_id = m.id
               
               WHERE h.leave_dt BETWEEN DATE('{today()}') - INTERVAL '1 day, -6 hours' AND DATE('{today()}') - INTERVAL '-6 hours'
               ORDER BY h.hosp_outcome_id;  
               """

    DEADS = f"""
             SELECT
	         mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,
             m.num||'-'||m.YEAR AS №ИБ,
                 CASE m.sex
	         		WHEN '1' THEN 'Муж'
	         		WHEN '2' THEN 'Жен'	
	         	END,
	         EXTRACT(YEAR from age(m.beg_dt, p.birth)) as Возраст,
	         h.dept_dt AS Дата_поступления,
	         ec.gravity AS Состояние_при_поступлении,
	         mm.dept_get_name(h.dept_id) AS Отделение, --отделение в которой умер пациент
	         h.bed_days AS кол_во_койко_дней,
                 (SELECT ic.kod
                     FROM mm.ds ds
                     JOIN mm.icd10 ic ON ic.id = ds.icd10_id
                      	  WHERE ds.ds_type_id = 4
                       	  AND ds.ehr_case_id = h.ehr_case_id
                           ORDER BY ds.create_dt DESC
                           LIMIT 1) AS Диаг_поступление,
             	    	h.final_diag_text AS Диаг_выписка,
                        mm.emp_get_fio_by_id (h.doctor_emp_id) AS Лечащий_врач
             	    	
             FROM mm.mdoc m
             JOIN mm.hospdoc h ON h.mdoc_id = m.id
             JOIN mm.people p ON p.id = m.people_id
             JOIN mm.ehr_case ec ON ec.id = h.ehr_case_id
 
             WHERE h.leave_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'
             AND h.hosp_outcome_id ='5' -- 5, умер в стационаре;
             """

    OAR_ARRIVED_QUERY = f"""
                         SELECT 
                         	    mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,
                                m.num||'-'||m.YEAR AS №ИБ,
                         	   EXTRACT(YEAR from age(m.beg_dt, p.birth)) as Возраст,
                         	   mm.dept_get_name(h.dept_id) AS Отделение,
                         	   mm.emp_get_fio_by_id (h.doctor_emp_id) AS Лечащий_врач,
                         (SELECT ic.kod
                            FROM mm.ds ds
                            JOIN mm.icd10 ic ON ic.id = ds.icd10_id
                            WHERE ds.ds_kind_id = 1
                            AND ds.ehr_case_id = h.ehr_case_id
                            ORDER BY ds.create_dt DESC
                            LIMIT 1) AS Диаг_поступление
                         
                         FROM mm.mdoc m
                         JOIN mm.hospdoc h ON h.mdoc_id = m.id
                         JOIN mm.people p ON p.id = m.people_id
                         
                         WHERE h.hosp_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'
                         AND h.dept_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'
                         AND h.dept_id IN (SELECT d.id from mm.dept d WHERE d.dept_med_type_id = 10220)
                         ORDER BY h.dept_id DESC;
                         """

    OAR_MOVED_QUERY = f"""
                       SELECT 
                       	    mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,
                            m.num||'-'||m.YEAR AS №ИБ,
                       	   EXTRACT(YEAR from age(m.beg_dt, p.birth)) as Возраст,
                       	   mm.dept_get_name(h.dept_id) AS Отделение,
                       	   mm.emp_get_fio_by_id (h.doctor_emp_id) AS Лечащий_врач,
                       	   h.dept_dt AS Дата_перевода,   
                       (SELECT d.name 
                       		FROM mm.hosp_move_hist hmh
                            	JOIN mm.dept d ON d.id = hmh.dept_id
                       	   	WHERE h.dept_dt = hmh.out_dt) AS Из_отделения,   
                       (SELECT ic.kod
                       		FROM mm.ds ds
                               JOIN mm.icd10 ic ON ic.id = ds.icd10_id
                               WHERE ds.ds_type_id = 1
                               AND ds.ehr_case_id = h.ehr_case_id
                               ORDER BY ds.create_dt DESC
                               LIMIT 1) AS Диаг_поступление   
                       FROM mm.mdoc m
                       JOIN mm.hospdoc h ON h.mdoc_id = m.id
                       JOIN mm.people p ON p.id = m.people_id

                       WHERE h.hosp_dt <=current_date - INTERVAL '1 day, -6 hours'
                       AND h.dept_dt BETWEEN current_date - INTERVAL '1 day, -6 hours' AND current_date - INTERVAL '-6 hours'
                       AND h.dept_id IN (SELECT d.id from mm.dept d WHERE d.dept_med_type_id = 10220)

                       ORDER BY h.dept_id DESC;
                       """

    OAR_CURRENT_QUERY = f"""
                         SELECT 
                         	   mm.famaly_io(m.surname,m.name,m.patron) AS ФИО_Пациента,
                               m.num||'-'||m.YEAR AS №ИБ,
                         	   EXTRACT(YEAR from age(m.beg_dt, p.birth)) as Возраст,
                         	   mm.dept_get_name(h.dept_id) AS Отделение,
                         	   mm.emp_get_fio_by_id (h.doctor_emp_id) AS Лечащий_врач,
                         	   h.bed_days AS койко_дни,
 
                         	   CASE WHEN EXISTS 
                         	    (SELECT ic.kod
                                    FROM mm.ds ds
                                    JOIN mm.icd10 ic ON ic.id = ds.icd10_id
                                    WHERE ds.ehr_case_id = h.ehr_case_id
                                    AND ds.ds_kind_id IN ('1') 
                                    AND ds.ds_type_id IN ('3')
                                    AND ds.create_dt  = (SELECT  max(d2.create_dt) 
                                     					  FROM mm.ds d2 
                                     					 WHERE d2.mdoc_id = m.id
                                     					   AND d2.ds_kind_id IN ('1') 
                                    						   AND d2.ds_type_id IN ('3'))
                                    						   LIMIT 1 )
                                 THEN (SELECT ic.kod
                         		         FROM mm.ds ds1
                         		         JOIN mm.icd10 ic ON ic.id = ds1.icd10_id
                         		         WHERE ds1.ehr_case_id = h.ehr_case_id
                         				 	AND ds1.ds_kind_id IN ('1')
                         		            AND ds1.ds_type_id IN ('3')
                         		            AND ds1.create_dt  = (SELECT  max(d3.create_dt) 
                                     					           FROM mm.ds d3 
                                     					           WHERE d3.mdoc_id = m.id
                                     					             AND d3.ds_kind_id IN ('1') 
                                    						             AND d3.ds_type_id IN ('3'))
                                    						             LIMIT 1 ) 
                                 ELSE  'не установлен' 
                         	    END AS Диаг_поступление
 
                         FROM mm.mdoc m
                         JOIN mm.hospdoc h ON h.mdoc_id = m.id
                         JOIN mm.people p ON p.id = m.people_id
 
                         WHERE h.leave_dt ISNULL
                         AND h.dept_id IN (SELECT d.id from mm.dept d WHERE d.dept_med_type_id = 10220);
                         """

    # Each string of this list is a keyword of dict where value is a serialized data.
    DICT_KEYWORDS = ['arrived', 'signout', 'deads', 'oar_deads',
                     'oar_arrived', 'oar_moved', 'oar_current', 'oar_numbers']

    # Lists of columns for mapping with values to creating CleanData class instances.
    COLUMNS = {
        'arrived': ['ch103', 'clinic_only', 'ch103_clinic', 'singly', 'plan',
                    'ZL', 'foreign', 'nr', 'nil', 'dms', 'undefined'],
        'signout': ['deads', 'moved', 'signout'],
        'deads_t': ['pat_fio', 'ib_num', 'sex', 'age', 'arriving_dt', 'state', 'dept', 'days', 'diag_arr',
                    'diag_dead', 'doc_fio'],
        'oar_arrived_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'diag_start'],
        'oar_moved_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'move_date', 'from_dept', 'diag_start'],
        'oar_current_t': ['pat_fio', 'ib_num', 'age', 'dept', 'doc_fio', 'days', 'diag_start'],
        'oar_amounts': ['oar1_d', 'oar2_d', 'oaronmk_d','oaroim_d','oar_d']
    }

    DMK_COLUMNS = ['arrived', 'hosp', 'refused', 'signout', 'deads', 'reanimation']

    # Filter-words for filter_dataset method of DataProcessing class.
    # If needed to add something more - "aapend" it, e.g. insert at the end of existing matched list.
    channels = ['103', 'Поликлиника', '103 Поликлиника', 'самотек', 'план']
    statuses = ['ЗЛ', 'Иногородний', 'НР', 'НИЛ', 'ДМС', 'Не указано'] 
    signout = ['Умер в стационаре', 'Переведён в другую МО из стационара', 'Выписан']
    oar_depts = ['Отделение реанимации и интенсивной терапии № 1', 
                 'Отделение реанимации и интенсивной терапии № 2',
                 'Отделение реанимации и интенсивной терапии для больных с ОНМК',
                 'Отделение реанимации и интенсивной терапии для больных с острым инфарктом миокарда',
                 'Отделение анестезиологии-реанимации'
                ]

    # Dict for mapping with serializer fields (relates to "план/факт по профилям" table).
    # All english names is fields of serializer.
    profiles_mapping = {
        'анестезиологии и реаниматологии': 'oar_p',
        'хирургии': 'surgery_p',
        'терапии': 'therapy_p',
        'неотложной медицинской помощи': 'emer1_p',
        'акушерству и гинекологии (за исключением использованиявспомогательных репродуктивных технологий)': 'gynekology_p',
        'рентгенологии': 'xray_p',
        'скорой медицинской помощи': 'emer2_p',
        'трансфузиологии': 'transfusiology_p',
        'общей практике': 'gpractice_p',
        'наркологии': 'narkology_p',
        'урологии': 'urology_p',
        'клинической лабораторной диагностике': 'lab_p',
        'реаниматологии': 'rean_p',
        'травматологии и ортопедии': 'truma_p',
        'нейрохирургии': 'neuro_p',
        'ультразвуковой диагностике': 'ultrasound_p',
        'функциональной диагностике': 'func_p',
        'кардиологии': 'cardio_p',
        'эндокринологии': 'endo_p',
        'неврологии': 'neurology_p',
        'медицинской статистике': 'static_p',
        'эпидемиологии': 'epid_p',
        'неонатологии': 'neon_p',
        'гистологии': 'gyst_p',
        'эндоскопии': 'endocop_p',
        'пульмонологии': 'pulmo_p'
    }

    # Dict for mapping columns on russian language with serializer fields (relates to "выписанные по отделениям" table).
    # All english names is fields of serializer.
    depts_mapping = {
        'Отделение реанимации и интенсивной терапии для больных с ОНМК': 'oaronmk_d',
        'Хирургическое отделение': 'surgery_d',
        'Отделение реанимации и интенсивной терапии № 1': 'oar1_d',
        'Приемное ДП': 'dp_d',
        'Отделение анестезиологии-реанимации': 'oar_d',
        'Отделение травматологии и ортопедии': 'trauma_d',
        'Нейрохирургическое отделение': 'neurosurgery_d',
        'Отделение реанимации и интенсивной терапии для больных с острым инфарктом миокарда': 'oaroim_d',
        'Отделение реанимации и интенсивной терапии № 2': 'oar2_d',
        'Кардиологическое отделение': 'cardio_d',
        'Терапевтическое отделение': 'therapy_d',
        'Эндокринологическое отделение': 'endo_d',
        'Неврологическое отделение для больных с ОНМК': 'neuroonmk_d',
        'Урологическое отделение': 'urology_d',
        'Отделение гнойной хирургии': 'pursurgery_d',
        '2 кардиологическое (ОИМ)': 'cardio2_d',
        'Стационар кратковременного пребывания': 'skp_d', 
        'Гинекологическое отделение': 'gynecology_d',
        'Приемное отделение': 'emer_d',
        'Многопрофильное отделение по оказанию платных медицинских услуг': 'multi_pay_d', 
        'Дневной стационар АПЦ': 'apc_d',
        'Отделение сочетанной травмы': 'combine_d',
        'Пульмонологическое отделение': 'pulmonology_d'
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

        :return: *list*: List of lists.
        """
        dmk_queries = self.queryset_for_dmk()[:-1]
        dmk_queries.insert(-1, self.DEADS)
        result = dmk_queries + [self.OAR_MOVED_QUERY, self.OAR_CURRENT_QUERY]
        return result

    def chosen_date_query(self, queryset: Union[str, list], chosen_date: str) -> list:
        """
        Replace date in the given query to passed and return query with needed date.

        :param queryset: *str*: Original class attribute query contains today date filter.
        :param chosen_date: Date for filtering that was chose users.
        :return: *str*: Changed query contains actual chosen date.
        """
        if type(queryset) is list:
            new_query = [query.replace(str(self.today()), chosen_date) for query in queryset]
            return new_query
        new_query = queryset.replace(str(self.today()), chosen_date)
        return [new_query]


