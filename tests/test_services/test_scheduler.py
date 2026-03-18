"""Scheduler service has been removed.

The scheduling algorithm is now implemented client-side in JavaScript
within the planner templates. See app/templates/planner/setup.html.
"""


class TestSchedulerRemoved:
    def test_scheduler_module_removed(self):
        """Scheduler service should not exist -- algorithm is now in JS."""
        import importlib
        try:
            importlib.import_module('app.services.scheduler')
            assert False, 'app.services.scheduler should not exist'
        except (ImportError, ModuleNotFoundError):
            pass
