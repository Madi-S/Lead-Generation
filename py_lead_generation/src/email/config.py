"""SMTP configuration for email outreach.

This module provides configuration management for SMTP email sending,
with support for loading credentials from environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class SMTPConfig:
    """Configuration for SMTP email sending.

    Attributes:
        host: SMTP server hostname
        port: SMTP server port
        email: Sender email address
        password: App password for authentication
        use_tls: Whether to use TLS encryption

    Example:
        >>> config = SMTPConfig.from_env()
        >>> config.host
        'smtp.gmail.com'
    """

    host: str = "smtp.gmail.com"
    port: int = 587
    email: str = ""
    password: str = ""
    use_tls: bool = True

    @classmethod
    def from_env(cls) -> SMTPConfig:
        """Load SMTP configuration from environment variables.

        Environment variables:
            GMAIL_ADDRESS: Sender email address
            GMAIL_APP_PASSWORD: Gmail app password (not regular password)
            SMTP_HOST: SMTP server (default: smtp.gmail.com)
            SMTP_PORT: SMTP port (default: 587)

        Returns:
            SMTPConfig instance with values from environment

        Raises:
            ValueError: If required environment variables are missing
        """
        email = os.environ.get("GMAIL_ADDRESS", "")
        password = os.environ.get("GMAIL_APP_PASSWORD", "")

        if not email or not password:
            raise ValueError(
                "Missing required environment variables: "
                "GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set"
            )

        return cls(
            host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
            port=int(os.environ.get("SMTP_PORT", "587")),
            email=email,
            password=password,
            use_tls=os.environ.get("SMTP_USE_TLS", "true").lower() == "true",
        )

    def validate(self) -> bool:
        """Validate that all required fields are set.

        Returns:
            True if configuration is valid
        """
        return bool(self.host and self.port and self.email and self.password)
