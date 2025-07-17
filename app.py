import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from models import db, Employee, Campaign, CampaignEmployee, Click
from phishing_sender import send_phishing_email
from config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    db.init_app(app)

    with app.app_context():
        db.create_all() # Create database tables if they don't exist

    @app.route('/')
    def index():
        campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
        employees = Employee.query.order_by(Employee.name).all()
        return render_template('index.html', campaigns=campaigns, employees=employees)

    @app.route('/employees/add', methods=['GET', 'POST'])
    def add_employee():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            if not name or not email:
                flash('Name and Email are required.', 'danger')
                return redirect(url_for('add_employee'))

            existing_employee = Employee.query.filter_by(email=email).first()
            if existing_employee:
                flash('Employee with this email already exists.', 'warning')
                return redirect(url_for('add_employee'))

            new_employee = Employee(name=name, email=email)
            try:
                db.session.add(new_employee)
                db.session.commit()
                flash('Employee added successfully!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding employee: {e}', 'danger')

        return render_template('add_employee.html')

    # NEW: Route to delete an employee
    @app.route('/employees/<int:employee_id>/delete', methods=['POST'])
    def delete_employee(employee_id):
        employee = Employee.query.get_or_404(employee_id)
        try:
            db.session.delete(employee)
            db.session.commit()
            flash(f'Employee "{employee.name}" and all associated data deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting employee: {e}', 'danger')
        return redirect(url_for('index'))


    @app.route('/campaigns/create', methods=['GET', 'POST'])
    def create_campaign():
        employees = Employee.query.all()
        if request.method == 'POST':
            name = request.form.get('name')
            subject = request.form.get('subject')
            email_body = request.form.get('email_body')
            selected_employee_ids = request.form.getlist('employees')

            if not name or not subject or not email_body or not selected_employee_ids:
                flash('All fields and at least one employee are required.', 'danger')
                return redirect(url_for('create_campaign'))

            new_campaign = Campaign(name=name, subject=subject, email_body=email_body)
            db.session.add(new_campaign)
            db.session.commit() # Commit to get the campaign ID

            for emp_id in selected_employee_ids:
                employee = Employee.query.get(emp_id)
                if employee:
                    campaign_employee = CampaignEmployee(
                        campaign=new_campaign,
                        employee=employee
                    )
                    db.session.add(campaign_employee)
            db.session.commit()
            flash('Campaign created successfully! Now you can send it.', 'success')
            return redirect(url_for('index'))
        return render_template('create_campaign.html', employees=employees)

    @app.route('/campaigns/<int:campaign_id>/send', methods=['POST'])
    def send_campaign(campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        campaign_employees = CampaignEmployee.query.filter_by(campaign_id=campaign.id).all()

        if not campaign_employees:
            flash('No employees associated with this campaign.', 'warning')
            return redirect(url_for('index'))

        emails_sent = 0
        for ce in campaign_employees:
            # Construct the tracking link
            # IMPORTANT: Replace 'http://127.0.0.1:5000' with your actual public domain/IP
            tracking_link = url_for('track_click', unique_id=ce.unique_id, _external=True)

            # Use the stored email body, which should have {{tracking_link}} placeholder
            email_body_with_link = campaign.email_body.replace("{{tracking_link}}", tracking_link)

            if send_phishing_email(ce.employee.email, campaign.subject, email_body_with_link, tracking_link):
                ce.sent_at = datetime.utcnow()
                emails_sent += 1
            else:
                flash(f'Failed to send email to {ce.employee.email}. Check SMTP config.', 'danger')

        db.session.commit()
        flash(f'Campaign "{campaign.name}" sent to {emails_sent} employees!', 'success')
        return redirect(url_for('index'))

    @app.route('/track/<unique_id>')
    def track_click(unique_id):
        campaign_employee = CampaignEmployee.query.filter_by(unique_id=unique_id).first()
        if campaign_employee:
            existing_click = Click.query.filter_by(unique_id=unique_id).first()
            if not existing_click:
                # Record the click
                new_click = Click(
                    unique_id=unique_id,
                    campaign_id=campaign_employee.campaign_id,
                    employee_id=campaign_employee.employee_id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent')
                )
                db.session.add(new_click)
                db.session.commit()
                app.logger.info(f"Click recorded for unique_id: {unique_id}")
            else:
                app.logger.info(f"Duplicate click from unique_id: {unique_id}")

            # Redirect to a safe page (e.g., a "You've been phished!" education page)
            # You can create a static HTML page or another Flask route for this.
            # For simplicity, redirect to Google.
            return redirect("https://www.google.com/search?q=phishing+awareness+training", code=302)
        else:
            # If unique_id is not found, it might be an invalid link or direct access
            abort(404)

    @app.route('/reports')
    def reports():
        campaigns = Campaign.query.all()
        # Fetch click data
        click_data = db.session.query(
            Campaign.name,
            Employee.name,
            Employee.email,
            Click.clicked_at,
            Click.ip_address
        ).join(Click, Click.campaign_id == Campaign.id)\
        .join(Employee, Click.employee_id == Employee.id)\
        .order_by(Click.clicked_at.desc()).all()

        # Calculate campaign summaries
        campaign_summaries = []
        for campaign in campaigns:
            total_sent = db.session.query(CampaignEmployee).filter_by(campaign_id=campaign.id).count()
            total_clicks = db.session.query(Click).filter_by(campaign_id=campaign.id).count()
            click_rate = (total_clicks / total_sent * 100) if total_sent > 0 else 0
            campaign_summaries.append({
                'id': campaign.id,
                'name': campaign.name,
                'total_sent': total_sent,
                'total_clicks': total_clicks,
                'click_rate': f"{click_rate:.2f}%"
            })

        # Suggestions for improving awareness
        suggestions = []
        if any(c['total_clicks'] > 0 for c in campaign_summaries):
            suggestions.append("Educate employees on common phishing red flags: suspicious senders, urgent language, generic greetings, and unusual links.")
            suggestions.append("Conduct regular, varied phishing simulations to keep employees vigilant.")
            suggestions.append("Provide immediate feedback and training to employees who click on phishing links.")
            suggestions.append("Implement multi-factor authentication (MFA) to mitigate account compromise even if credentials are stolen.")
            suggestions.append("Remind employees to always verify requests for sensitive information or actions through an alternative, trusted channel (e.g., phone call).")

        return render_template('reports.html', campaign_summaries=campaign_summaries, click_data=click_data, suggestions=suggestions)

    # Route to view campaign details and its recipients
    @app.route('/campaigns/<int:campaign_id>/view')
    def view_campaign(campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        # Eager load campaign_employees to avoid N+1 queries in template
        campaign_employees = db.session.query(CampaignEmployee)\
                                       .filter_by(campaign_id=campaign_id)\
                                       .join(Employee)\
                                       .order_by(Employee.name)\
                                       .all()
        return render_template('view_campaign.html', campaign=campaign, campaign_employees=campaign_employees)

    # Route to remove an employee from a specific campaign
    @app.route('/campaigns/<int:campaign_id>/remove_employee/<int:employee_id>', methods=['POST'])
    def remove_employee_from_campaign(campaign_id, employee_id):
        campaign_employee = CampaignEmployee.query.filter_by(
            campaign_id=campaign_id,
            employee_id=employee_id
        ).first_or_404()

        try:
            db.session.delete(campaign_employee)
            db.session.commit()
            flash(f'Employee "{campaign_employee.employee.name}" removed from campaign "{campaign_employee.campaign.name}" successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error removing employee from campaign: {e}', 'danger')
        return redirect(url_for('view_campaign', campaign_id=campaign_id))

    # Route to delete an entire campaign
    @app.route('/campaigns/<int:campaign_id>/delete', methods=['POST'])
    def delete_campaign(campaign_id):
        campaign = Campaign.query.get_or_404(campaign_id)
        try:
            db.session.delete(campaign)
            db.session.commit()
            flash(f'Campaign "{campaign.name}" and all its associated data deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting campaign: {e}', 'danger')
        return redirect(url_for('index'))


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)