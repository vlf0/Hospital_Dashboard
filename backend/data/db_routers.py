class KisDbRouter:
    """
    A router to control all database operations on models in the
    'backend' application to use the 'kis_db' database.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to kis_db.
        """
        if model._meta.app_label == 'data':
            return 'kis_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to kis_db.
        """
        if model._meta.app_label == 'data':
            return None
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the your_app app is involved.
        """
        # if obj1._state.db == 'kis_db' and obj2._state.db == 'kis_db':
        #     return False
        # elif obj1._state.db == 'default' and obj2._state.db == 'default':
        #     return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the backend app's models get created on the right database.
        """
        if db == 'kis_db':
            return False
        return None
