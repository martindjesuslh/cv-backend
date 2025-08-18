from app.core.responses_builder import internal_error
from app.core.responses_builder import ok
from app.modules.scraper.service import scraper_client
from app.modules.browser.service import browser_client, BrowserTask, BrowserAction, ActionType  # fmt:skip
from .schemas import RequestBody, Pages
from app.utils.parse import ParseData
from app.core.config.settings import settings
from app.core.constants import SelectorsIndeed
from typing import Any, Dict, List
from asyncio import gather


class _CvHandler:
    def __init__(self):
        self.cookie = ParseData.parse_http_cookie(settings.DEFAULT_COOKIE)

    def test(data: Any):
        return ok()

    async def create_cv(self, payload: RequestBody) -> Dict[str, Any]:
        data = ParseData.pydantic_to_dict(payload)
        try:
            pages = await self._process_pages(data["profiles"])

            return ok()

        except Exception as e:
            return internal_error(message="La cagaste hijo", details=str(e))

    async def _process_pages(self, list: List[str]) -> List[Pages]:
        if len(list) == 0:
            raise ValueError("List empty")

        tasks: List[BrowserTask] = [self._create_task(url) for url in list]

        pages = await gather(*[browser_client.execute_task(task) for task in tasks])

        result: List[Pages] = []

        for page in pages:
            if page["success"]:
                result.append(Pages(url=page["url"], page_source=page["page_source"]))
            else:
                result.append(Pages(url=page["url"], pages_source=page["error"]))

        print(result)

        return ok(data=result)

    def _create_task(self, url: str) -> BrowserTask:
        return BrowserTask(
            url=url, headless=True, cookies=self.cookie, actions=[self._create_action()]
        )

    def _create_action(self) -> BrowserAction:
        return BrowserAction(
            type=ActionType.CLICK,
            selector=SelectorsIndeed.BUTTON_SKILLS.value,
        )


cv_handler = _CvHandler()
