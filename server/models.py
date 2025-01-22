from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
import logging

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String (10), nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, value):
        """Ensure that the name is not empty and unique before insert."""
        if not value or value.strip() == "":
            raise ValueError("Author name cannot be empty.")
        
        
        if db.session.query(Author).filter_by(name=value).first():
            raise ValueError(f"Author name '{value}' must be unique.")
        return value
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        """Ensure the phone number is exactly 10 digits."""
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return value
 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String ,nullable=False)
    category = db.Column(db.String ,nullable=False)
    summary = db.Column(db.String ,nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content')
    def validate_content(self, key, value):
        """Ensure content is at least 250 characters long."""
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return value
    @validates('summary')
    def validate_summary(self, key, value):
        """Ensure the summary is at most 250 characters long."""
        if len(value) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return value
    @validates('category')
    def validate_category(self, key, value):
        """Ensure the category is either 'Fiction' or 'Non-Fiction'."""
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    @validates('title')
    def validate_title(self, key, value):
        """Ensure the title contains a clickbait keyword."""
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError("Post title must contain one of the following clickbait keywords: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
        return value  


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
