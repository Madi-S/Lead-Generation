import asyncio
import pyppeteer


from fake_useragent import UserAgent
from pyppeteer import launch
from time import sleep

from logger_config import get_logger
from bufferization import Buffer

logger = get_logger('webdriver')


class Webdriver:
    viewport = {'width': 1920, 'height': 1080, 'deviceScaleFactor': 1.0,
                'isMobile': False, 'hasTouch': False, 'isLandscape': False}
    _ua = UserAgent()
    _buf = Buffer()

    async def init_browser(self, headless_status=False, language='en-gb'):
        self.browser = await launch(
            ignoreHTTPSErrors=True,
            headless=headless_status,
            viewport=None,
            autoclose=True,
            args=['--start-maximized'],
        )
        self._page = (await self.browser.pages())[0]

        await self._page.setUserAgent(self._ua.random)
        await self._page.setViewport(self.viewport)
        await self._page.setExtraHTTPHeaders({'Accept-Language': language})
        await self._page.reload()

        logger.debug('Successfull initialization')

    async def _shut_browser(self):
        logger.debug('Shutting down browser in 15 seconds')
        sleep(15)
        await self._page.close()
        await self.browser.close()

    async def _do_retry(self, operation, xpath, dest=None, retries=0):
        if retries == 10:
            raise SystemError(
                'Max 10 retries exceeded when clicking the place')
        try:
            if dest:
                await operation(dest)
            else:
                await operation()
            sleep(1)
            await self._page.waitForXPath(xpath, {'visible': True})
        except pyppeteer.errors.TimeoutError:
            await self._do_retry(operation, xpath, dest, retries + 1)
        except Exception as e:
            print(e)
            raise SystemError('Some shit happened to pyppeteer, fix it')
    
    async def _jump(self, url, xpath):
        try:
            await self._page.goto(url)
            logger.debug('Validating given URL')
            self._page.waitForXPath(xpath, {'visible': True})
        except:
            await self._shut_browser()
            raise ValueError('Got invalid URL for google maps')
