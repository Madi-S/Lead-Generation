"""Gmail SMTP email sender.

This module provides async email sending functionality using Gmail SMTP.
Supports single and bulk email sending with configurable templates.
"""

from __future__ import annotations

import asyncio
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_lead_generation.src.email.config import SMTPConfig
    from py_lead_generation.src.email.templates import EmailTemplate


# Email validation regex pattern
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    """Validate an email address format.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise

    Example:
        >>> is_valid_email("test@example.com")
        True
        >>> is_valid_email("invalid-email")
        False
    """
    return bool(EMAIL_PATTERN.match(email))


class GmailSMTPSender:
    """Async email sender using Gmail SMTP.

    This class provides methods for sending single and bulk emails
    using Gmail's SMTP server with app password authentication.

    Attributes:
        config: SMTP configuration with credentials

    Example:
        >>> config = SMTPConfig.from_env()
        >>> sender = GmailSMTPSender(config)
        >>> await sender.send("recipient@example.com", "Subject", "Body")
        True
    """

    def __init__(self, config: SMTPConfig) -> None:
        """Initialize Gmail SMTP sender.

        Args:
            config: SMTP configuration with Gmail credentials
        """
        self.config = config

    async def send(self, to: str, subject: str, body: str) -> bool:
        """Send a single email asynchronously.

        Args:
            to: Recipient email address
            subject: Email subject line
            body: Email body content (plain text)

        Returns:
            True if email was sent successfully, False otherwise

        Raises:
            ValueError: If recipient email is invalid
        """
        if not is_valid_email(to):
            raise ValueError(f"Invalid email address: {to}")

        # Run blocking SMTP operation in thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self._send_sync, to, subject, body
        )

    def _send_sync(self, to: str, subject: str, body: str) -> bool:
        """Send email synchronously (internal method).

        Args:
            to: Recipient email address
            subject: Email subject line
            body: Email body content

        Returns:
            True if successful, False otherwise
        """
        try:
            msg = MIMEMultipart()
            msg["From"] = self.config.email
            msg["To"] = to
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.config.host, self.config.port) as server:
                if self.config.use_tls:
                    server.starttls()
                server.login(self.config.email, self.config.password)
                server.send_message(msg)

            return True
        except smtplib.SMTPException as e:
            print(f"SMTP error sending to {to}: {e}")
            return False
        except Exception as e:
            print(f"Error sending email to {to}: {e}")
            return False

    async def send_bulk(
        self,
        leads: list[dict[str, str]],
        template: EmailTemplate,
        email_field: str = "email",
        delay_seconds: float = 1.0,
    ) -> list[bool]:
        """Send bulk emails to multiple leads.

        Args:
            leads: List of lead dictionaries with email and data
            template: Email template for rendering
            email_field: Key in lead dict containing email address
            delay_seconds: Delay between emails to avoid rate limits

        Returns:
            List of success/failure booleans for each lead

        Example:
            >>> leads = [
            ...     {"title": "Business A", "email": "a@example.com"},
            ...     {"title": "Business B", "email": "b@example.com"},
            ... ]
            >>> results = await sender.send_bulk(leads, template)
            >>> results
            [True, True]
        """
        results: list[bool] = []

        for lead in leads:
            email = lead.get(email_field, "")

            if not email or not is_valid_email(email):
                results.append(False)
                continue

            subject, body = template.render(lead)
            success = await self.send(email, subject, body)
            results.append(success)

            # Delay to avoid rate limiting
            if delay_seconds > 0:
                await asyncio.sleep(delay_seconds)

        return results
