"""Progress models (Progress, Deadline, ScheduleItem) have been removed.

All user-specific data (progress, deadlines, schedules) is now stored
client-side in browser localStorage for privacy.
"""


class TestProgressModelsRemoved:
    def test_no_progress_model(self):
        """Progress model should not exist -- progress is in localStorage."""
        from app.models import __all__ as exported
        assert 'Progress' not in exported

    def test_no_deadline_model(self):
        """Deadline model should not exist -- deadlines are in localStorage."""
        from app.models import __all__ as exported
        assert 'Deadline' not in exported

    def test_no_schedule_item_model(self):
        """ScheduleItem model should not exist -- schedules are in localStorage."""
        from app.models import __all__ as exported
        assert 'ScheduleItem' not in exported
