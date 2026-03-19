# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2026/3/8 10:53
desc: 
'''
from dataclasses import dataclass

"""

-----------------
A truly site-agnostic base Page Object.

This class contains ONLY generic Playwright interaction wrappers and
utility helpers that apply to ANY web application. It has zero knowledge
of any specific site's structure, URLs, selectors, or business logic.

All site-specific Page Objects should inherit (directly or indirectly)
from this class.

Inheritance pattern
-------------------
core.BasePage                        # generic Playwright helpers (this file)
    └── projects/<site>/pages/base_page.BasePage   # site-level shared UI (navbar etc.)
            └── projects/<site>/pages/home_page.HomePage  # individual page
"""

import logging
import re
from typing import Optional

from playwright.sync_api import Page, Locator, expect

logger = logging.getLogger(__name__)

# Default timeouts (ms) used when no external config is injected.
_DEFAULT_TIMEOUT = 30_000
_DEFAULT_NAV_TIMEOUT = 60_000


class BasePage():
    """
    Generic base class for all Page Objects across any project.

    Provides a thin, consistent wrapper around Playwright's Page API so
    that every subclass gets the same helpers without duplicating code.

    Use compose instead of inherit from Playwright Page class, to prevent exposing all low-level APIs
    (code should use encapsulated methods instead of calling low-level page.goto(), page.fill(), etc.)

    Args:
        page:    Playwright Page instance.
        timeout: Default action timeout in milliseconds (optional).
                 When omitted, falls back to _DEFAULT_TIMEOUT.
    """

    def __init__(self, page: Page, timeout: int = _DEFAULT_TIMEOUT) -> None:
        self.page = page
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> None:
        """
        Navigate to a URL and wait for the page to reach a ready state.

        Args:
            url:        Full URL to navigate to.
            wait_until: Playwright load state to wait for.
                        One of: 'load', 'domcontentloaded', 'networkidle'.
        """
        logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until=wait_until, timeout=_DEFAULT_NAV_TIMEOUT)

    def get_current_url(self) -> str:
        """Return the browser's current URL."""
        return self.page.url

    def get_page_title(self) -> str:
        """Return the current page's <title> text."""
        return self.page.title()

    def go_back(self) -> None:
        """Navigate back in the browser history."""
        self.page.go_back(timeout=_DEFAULT_NAV_TIMEOUT)

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload(wait_until="domcontentloaded", timeout=_DEFAULT_NAV_TIMEOUT)

    def wait_for_url(self, pattern: str) -> None:
        """
        Wait until the current URL matches a glob or substring pattern.

        Args:
            pattern: A substring to match against the URL (glob-style).
                     E.g. '/dashboard' will match any URL containing '/dashboard'.
        """
        self.page.wait_for_url(f"**{pattern}**", timeout=_DEFAULT_NAV_TIMEOUT)

    # ------------------------------------------------------------------
    # Element Interactions
    # ------------------------------------------------------------------

    def click(self, locator: Locator, force: bool = False) -> None:
        """
        Scroll an element into view and click it.

        Args:
            locator: Playwright Locator for the target element.
            force:   Bypass actionability checks when True (use sparingly).
        """
        locator.scroll_into_view_if_needed(timeout=self.timeout)
        locator.click(timeout=self.timeout, force=force)

    def fill(self, locator: Locator, text: str) -> None:
        """
        Clear an input field and type the given text.

        Args:
            locator: Playwright Locator for the input element.
            text:    Text to enter.
        """
        locator.clear()
        locator.fill(text, timeout=self.timeout)

    def type_text(self, locator: Locator, text: str, delay: int = 0) -> None:
        """
        Type text character by character (useful for fields with JS listeners).

        Args:
            locator: Playwright Locator for the input element.
            text:    Text to type.
            delay:   Delay in milliseconds between keystrokes (default: 0).
        """
        locator.type(text, delay=delay)

    def select_option(self, locator: Locator, value: str) -> None:
        """
        Select an option in a <select> element by its value attribute.

        Args:
            locator: Playwright Locator for the <select> element.
            value:   The option value to select.
        """
        locator.select_option(value=value, timeout=self.timeout)

    def select_option_by_label(self, locator: Locator, label: str) -> None:
        """
        Select an option in a <select> element by its visible label text.

        Args:
            locator: Playwright Locator for the <select> element.
            label:   The visible text of the option to select.
        """
        locator.select_option(label=label, timeout=self.timeout)

    def check(self, locator: Locator) -> None:
        """Check a checkbox or radio button."""
        locator.check(timeout=self.timeout)

    def uncheck(self, locator: Locator) -> None:
        """Uncheck a checkbox."""
        locator.uncheck(timeout=self.timeout)

    def hover(self, locator: Locator) -> None:
        """Hover the mouse over an element."""
        locator.hover(timeout=self.timeout)

    def upload_file(self, locator: Locator, file_path: str) -> None:
        """
        Set a file on a file input element.

        Args:
            locator:   Playwright Locator for the <input type="file"> element.
            file_path: Absolute path to the file to upload.
        """
        locator.set_input_files(file_path)

    # ------------------------------------------------------------------
    # Reading Element State
    # ------------------------------------------------------------------

    def get_text(self, locator: Locator) -> str:
        """
        Return the visible inner text of an element, stripped of whitespace.

        Args:
            locator: Playwright Locator for the element.

        Returns:
            str: The element's text content.
        """
        return locator.inner_text(timeout=self.timeout).strip()

    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Return the value of a specific HTML attribute on an element.

        Args:
            locator:   Playwright Locator for the element.
            attribute: Attribute name, e.g. 'href', 'value', 'data-id'.

        Returns:
            Optional[str]: The attribute value, or None if not present.
        """
        return locator.get_attribute(attribute, timeout=self.timeout)

    def get_input_value(self, locator: Locator) -> str:
        """
        Return the current value of an <input> or <textarea> element.

        Args:
            locator: Playwright Locator for the input element.

        Returns:
            str: The current input value.
        """
        return locator.input_value(timeout=self.timeout)

    def is_visible(self, locator: Locator) -> bool:
        """Return True if the element is currently visible on the page."""
        return locator.is_visible()

    def is_enabled(self, locator: Locator) -> bool:
        """Return True if the element is enabled (not disabled)."""
        return locator.is_enabled()

    def is_checked(self, locator: Locator) -> bool:
        """Return True if a checkbox or radio button is checked."""
        return locator.is_checked()

    def count(self, locator: Locator) -> int:
        """Return the number of elements matching the locator."""
        return locator.count()

    # ------------------------------------------------------------------
    # Waiting
    # ------------------------------------------------------------------

    def wait_for_visible(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Wait until an element becomes visible.

        Args:
            locator: Playwright Locator for the element.
            timeout: Override timeout in milliseconds (uses instance default if omitted).
        """
        locator.wait_for(state="visible", timeout=timeout or self.timeout)

    def wait_for_hidden(self, locator: Locator, timeout: Optional[int] = None) -> None:
        """
        Wait until an element is hidden or detached from the DOM.

        Args:
            locator: Playwright Locator for the element.
            timeout: Override timeout in milliseconds.
        """
        locator.wait_for(state="hidden", timeout=timeout or self.timeout)

    def wait_for_text(self, locator: Locator, text: str) -> None:
        """
        Wait until an element contains the specified text.

        Args:
            locator: Playwright Locator for the element.
            text:    Expected text substring.
        """
        expect(locator).to_contain_text(text, timeout=self.timeout)

    def wait_milliseconds(self, ms: int) -> None:
        """
        Pause execution for a fixed number of milliseconds.

        Use sparingly — prefer explicit waits (wait_for_visible, etc.) over
        fixed sleeps. Acceptable for brief animation waits.

        Args:
            ms: Duration to wait in milliseconds.
        """
        self.page.wait_for_timeout(ms)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------

    def assert_url_contains(self, path: str) -> None:
        """
        Assert that the current URL contains the given path segment.

        Args:
            path: Expected URL substring, e.g. '/login'.
        """
        expect(self.page).to_have_url(re.compile(f".*{re.escape(path)}.*"))

    def assert_title_contains(self, text: str) -> None:
        """
        Assert that the page <title> contains the given text.

        Args:
            text: Expected title substring.
        """
        expect(self.page).to_have_title(re.compile(f".*{re.escape(text)}.*"))

    def assert_visible(self, locator: Locator) -> None:
        """Assert that an element is visible."""
        expect(locator).to_be_visible(timeout=self.timeout)

    def assert_hidden(self, locator: Locator) -> None:
        """Assert that an element is hidden."""
        expect(locator).to_be_hidden(timeout=self.timeout)

    def assert_text_equals(self, locator: Locator, text: str) -> None:
        """Assert that an element's text exactly matches the expected string."""
        expect(locator).to_have_text(text, timeout=self.timeout)

    def assert_text_contains(self, locator: Locator, text: str) -> None:
        """Assert that an element's text contains the expected substring."""
        expect(locator).to_contain_text(text, timeout=self.timeout)

    def assert_enabled(self, locator: Locator) -> None:
        """Assert that an element is enabled."""
        expect(locator).to_be_enabled(timeout=self.timeout)

    def assert_checked(self, locator: Locator) -> None:
        """Assert that a checkbox or radio button is checked."""
        expect(locator).to_be_checked(timeout=self.timeout)

    # ------------------------------------------------------------------
    # Scrolling
    # ------------------------------------------------------------------

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_into_view(self, locator: Locator) -> None:
        """
        Scroll a specific element into the visible viewport.

        Args:
            locator: Playwright Locator for the target element.
        """
        locator.scroll_into_view_if_needed(timeout=self.timeout)

    # ------------------------------------------------------------------
    # Dialog / Alert Handling
    # ------------------------------------------------------------------

    def accept_dialog(self) -> None:
        """Register a one-time handler to accept the next browser dialog."""
        self.page.once("dialog", lambda dialog: dialog.accept())

    def dismiss_dialog(self) -> None:
        """Register a one-time handler to dismiss the next browser dialog."""
        self.page.once("dialog", lambda dialog: dialog.dismiss())

    # ------------------------------------------------------------------
    # JavaScript
    # ------------------------------------------------------------------

    def execute_script(self, script: str, *args) -> any:
        """
        Execute arbitrary JavaScript in the page context.

        Args:
            script: JavaScript expression or function body.
            *args:  Arguments passed to the script.

        Returns:
            The return value of the JavaScript expression.
        """
        return self.page.evaluate(script, *args)

    # ------------------------------------------------------------------
    # Screenshot
    # ------------------------------------------------------------------


@dataclass
class Timeouts:
    """Playwright timeout settings in milliseconds."""
    default: int = 30_000       # General action timeout
    navigation: int = 60_000    # Page navigation timeout
    element: int = 10_000       # Element visibility/clickability
    animation: int = 2_000      # Wait for CSS animations