from playwright.async_api import Browser, Page, BrowserType


class PlaywrightEngineConfig:
    '''
    `PlaywrightEngineConfig`

    Playwright setup configuration parameters

    [EDITABLE] `BROWSER_PARAMS` - chromiun browser parameters configuration from playwright, additional parameters can be set if needed

    [EDITABLE] `PAGE_PARAMS` - browser page parameters configuration from playwright, additional parameters can be set if needed
    '''

    BROWSER_PARAMS = {'headless': False, 'proxy': None, 'slow_mo': 150}
    PAGE_PARAMS = {'java_script_enabled': True, 'bypass_csp': True}

    async def _setup_browser(self) -> None:
        '''
        Sets up the browser by initializing `playwright.chromiun` and `Browser` along with `Page` after
        '''
        chromium: BrowserType = self.playwright.chromium
        self.browser: Browser = await chromium.launch(**self.BROWSER_PARAMS)
        self.page: Page = await self.browser.new_page(**self.PAGE_PARAMS)
