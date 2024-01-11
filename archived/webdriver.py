import asyncio
import pyppeteer


from fake_useragent import UserAgent
from screeninfo import get_monitors
from pyppeteer import launch
from random import uniform
from time import sleep

from logger_config import get_logger
from bufferization import Buffer

logger = get_logger('webdriver')


class Webdriver:
    _ua = UserAgent()
    _buf = Buffer()
    _monitor = get_monitors()[0]
    _viewport = {'width': _monitor.width, 'height': _monitor.height, }

    async def init_browser(self, hidden=False, language='en-gb'):
        '''
        Initializing browser by opening pages, setting headers and parameters before starting lead generaiton

        :param hidden: Run Webdriver in headless mode
        :param language: Specify Accept-Language header value. English by default. Look up for them here https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
        :return: returns nothing
        '''
        self.browser = await launch(
            ignoreHTTPSErrors=True,
            headless=hidden,
            viewport=None,
            autoclose=True,
            args=['--start-maximized'],
        )
        self._page = (await self.browser.pages())[0]

        await self._page.setUserAgent(self._ua.random)
        await self._page.setViewport(self._viewport)
        await self._page.setExtraHTTPHeaders({'Accept-Language': language})
        await self._page.reload()

        logger.debug('Successfull Websdriver initialization')

    async def _shut_browser(self):
        logger.debug('Shutting down Webdriver in 10 seconds')
        sleep(10)
        await self._page.close()
        await self.browser.close()
        if self._page.isClosed():
            logger.debug('Webdriver has been closed')

    async def _do_retry(self, operation, xpath, dest=None, retries=0):
        if retries == 10:
            raise SystemError(
                'Max 10 retries exceeded when clicking the place')
        try:
            if dest:
                await operation(dest)
            else:
                await operation()
            sleep(uniform(1, 1.5))
            await self._page.waitForXPath(xpath, {'visible': True})
        except pyppeteer.errors.TimeoutError:
            logger.warning('Cannot locate xpath retry #%s', retries + 1)
            await self._do_retry(operation, xpath, dest, retries + 1)
        except:
            logger.error('Exception found when retrying', exc_info=True)

    async def _jump(self, url, xpath):
        try:
            await self._page.goto(url)
            logger.debug('Validating given URL')
            self._page.waitForXPath(xpath, {'visible': True})
        except:
            logger.warning('Webdriver got invalid URL for lead generation')
            await self._shut_browser()
            raise ValueError('Got invalid URL for google maps')
