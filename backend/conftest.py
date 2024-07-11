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
def connect_to_dmk(request):

    conn = BaseConnectionDB(dbname=conn_dmk['NAME'],
                            host=conn_dmk['HOST'],
                            user=conn_dmk['USER'],
                            password=conn_dmk['PASSWORD']
                            )
    request.cls.conn = conn
    yield
    conn.close_connection()
