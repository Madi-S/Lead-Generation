"""Lead Generation GUI Application.

This module provides a Tkinter-based desktop application for
searching leads and exporting data without using command line.

Usage:
    # As a module
    from py_lead_generation.src.gui import LeadGenerationApp
    app = LeadGenerationApp()
    app.run()

    # From command line
    lead-gen-gui
"""

from __future__ import annotations

import asyncio
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_lead_generation.src.google_maps.engine import GoogleMapsEngine
    from py_lead_generation.src.yelp.engine import YelpEngine


class LeadGenerationApp:
    """Lead Generation GUI Application.

    A Tkinter-based desktop application for searching and exporting leads
    from various sources (Google Maps, Yelp, etc.).

    Attributes:
        root: Main Tkinter window
        entries: Collected lead entries
    """

    def __init__(self) -> None:
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Lead Generation Tool")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        self.entries: list[dict[str, str]] = []
        self._search_in_progress = False

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Search form
        self._setup_search_form(main_frame)

        # Results display
        self._setup_results_display(main_frame)

        # Status bar
        self._setup_status_bar(main_frame)

    def _setup_search_form(self, parent: ttk.Frame) -> None:
        """Set up the search form section."""
        form_frame = ttk.LabelFrame(parent, text="Search Parameters", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        # Query input
        ttk.Label(form_frame, text="Search Query:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.query_var = tk.StringVar(value="restaurants")
        self.query_entry = ttk.Entry(form_frame, textvariable=self.query_var, width=30)
        self.query_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Location input
        ttk.Label(form_frame, text="Location:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.location_var = tk.StringVar(value="Paris")
        self.location_entry = ttk.Entry(
            form_frame, textvariable=self.location_var, width=30
        )
        self.location_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)

        # Source dropdown
        ttk.Label(form_frame, text="Source:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.source_var = tk.StringVar(value="google_maps")
        self.source_combo = ttk.Combobox(
            form_frame,
            textvariable=self.source_var,
            values=["google_maps", "yelp"],
            state="readonly",
            width=27,
        )
        self.source_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=1, column=2, columnspan=2, sticky=tk.E, padx=5, pady=5)

        self.search_btn = ttk.Button(
            button_frame, text="Search", command=self._on_search
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)

        self.export_btn = ttk.Button(
            button_frame, text="Export CSV", command=self._on_export, state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(
            button_frame, text="Clear", command=self._on_clear
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

    def _setup_results_display(self, parent: ttk.Frame) -> None:
        """Set up the results Treeview display."""
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview with scrollbars
        columns = ("title", "address", "phone", "website")
        self.tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", selectmode="extended"
        )

        # Configure columns
        self.tree.heading("title", text="Title")
        self.tree.heading("address", text="Address")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("website", text="Website")

        self.tree.column("title", width=200)
        self.tree.column("address", width=250)
        self.tree.column("phone", width=120)
        self.tree.column("website", width=200)

        # Scrollbars
        vsb = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(
            results_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        vsb.grid(row=0, column=1, sticky=tk.NS)
        hsb.grid(row=1, column=0, sticky=tk.EW)

        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

    def _setup_status_bar(self, parent: ttk.Frame) -> None:
        """Set up the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            status_frame, textvariable=self.status_var, anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(
            status_frame, mode="indeterminate", length=200
        )
        self.progress.pack(side=tk.RIGHT)

    def _on_search(self) -> None:
        """Handle search button click."""
        if self._search_in_progress:
            return

        query = self.query_var.get().strip()
        location = self.location_var.get().strip()
        source = self.source_var.get()

        if not query or not location:
            messagebox.showwarning("Input Required", "Please enter query and location.")
            return

        self._search_in_progress = True
        self.search_btn.configure(state=tk.DISABLED)
        self.status_var.set(f"Searching for '{query}' in '{location}'...")
        self.progress.start(10)

        # Run search in background thread
        thread = threading.Thread(
            target=self._run_search_async, args=(query, location, source)
        )
        thread.daemon = True
        thread.start()

    def _run_search_async(self, query: str, location: str, source: str) -> None:
        """Run the search in a background thread."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if source == "google_maps":
                from py_lead_generation.src.google_maps.engine import GoogleMapsEngine
                engine: GoogleMapsEngine | YelpEngine = GoogleMapsEngine(query, location)
            else:
                from py_lead_generation.src.yelp.engine import YelpEngine
                engine = YelpEngine(query, location)

            loop.run_until_complete(engine.run())
            entries = engine.entries

            self.root.after(0, lambda: self._on_search_complete(entries))

        except Exception as exc:
            error_msg = str(exc)
            self.root.after(0, lambda msg=error_msg: self._on_search_error(msg))  # type: ignore[misc]

    def _on_search_complete(self, entries: list[dict[str, str]]) -> None:
        """Handle search completion on main thread."""
        self._search_in_progress = False
        self.search_btn.configure(state=tk.NORMAL)
        self.progress.stop()

        self.entries.extend(entries)
        self._populate_tree(entries)

        self.status_var.set(f"Found {len(entries)} results. Total: {len(self.entries)}")
        self.export_btn.configure(state=tk.NORMAL if self.entries else tk.DISABLED)

    def _on_search_error(self, error: str) -> None:
        """Handle search error on main thread."""
        self._search_in_progress = False
        self.search_btn.configure(state=tk.NORMAL)
        self.progress.stop()
        self.status_var.set("Search failed")
        messagebox.showerror("Search Error", f"Search failed: {error}")

    def _populate_tree(self, entries: list[dict[str, str]]) -> None:
        """Populate the Treeview with entries."""
        for entry in entries:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    entry.get("Title", "N/A"),
                    entry.get("Address", "N/A"),
                    entry.get("PhoneNumber", "N/A"),
                    entry.get("WebsiteURL", "N/A"),
                ),
            )

    def _on_export(self) -> None:
        """Handle export button click."""
        if not self.entries:
            messagebox.showinfo("No Data", "No leads to export.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="leads.csv",
        )

        if not filename:
            return

        try:
            from py_lead_generation.src.misc.writer import CsvWriter

            field_names = list(self.entries[0].keys())
            writer = CsvWriter(filename, field_names)
            writer.append(self.entries)

            self.status_var.set(f"Exported {len(self.entries)} leads to {filename}")
            messagebox.showinfo("Export Complete", f"Saved {len(self.entries)} leads.")

        except Exception as e:
            messagebox.showerror("Export Error", f"Export failed: {e}")

    def _on_clear(self) -> None:
        """Handle clear button click."""
        self.entries.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.export_btn.configure(state=tk.DISABLED)
        self.status_var.set("Cleared all results")

    def run(self) -> None:
        """Start the GUI application main loop."""
        self.root.mainloop()


def main() -> None:
    """Entry point for lead-gen-gui command."""
    app = LeadGenerationApp()
    app.run()


if __name__ == "__main__":
    main()
