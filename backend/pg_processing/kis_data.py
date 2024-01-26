from .psycopg_module import kis_conn
from .sql_queries import *
from .serializers import KISDataSerializer


class KISData:

    kis_conn = kis_conn.execute_query

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.dept = kwargs.get('dept')
        self.channel = kwargs.get('channel')
        self.patient_type = kwargs.get('patient_type')
        self.status = kwargs.get('status')

    @staticmethod
    def arrived_data():
        data = KISData.kis_conn(ARRIVED_QUERY)
        objects_list = [KISData(id=row[0], dept=row[1], channel=row[2], patient_type=row[3]) for row in data]
        return objects_list

    @staticmethod
    def signout_data():
        data = KISData.kis_conn(SIGNOUT_QUERY)
        objects_list = [KISData(id=row[0], dept=row[1], status=row[2]) for row in data]
        return objects_list


arr_dict = KISData().arrived_data()
signout_dict = KISData().signout_data()

# print(KISDataSerializer(arr_dict, many=True).data)
# print(KISDataSerializer(signout_dict, many=True).data)



