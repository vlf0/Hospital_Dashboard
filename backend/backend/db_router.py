class ExternalDatabaseRouter:
    """
    A database router to route all queries for the KISProfiles model
    to the 'kis_db' database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'external_kis' and model._meta.model_name == 'kisprofiles':
            return 'kis_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'external_kis' and model_name == 'kisprofiles':
            return False
        return None
