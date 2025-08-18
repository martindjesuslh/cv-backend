from app.core.responses_builder import internal_error
from app.core.responses_builder import ok
from app.modules.scraper.service import ScraperClient
from app.modules.browser.service import (BrowserClient,BrowserTask,BrowserAction,ActionType)  # fmt:skip
from .schemas import RequestBody, Pages
from app.utils.parse import ParseData
from app.core.config.settings import settings
from app.core.constants import SelectorsIndeed
from typing import Any, Dict, List


class _CvHandler:
    def __init__(self):
        self.cookie = ParseData.parse_http_cookie(settings.DEFAULT_COOKIE)

    def test(data: Any):
        return ok()

    def create_cv(self, data: RequestBody) -> Dict[str, Any]:
        try:
            html_content = ""
            return {"success": True}

        except Exception as e:
            return internal_error(message="La cagaste hijo", details=str(e))

    async def _process_pages(list: List[str]) -> List[Pages]:
        if not list:
            raise ValueError("List empty")

        browser_client = BrowserClient()
        result = []

        for url in list:
            await browser_client.execute_task()

    def _create_task(self, url: str) -> BrowserTask:
        return BrowserTask(
            url=url, headless=True, cookies=self.cookie, actions=self._create_action()
        )

    def _create_action() -> BrowserAction:
        return BrowserAction(
            type=ActionType.CLICK,
            selector=SelectorsIndeed.BUTTON_SKILLS.value,
        )


cv_handler = _CvHandler()
