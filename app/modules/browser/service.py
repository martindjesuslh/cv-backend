from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List, Any, Optional, ClassVar
from app.modules.browser.models import BrowserTask, BrowserAction, ActionType
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
import time
import atexit


class _BrowserClient:
    _instance: ClassVar[Optional["_BrowserClient"]] = None
    _initialized: ClassVar[bool] = False

    def __new__(cls) -> "_BrowserClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not _BrowserClient._initialized:
            self.max_drivers = 3
            self.semaphore = ThreadPoolExecutor(max_workers=self.max_drivers)
            self.driver: Optional[webdriver.Chrome] = None
            self._current_url: Optional[str] = None

            _BrowserClient._initialized = True

            atexit.register(self._cleanup_driver)

    async def execute_task(self, task: BrowserTask) -> Dict[str, Any]:
        try:
            await get_event_loop().run_in_executor(
                self.semaphore, self._ensure_driver, task.headless
            )

            if self._current_url != task.url:
                await get_event_loop().run_in_executor(
                    self.semaphore, self._navigate_to_url, task.url
                )

            if task.cookies:
                await get_event_loop().run_in_executor(
                    self.semaphore, self._add_cookies_and_refresh, task.cookies
                )
            page_source = await get_event_loop().run_in_executor(
                self.semaphore, self._get_page_source
            )

            return self._success_response(page_source)

        except Exception as e:
            return self._error_response(str(e))

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

    def _navigate_to_url(self, url: str):
        self.driver.get(url)
        self._current_url = url

    def _get_page_source(self) -> str:
        if not self.driver:
            raise Exception("No active session")
        return self.driver.page_source

    def _ensure_driver(self, headless: bool):
        if self.driver is None:
            self._setup_driver(headless)

    def _setup_driver(self, headless: bool):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-logging")
        options.add_argument("--silent")

        self.driver = webdriver.Chrome(options=options)

    def _cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                self._current_url = None
        if hasattr(self, "semaphore"):
            self.semaphore.shutdown(wait=True)

    def _add_cookies_and_refresh(self, cookies: Dict[str, str]):
        for name, value in cookies.items():
            self.driver.add_cookie({"name": name, "value": value})

        self.driver.refresh()

        self._current_url = self.driver.current_url

    def _success_response(self, page_source: str = "") -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Actions completed successfully",
            "session_active": bool(self.driver),
            "url": self.driver.current_url if self.driver else None,
            "page_source": page_source,
        }

    def _error_response(self, error_message: str) -> Dict[str, Any]:
        return {
            "success": False,
            "error": error_message,
            "session_active": bool(self.driver),
        }

    def close_browser(self):
        self._cleanup_driver()


browser_client = _BrowserClient()
