"""GUI module for py-lead-generation.

This module provides a Tkinter-based desktop application for
searching leads and exporting data without using command line.

Classes:
    LeadGenerationApp: Main GUI application window
"""

from py_lead_generation.src.gui.app import LeadGenerationApp, main

__all__ = ["LeadGenerationApp", "main"]
