"""Tests for email module."""


def test_smtp_config_import() -> None:
    """Test that SMTPConfig can be imported."""
    from py_lead_generation.src.email.config import SMTPConfig

    assert SMTPConfig is not None


def test_email_template_import() -> None:
    """Test that EmailTemplate can be imported."""
    from py_lead_generation.src.email.templates import EmailTemplate

    assert EmailTemplate is not None


def test_gmail_sender_import() -> None:
    """Test that GmailSMTPSender can be imported."""
    from py_lead_generation.src.email.sender import GmailSMTPSender

    assert GmailSMTPSender is not None


def test_smtp_config_defaults() -> None:
    """Test SMTPConfig default values."""
    from py_lead_generation.src.email.config import SMTPConfig

    config = SMTPConfig()
    assert config.host == "smtp.gmail.com"
    assert config.port == 587
    assert config.use_tls is True


def test_email_template_render() -> None:
    """Test EmailTemplate placeholder substitution."""
    from py_lead_generation.src.email.templates import EmailTemplate

    template = EmailTemplate(
        subject="Hello {title}!",
        body="Your business at {address} looks great.",
    )
    lead = {"title": "Acme Inc", "address": "123 Main St"}
    subject, body = template.render(lead)

    assert subject == "Hello Acme Inc!"
    assert "123 Main St" in body


def test_email_template_missing_placeholder() -> None:
    """Test EmailTemplate handles missing placeholders gracefully."""
    from py_lead_generation.src.email.templates import EmailTemplate

    template = EmailTemplate(
        subject="Hello {title}!",
        body="Your phone: {phone}",
    )
    lead = {"title": "Test Corp"}  # Missing 'phone'
    subject, body = template.render(lead)

    assert subject == "Hello Test Corp!"
    assert "{phone}" in body  # Placeholder preserved


def test_email_validation() -> None:
    """Test email validation function."""
    from py_lead_generation.src.email.sender import is_valid_email

    assert is_valid_email("test@example.com") is True
    assert is_valid_email("user.name@domain.org") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("@nodomain.com") is False
    assert is_valid_email("") is False
