"""Handler untuk ZippyShare."""

import re
from urllib.parse import urljoin
from .base import BaseHostingHandler


class ZippyShareHandler(BaseHostingHandler):
    """Handler untuk zippyshare.com."""
    
    HOSTING_NAME = "zippyshare"
    DOMAINS = ["zippyshare.com", "www.zippyshare.com"]
    
    def get_direct_link(self, url: str) -> str:
        """
        Parse ZippyShare URL - butuh evaluasi JavaScript sederhana.
        ZippyShare menggunakan obfuscation JS untuk generate link.
        """
        html = self._get_page_content(url)
        
        # Cari script yang mengandung logic download
        # ZippyShare biasanya punya pattern seperti:
        # document.getElementById('dlbutton').href = "...";
        
        # Pattern umum ZippyShare
        patterns = [
            r'dlbutton.*?href\s*=\s*"([^"]+)"',
            r'href\s*=\s*"(/d/[^"]+)"',
            r'"(/d/[^"]+)"\s*\+\s*[^;]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                relative_url = match.group(1)
                # Bersihkan dari escape characters
                relative_url = relative_url.replace('\\', '')
                return urljoin(url, relative_url)
        
        # Jika tidak ketemu, coba extract dari element dlbutton
        dl_match = re.search(r'id="dlbutton".*?href="([^"]+)"', html, re.DOTALL)
        if dl_match:
            return urljoin(url, dl_match.group(1))
        
        raise ValueError("Tidak dapat menemukan direct link ZippyShare")