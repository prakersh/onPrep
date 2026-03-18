"""Progress models removed -- all user-specific data is in browser localStorage.

The following models were removed for privacy (shared server, no user accounts):
- Progress: question completion tracking -> awesomeprep:progress
- Deadline: interview deadlines -> awesomeprep:deadlines
- ScheduleItem: study schedule items -> awesomeprep:deadlines (embedded)
"""
