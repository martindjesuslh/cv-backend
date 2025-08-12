from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Any
from app.modules.browser.models import BrowserTask, BrowserAction, ActionType
import time


class _BrowserController:
    def __init__(self):
        self.driver = None

    def execute_task(self, task: BrowserTask) -> Dict[str, Any]:
        try:
            self._setup_driver(task.headless)
            self.driver.get(task.url)

            if task.cookies:
                self._add_cookies_and_refresh(task.cookies)

            self._execute_actions(task.actions)

            response = self._success_response(self.driver.page_source)

            return response

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_actions(self, actions: List[BrowserAction]):
        for action in actions:
            self._execute_single_action(action)

    def _execute_single_action(self, action: BrowserAction):
        if not self.driver:
            raise Exception("No active session")

        wait = WebDriverWait(self.driver, action.timeout)

        if action.type == ActionType.CLICK and action.selector:
            element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, action.selector))
            )
            element.click()
        elif action.type == ActionType.WAIT and action.wait_time:
            time.sleep(action.wait_time)

    def _setup_driver(self, headless: bool):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    def _add_cookies_and_refresh(self, cookies: Dict[str, str]):
        for name, value in cookies.items():
            self.driver.add_cookie({"name": name, "value": value})

        self.driver.refresh()

    def _success_response(self, page_source: str = "") -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Actions completed successfully",
            "session_active": True,
            "url": self.driver.current_url if self.driver else None,
            "page_source": page_source,
        }

    def _error_response(self, error_message: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": error_message,
            "session_active": bool(self.driver),
        }


browser_controller = _BrowserController()
