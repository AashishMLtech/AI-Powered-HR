class SimpleCeleryApp:
    """Tiny placeholder so the project shape matches the document without requiring Redis."""

    def task(self, func):
        return func


celery_app = SimpleCeleryApp()
