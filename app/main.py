from fastapi import FastAPI
from bs4 import BeautifulSoup
from app.core.responses import ok, bad_request, not_found, internal_error
from app.modules.scraper.models import ScrapedData, ScrapeMethod
from app.modules.browser.models import BrowserTask, BrowserAction, ActionType
from app.modules.browser.service import browser_controller
import time

app = FastAPI()

url_test = "http://localhost:4200"

@app.get("/browser")
async def browser_with_scrape():
    try:
        # Ejecutamos las acciones en el browser
        task = BrowserTask(
            url=url_test,
            actions=[
                BrowserAction(
                    type=ActionType.CLICK, 
                    selector="#test-button", 
                    timeout=10
                ),
                BrowserAction(
                    type=ActionType.WAIT, 
                    wait_time=2
                )
            ],
            headless=True,
            cookies=None,
        )
        
        browser_result = browser_controller.execute_task(task)
        
        if not browser_result.get("success"):
            return bad_request(message="Error en browser", details=browser_result.get("error"))
        
        # Procesamos el page_source directamente con BeautifulSoup
        page_source = browser_result.get("page_source", "")
        
        if not page_source:
            return bad_request(message="No se obtuvo page_source del browser")
        
        # Scraping directo del page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Buscamos el div con la clase lorem
        lorem_div = soup.select_one('.lorem')
        lorem_text = lorem_div.get_text(strip=True) if lorem_div else None
        
        # Creamos un resultado de scraping manual
        scrape_result = ScrapedData(
            url=url_test,
            data={
                "lorem_content": lorem_text,
                "lorem_found": lorem_text is not None
            },
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            method_used=ScrapeMethod.BEAUTIFUL_SOUP
        )
        
        return ok(data={
            "scrape_result": scrape_result.model_dump()
        }, message="Acciones completadas y contenido extraído")

    except Exception as e:
        return internal_error(details=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)