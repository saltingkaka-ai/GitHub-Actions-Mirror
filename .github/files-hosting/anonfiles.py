"""Handler untuk AnonFiles dan variannya."""

import re
import json
from .base import BaseHostingHandler


class AnonFilesHandler(BaseHostingHandler):
    """Handler untuk anonfiles.com, anonfile.com, dll."""
    
    HOSTING_NAME = "anonfiles"
    DOMAINS = ["anonfiles.com", "anonfile.com", "bayfiles.com", "letsupload.cc"]
    
    def get_direct_link(self, url: str) -> str:
        """
        Parse AnonFiles URL untuk mendapatkan direct link.
        Contoh: https://anonfiles.com/xxxxx/filename.ext
        """
        # Ambil page content
        html = self._get_page_content(url)
        
        # Cari direct link di meta tag atau download button
        # Method 1: Cari di meta property
        patterns = [
            r'id="download-url".*?href="(https://[^"]+)"',
            r'class=".*?(download-btn|btn-primary).*?href="(https://[^"]+)"',
            r'"url":"(https://cdn-[^"]+)"',
            r'href="(https://cdn-\d+\.anonfiles\.com/[^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                # Ambil group terakhir yang match
                groups = [g for g in match.groups() if g and g.startswith('http')]
                if groups:
                    return groups[-1]
        
        # Method 2: Parse JSON embedded
        try:
            json_match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?});', html)
            if json_match:
                data = json.loads(json_match.group(1))
                # Navigate structure untuk cari download URL
                if 'file' in data and 'url' in data['file']:
                    return data['file']['url']['full']
        except (json.JSONDecodeError, KeyError):
            pass
        
        raise ValueError("Tidak dapat menemukan direct link di page AnonFiles")