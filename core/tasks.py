"""
Celery tasks for core functionality.
"""

from celery import shared_task
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)


@shared_task
def cleanup_expired_sessions():
    """Clean up expired sessions from the database."""
    try:
        call_command('clearsessions')
        logger.info("Successfully cleaned up expired sessions")
        return "Sessions cleaned"
    except Exception as e:
        logger.error(f"Error cleaning sessions: {str(e)}")
        raise


@shared_task
def send_email_notification(subject, message, recipient_list):
    """
    Send email notification asynchronously.
    
    Args:
        subject: Email subject
        message: Email message
        recipient_list: List of recipient email addresses
    """
    from django.core.mail import send_mail
    from django.conf import settings
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_list}")
        return f"Email sent to {len(recipient_list)} recipients"
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise


@shared_task
def generate_report(report_type, params):
    """
    Generate various types of reports asynchronously.
    
    Args:
        report_type: Type of report to generate
        params: Parameters for report generation
    """
    logger.info(f"Generating {report_type} report with params: {params}")
    
    # Implement report generation logic here
    # This is a placeholder for future implementation
    
    return f"Report {report_type} generated successfully"
