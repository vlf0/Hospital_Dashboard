import pytest
from data.sql_queries import MainQueries, EmergencyQueries, PlanHospitalizationQueries


class TestMainQueries:

    checking_class = MainQueries()
    dmk_query = checking_class.create_dmk_query()
    kis_query = checking_class.create_kis_query()

    @staticmethod
    def normalize_query(query):
        return '\n'.join(line.strip() for line in query.strip().split('\n'))

    def test_environment_query(self):
        current_query = self.checking_class.KIS_PROFILES
        production_query = """
	        SELECT pm.id,pm.name
    
            FROM mm.dept d
            JOIN mm.bed_fund bf ON bf.dept_id = d.id
            JOIN mm.profile_med pm ON pm.id = d.profile_med_id
    
            WHERE bf.bed_count >= 1
            AND d.end_dt ISNULL
    
            GROUP BY pm.id,pm.name
            ORDER BY pm.id;
        """
        r_production_query = self.normalize_query(production_query)
        r_current_query = self.normalize_query(current_query)
        assert r_production_query == r_current_query

    def test_create_dmk_query_length(self):
        assert len(self.dmk_query) == 4

    def test_create_dmk_query(self):
        for i in self.dmk_query:
            assert i != ''

    def test_create_kis_query_length(self):
        assert len(self.kis_query) == 6

    def test_create_kis_query_order(self):
        parent = self.checking_class
        query = parent.create_kis_query()
        assert query[2] == parent.DEADS and query[-1] == parent.OAR_CURRENT_QUERY

    @pytest.mark.usefixtures('main_sql_queries')
    def test_chosen_date_query_type(self):
        parent = self.checking_class
        result = parent.chosen_date_query(self.query, self.date)
        assert isinstance(result, list)

    @pytest.mark.usefixtures('main_sql_queries')
    def test_chosen_date_query(self):
        parent = self.checking_class
        result = parent.chosen_date_query(self.query, self.date)
        assert result[0] == self.answer


class TestEmergencyQueries:

    checking_class = EmergencyQueries()

    def test_get_emergency_queries(self):
        queries = self.checking_class.get_emergency_queries()
        assert len(queries) == 2

    @pytest.mark.usefixtures('emergency_sql_queries')
    def test_get_detail_refuse_query_length(self):
        result = self.checking_class.get_detail_refuse_query(self.initials)
        assert len(result) == 3

    @pytest.mark.usefixtures('emergency_sql_queries')
    def test_get_detail_refuse_query(self):
        result = self.checking_class.get_detail_refuse_query(self.initials)
        assert 'Bob' in result[0]


class TestPlanHospitalizationQueries:

    checking_class = PlanHospitalizationQueries()

    def test_get_plan_hosp_query_length(self):
        result = self.checking_class.get_plan_hosp_query()
        assert len(result) == 1

    def test_get_plan_hosp_query(self):
        parent = self.checking_class
        result = parent.get_plan_hosp_query()
        assert result[0] == parent.PLAN_HOSP

