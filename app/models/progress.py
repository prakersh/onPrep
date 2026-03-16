from datetime import datetime, timezone
from app.extensions import db


class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), unique=True, nullable=False)
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    confidence = db.Column(db.Integer, default=0)  # 1-5
    last_studied_at = db.Column(db.DateTime, nullable=True)
    times_reviewed = db.Column(db.Integer, default=0)

    question = db.relationship('Question', backref=db.backref('progress', uselist=False))

    def __repr__(self):
        return f'<Progress Q#{self.question_id} {self.status}>'


class Deadline(db.Model):
    __tablename__ = 'deadlines'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    company_name = db.Column(db.String(200), default='')
    role = db.Column(db.String(200), default='')
    interview_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)
    color = db.Column(db.String(20), default='indigo')  # for visual distinction

    language = db.relationship('Language', backref='deadlines')
    schedule_items = db.relationship('ScheduleItem', backref='deadline', cascade='all, delete-orphan',
                                    order_by='ScheduleItem.scheduled_date')

    def __repr__(self):
        return f'<Deadline {self.company_name} {self.interview_date}>'


class ScheduleItem(db.Model):
    __tablename__ = 'schedule_items'

    id = db.Column(db.Integer, primary_key=True)
    deadline_id = db.Column(db.Integer, db.ForeignKey('deadlines.id'), nullable=False)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    is_review = db.Column(db.Boolean, default=False)

    concept = db.relationship('Concept', backref='schedule_items')

    def __repr__(self):
        return f'<ScheduleItem {self.scheduled_date} concept={self.concept_id}>'
