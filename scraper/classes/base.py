from bs4 import BeautifulSoup
import urllib, urllib.request
import os, os.path, time

class BaseScraper:

    """
    The initializing method. Notice that the URL is passed externally. That was done beause URL is also contained in the DB, and it would be better to have a single point of change for future.
    """
    def __init__ (self, dirname='data', filename=None, url=None):
        self.dirname  = dirname # The directory where all files reside ('./data')
        self.filename = filename # File containing daily cached HTML
        self.htmlFile = self.dirname + os.sep + self.filename
        self.url      = url

    """
    Returns a summary of the website this class represents. The summary is simply HTML code of an unordered list, which can be appended by the calling class to form the mailer HTML.
    """
    def getSummary(self):
        self.makeCacheFile()
        
        # Read the summary of HTML and return it
        with open(self.htmlFile) as f:
            return f.read()

    """
    Check for cache file. If it doesn't exist, create one
    """
    def makeCacheFile(self):
        make_new_file = False
        if os.path.exists(self.htmlFile):
            # We need to make sure that the cache file was created today only
            last_modified = int(os.path.getmtime(self.htmlFile))
            current_time = int(time.time())

            if (current_time - last_modified >= 24 * 3600 ):
                make_new_file = True
        else:
                make_new_file = True
        
        if make_new_file:
            f = open(self.htmlFile, 'w')
            f.write(self.extractSummaryFromUrl())


    """
    Extracts HTML summary from the URL based on website-specific patterns
    """
    def extractSummaryFromUrl(self):
        raise NotImplementedError # Force child classes to define their own URLs