# https://scrapeops.io/app/onboarding

# pip install scrapeops-scrapy

SCRAPEOPS_API_KEY = 'ae96ef6b-04c6-4b08-b790-373820b8f771'
  
EXTENSIONS = {
        'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
        }
  
DOWNLOADER_MIDDLEWARES = {
        'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
        }