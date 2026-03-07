# -*- coding: utf-8 -*-
# **************************************
# @Time : 2024/12/6 12:36
# @Author : Olivia
# Desc:
# **************************************
import time
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from base.po.base_page import BasePage



class WebBasePage(BasePage):
    def __init__(self, driver: WebDriver):
        """
        Note: Must add this construction. If not, seem the one in BasePage isn't used either

        :param driver:
        """
        self.driver = driver


class AdHandlerMixin:
    """Mixin for handling advertisements and popups - available on all pages"""

    # Common ad/popup close button selectors
    AD_CLOSE_BUTTONS = [
        (By.XPATH, "//div[@id='dismiss-button']"),  # Google AdSense dismiss
        (By.XPATH, "//button[contains(@class, 'close')]"),  # Generic close button
        (By.XPATH, "//button[contains(@aria-label, 'Close')]"),  # Aria labeled close
        (By.XPATH, "//button[contains(@aria-label, 'close')]"),
        (By.XPATH, "//a[contains(@class, 'close')]"),  # Close link
        (By.XPATH, "//div[contains(@class, 'modal-close')]"),  # Modal close
        (By.XPATH, "//span[contains(@class, 'close')]"),  # Close span
        (By.ID, "closeBtn"),  # Common close button ID
        (By.CLASS_NAME, "ad-close"),  # Ad close class
        (By.XPATH, "//div[@class='ns-p6ow-e-23']"),  # Google ad specific
        (By.XPATH, "//iframe[contains(@id, 'google_ads')]"),  # Ad iframe
    ]

    # Common modal/overlay selectors
    MODAL_OVERLAYS = [
        (By.CLASS_NAME, "modal-backdrop"),
        (By.CLASS_NAME, "overlay"),
        (By.XPATH, "//div[contains(@class, 'modal') and contains(@style, 'display: block')]"),
    ]

    def close_ad_if_present(self, wait_time=2):
        """
        Try to close any advertisements or popups that appear

        Args:
            wait_time: Time to wait for ads to appear (seconds)

        Returns:
            bool: True if ad was closed, False if no ad found
        """
        time.sleep(wait_time)  # Wait for ads to load

        # Try each close button selector
        for locator in self.AD_CLOSE_BUTTONS:
            try:
                close_btn = WebDriverWait(self.driver, 1).until(
                    EC.element_to_be_clickable(locator)
                )
                close_btn.click()
                print(f"✓ Closed ad using locator: {locator}")
                time.sleep(0.5)
                return True
            except (TimeoutException, NoSuchElementException):
                continue

        return False

    def close_all_ads(self, max_attempts=3):
        """
        Aggressively try to close all ads/popups

        Args:
            max_attempts: Maximum number of attempts to close ads

        Returns:
            int: Number of ads closed
        """
        ads_closed = 0

        for attempt in range(max_attempts):
            if self.close_ad_if_present(wait_time=1):
                ads_closed += 1
                print(f"Closed ad #{ads_closed}")
            else:
                break  # No more ads found

        return ads_closed

    def handle_google_adsense(self):
        """Handle Google AdSense specifically"""
        try:
            # Switch to ad iframe if present
            ad_iframes = self.driver.find_elements(By.XPATH,
                                                   "//iframe[contains(@id, 'google_ads') or contains(@id, 'aswift')]")

            for iframe in ad_iframes:
                try:
                    self.driver.switch_to.frame(iframe)

                    # Try to find and click close button inside iframe
                    close_buttons = [
                        (By.ID, "dismiss-button"),
                        (By.XPATH, "//div[@aria-label='Close ad']"),
                        (By.XPATH, "//button[contains(@aria-label, 'Close')]"),
                    ]

                    for locator in close_buttons:
                        try:
                            close_btn = WebDriverWait(self.driver, 2).until(
                                EC.element_to_be_clickable(locator)
                            )
                            close_btn.click()
                            print("✓ Closed Google AdSense ad")
                            self.driver.switch_to.default_content()
                            return True
                        except:
                            continue

                    self.driver.switch_to.default_content()
                except:
                    self.driver.switch_to.default_content()
                    continue
        except Exception as e:
            self.driver.switch_to.default_content()

        return False

    def dismiss_modal_overlay(self):
        """Dismiss modal overlays by clicking outside or pressing ESC"""
        try:
            # Try pressing ESC key
            from selenium.webdriver.common.keys import Keys
            body = self.driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            time.sleep(0.5)
            print("✓ Dismissed modal with ESC key")
            return True
        except Exception as e:
            pass

        # Try clicking on overlay backdrop
        for locator in self.MODAL_OVERLAYS:
            try:
                overlay = self.driver.find_element(*locator)
                overlay.click()
                print("✓ Dismissed modal by clicking overlay")
                return True
            except:
                continue

        return False

    def wait_and_handle_ads(self, wait_time=3):
        """
        Wait for page to load and handle any ads that appear

        Args:
            wait_time: Time to wait before checking for ads
        """
        time.sleep(wait_time)

        # Try multiple ad handling strategies
        self.close_all_ads(max_attempts=2)
        self.handle_google_adsense()
        self.dismiss_modal_overlay()

        print("✓ Ad handling complete")

    def execute_with_ad_handling(self, action_func, *args, **kwargs):
        """
        Execute an action with automatic ad handling before and after

        Args:
            action_func: Function to execute
            *args, **kwargs: Arguments for the function

        Returns:
            Result of action_func
        """
        # Handle ads before action
        self.close_ad_if_present(wait_time=1)

        # Execute the action
        result = action_func(*args, **kwargs)

        # Handle ads after action
        self.close_ad_if_present(wait_time=1)

        return result

    def click_with_ad_retry(self, locator, max_retries=3):
        """
        Click an element with retry logic in case ads block the element

        Args:
            locator: Element locator tuple
            max_retries: Maximum number of retry attempts
        """
        for attempt in range(max_retries):
            try:
                # Try to close any ads first
                if attempt > 0:
                    self.close_ad_if_present(wait_time=1)

                # Try to click
                element = self.wait.until(EC.element_to_be_clickable(locator))

                # Scroll to element to ensure it's visible
                self.scroll_to_element(element)
                time.sleep(0.5)

                element.click()
                return True

            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Click attempt {attempt + 1} failed, retrying after closing ads...")
                    self.close_all_ads(max_attempts=2)
                    time.sleep(1)
                else:
                    raise Exception(f"Failed to click element after {max_retries} attempts: {e}")

        return False