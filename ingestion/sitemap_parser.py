import requests
import xml.etree.ElementTree as ET #used element tree for efficiency, used lxml in different project
from utils.logger import info, error
import aiohttp
import asyncio

class SitemapParser:
    def __init__(self, sitemap_url):
        self.url = sitemap_url
    
    async def get_pages(self):
        """
            parse the sitemap and return the pages
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as resp:
                    content = await resp.text()
            root = ET.fromstring(content)
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'} #defined to get the namespace of the sitemap
            pages = []
            for url_elem in root.findall('.//ns:url', namespace):
                loc_elem = url_elem.find('ns:loc', namespace)
                if loc_elem is not None:
                    url = loc_elem.text
                    pages.append({'url': url, 'content': url})
            return pages
        except Exception as e:
            error(f"Error parsing sitemap: {e}")
            return []
