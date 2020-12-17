# async def _evaluate(page, retries=0):
#    if retries > 10:
#        return await page.evaluate('document.body.innerHTML')
#     else:
#        try:
#            return await page.evaluate('document.body.innerHTML')
#        except pyppeteer.errors.NetworkError:
#             await asyncio.sleep(0.5)
#             return await _evaluate(page, retries+1)