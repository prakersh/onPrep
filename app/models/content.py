from app.extensions import db


class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50), default='')
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

    concepts = db.relationship('Concept', backref='language', cascade='all, delete-orphan',
                               order_by='Concept.display_order')

    def __repr__(self):
        return f'<Language {self.name}>'


class Concept(db.Model):
    __tablename__ = 'concepts'

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default='')
    display_order = db.Column(db.Integer, default=0)
    estimated_minutes = db.Column(db.Integer, default=30)
    difficulty = db.Column(db.String(20), default='beginner')

    questions = db.relationship('Question', backref='concept', cascade='all, delete-orphan',
                                order_by='Question.display_order')

    __table_args__ = (
        db.UniqueConstraint('language_id', 'slug', name='uq_concept_language_slug'),
    )

    def __repr__(self):
        return f'<Concept {self.title}>'


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    difficulty = db.Column(db.String(20), default='beginner')
    tags = db.Column(db.JSON, default=list)

    answers = db.relationship('Answer', backref='question', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Question {self.title[:50]}>'


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    mode = db.Column(db.String(20), nullable=False)  # 'detailed' or 'quick'
    explanation = db.Column(db.Text, default='')
    pseudo_code = db.Column(db.Text, default='')
    actual_code = db.Column(db.Text, default='')
    code_language = db.Column(db.String(20), default='python')
    key_points = db.Column(db.JSON, default=list)
    gotchas = db.Column(db.JSON, default=list)

    __table_args__ = (
        db.CheckConstraint("mode IN ('detailed', 'quick')", name='ck_answer_mode'),
    )

    def __repr__(self):
        return f'<Answer {self.mode} for Q#{self.question_id}>'


class ConceptRelationship(db.Model):
    __tablename__ = 'concept_relationships'

    id = db.Column(db.Integer, primary_key=True)
    concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    related_concept_id = db.Column(db.Integer, db.ForeignKey('concepts.id'), nullable=False)
    relationship_type = db.Column(db.String(50), default='related')  # 'prerequisite', 'related'

    concept = db.relationship('Concept', foreign_keys=[concept_id], backref='outgoing_relationships')
    related_concept = db.relationship('Concept', foreign_keys=[related_concept_id])

    def __repr__(self):
        return f'<ConceptRelationship {self.concept_id} -> {self.related_concept_id}>'
