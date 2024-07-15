import pytest
from django.db import connections
from data.psycopg_module import BaseConnectionDB

conn_kis = connections.settings['kis_db']
conn_dmk = connections.settings['dmk']


@pytest.fixture(scope='class')
def connect_to_kisdb(request):

    conn = BaseConnectionDB(dbname=conn_kis['NAME'],
                            host=conn_kis['HOST'],
                            user=conn_kis['USER'],
                            password=conn_kis['PASSWORD']
                            )
    request.cls.conn = conn
    yield
    conn.close_connection()


@pytest.fixture
def main_sql_queries(request):
    date = '2025-01-01'
    query = """
        SELECT * FROM mm.test
        WHERE ec.create_dt BETWEEN CURRENT_DATE - INTERVAL '18 hours'
        AND CURRENT_DATE + INTERVAL '6 hours'
    """
    answer = f"""
        SELECT * FROM mm.test
        WHERE ec.create_dt BETWEEN DATE '2025-01-01' - INTERVAL '18 hours'
        AND DATE '2025-01-01' + INTERVAL '6 hours'
    """
    request.cls.date = date
    request.cls.query = query
    request.cls.answer = answer


@pytest.fixture
def emergency_sql_queries(request):
    initials = ['Bob', 'Fred', 'Helen']
    request.cls.initials = initials

