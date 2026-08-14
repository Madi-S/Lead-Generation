"""Email outreach module for py-lead-generation.

This module provides Gmail SMTP integration for sending personalized
cold emails to collected leads.

Classes:
    SMTPConfig: Configuration dataclass for SMTP settings
    EmailTemplate: Email template with placeholder substitution
    GmailSMTPSender: Async email sender using Gmail SMTP
"""

from py_lead_generation.src.email.config import SMTPConfig
from py_lead_generation.src.email.sender import GmailSMTPSender
from py_lead_generation.src.email.templates import EmailTemplate

__all__ = ["SMTPConfig", "EmailTemplate", "GmailSMTPSender"]
