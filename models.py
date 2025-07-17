from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Add cascade for CampaignEmployee records when an Employee is deleted
    campaigns = db.relationship('CampaignEmployee', back_populates='employee', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Employee {self.email}>'

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    email_body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Add cascade for CampaignEmployee and Click records when a Campaign is deleted
    # The 'clicks' cascade ensures that even if a Click isn't directly linked to CampaignEmployee
    # it gets deleted when its parent Campaign goes.
    employees = db.relationship('CampaignEmployee', back_populates='campaign', lazy=True, cascade='all, delete-orphan')
    clicks = db.relationship('Click', back_populates='campaign', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f'<Campaign {self.name}>'

class CampaignEmployee(db.Model):
    __tablename__ = 'campaign_employee'
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    unique_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4())) # For tracking
    sent_at = db.Column(db.DateTime, nullable=True)

    campaign = db.relationship('Campaign', back_populates='employees')
    # employee = db.relationship('Employee', back_popates='campaigns')
    employee = db.relationship('Employee', back_populates='campaigns') 

    def __repr__(self):
        return f'<CampaignEmployee Campaign: {self.campaign_id}, Employee: {self.employee_id}>'

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add ondelete='CASCADE' to all relevant foreign keys for database-level cascading
    unique_id = db.Column(db.String(36), db.ForeignKey('campaign_employee.unique_id', ondelete='CASCADE'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45)) # IPv4 or IPv6
    user_agent = db.Column(db.Text)

    campaign = db.relationship('Campaign', back_populates='clicks')
    employee = db.relationship('Employee', uselist=False, lazy='joined',
                               primaryjoin="Click.employee_id == Employee.id")
    campaign_employee = db.relationship('CampaignEmployee', uselist=False, lazy='joined',
                                        primaryjoin="Click.unique_id == CampaignEmployee.unique_id")

    def __repr__(self):
        return f'<Click {self.unique_id}>'