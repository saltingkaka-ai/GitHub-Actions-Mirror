"""Handler untuk MediaFire."""

import re
from .base import BaseHostingHandler


class MediaFireHandler(BaseHostingHandler):
    """Handler untuk mediafire.com."""
    
    HOSTING_NAME = "mediafire"
    DOMAINS = ["mediafire.com", "www.mediafire.com"]
    
    def get_direct_link(self, url: str) -> str:
        """Parse MediaFire download page."""
        html = self._get_page_content(url)
        
        # MediaFire biasanya expose direct link di meta atau script
        patterns = [
            r'href="(https://download\d+\.mediafire\.com/[^"]+)"',
            r'"(https://[^"]+\.mediafire\.com/[^"]+)"\s*download',
            r'downloadButton.*?href="([^"]+)"',
            r'kNO\s*=\s*"([^"]+)"',  # Variable obfuscation
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                direct_url = match.group(1)
                if direct_url.startswith('http'):
                    return direct_url
        
        raise ValueError("Tidak dapat menemukan direct link MediaFire")