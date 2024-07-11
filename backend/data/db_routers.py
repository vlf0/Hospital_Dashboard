class DMKDBRouter:
    """
    A router to control all database operations on models in the
    'backend' application to use the 'kis_db' database.
    """

    route_app_labels = {'data'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to the appropriate database.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'dmk'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to kis_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'dmk'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the your_app app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
            ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that the backend app's models get created on the right database.
        """
        if app_label in self.route_app_labels:
            return True
        return None
