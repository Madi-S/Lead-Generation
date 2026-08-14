"""Email templates with placeholder substitution.

This module provides email template management with support for
dynamic placeholder replacement using lead data.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EmailTemplate:
    """Email template with placeholder substitution.

    Placeholders use Python's str.format() syntax: {placeholder_name}
    Common placeholders: {title}, {address}, {phone}, {website}

    Attributes:
        subject: Email subject line with optional placeholders
        body: Email body with optional placeholders

    Example:
        >>> template = EmailTemplate(
        ...     subject="Hello {title}!",
        ...     body="We found your business at {address}."
        ... )
        >>> subject, body = template.render({"title": "Joe's Pizza", "address": "123 Main St"})
        >>> subject
        "Hello Joe's Pizza!"
    """

    subject: str
    body: str

    def render(self, lead: dict[str, str]) -> tuple[str, str]:
        """Render template with lead data.

        Args:
            lead: Dictionary with lead data for placeholder substitution

        Returns:
            Tuple of (rendered_subject, rendered_body)

        Example:
            >>> template = EmailTemplate("Hi {title}", "Your address: {address}")
            >>> template.render({"title": "Acme Inc", "address": "456 Oak Ave"})
            ("Hi Acme Inc", "Your address: 456 Oak Ave")
        """
        rendered_subject = self._safe_format(self.subject, lead)
        rendered_body = self._safe_format(self.body, lead)
        return rendered_subject, rendered_body

    def _safe_format(self, template: str, data: dict[str, str]) -> str:
        """Safely format a template string, leaving missing placeholders intact.

        Args:
            template: Template string with {placeholder} syntax
            data: Dictionary of placeholder values

        Returns:
            Formatted string with available placeholders replaced
        """
        try:
            return template.format_map(_SafeDict(data))
        except (KeyError, ValueError):
            return template


class _SafeDict(dict):  # type: ignore[type-arg]
    """Dict subclass that returns placeholder for missing keys."""

    def __missing__(self, key: str) -> str:
        return f"{{{key}}}"


# Pre-built templates for common use cases
DEFAULT_COLD_EMAIL = EmailTemplate(
    subject="Partnership Opportunity - {title}",
    body="""Dear {title},

I came across your business and was impressed by what you do.

I believe we could explore some mutually beneficial opportunities together.

Would you be available for a brief call this week?

Best regards,
[Your Name]

P.S. I found your business at {address}.
""",
)

FOLLOW_UP_TEMPLATE = EmailTemplate(
    subject="Following up - {title}",
    body="""Hi {title},

I wanted to follow up on my previous email.

I understand you're busy, but I believe this could be valuable for your business.

Let me know if you'd like to schedule a quick call.

Best,
[Your Name]
""",
)
