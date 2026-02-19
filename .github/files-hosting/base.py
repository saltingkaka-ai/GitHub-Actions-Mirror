"""
Base class untuk semua file hosting handlers.
Setiap hosting harus inherit dari class ini.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import requests
import os
from pathlib import Path


class BaseHostingHandler(ABC):
    """Base class yang harus diimplementasikan oleh setiap hosting handler."""
    
    # Identifikasi hosting - override di subclass
    HOSTING_NAME = "base"
    DOMAINS = []  # List domain yang dihandle, e.g., ["anonfiles.com", "anonfile.com"]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        })
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
    
    @classmethod
    def can_handle(cls, url: str) -> bool:
        """Cek apakah handler ini bisa menangani URL tersebut."""
        url_lower = url.lower()
        return any(domain in url_lower for domain in cls.DOMAINS)
    
    @abstractmethod
    def get_direct_link(self, url: str) -> str:
        """
        Parse URL dan kembalikan direct download link.
        Must implement di setiap subclass.
        """
        pass
    
    def download(self, url: str, filename: Optional[str] = None, 
                 progress_callback=None) -> Dict[str, Any]:
        """
        Download file dari URL.
        
        Returns:
            Dict dengan keys: success, file_path, file_size, message
        """
        try:
            # Dapatkan direct link
            direct_url = self.get_direct_link(url)
            
            # Download file
            response = self.session.get(direct_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Tentukan filename
            if not filename:
                # Coba ambil dari header
                cd = response.headers.get('content-disposition', '')
                if 'filename=' in cd:
                    filename = cd.split('filename=')[-1].strip('"\'')
                else:
                    # Ambil dari URL
                    filename = os.path.basename(direct_url.split('?')[0]) or 'unknown_file'
            
            file_path = self.download_dir / filename
            
            # Download dengan progress
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': downloaded,
                'hosting': self.HOSTING_NAME,
                'message': f'Berhasil download: {filename}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'file_size': 0,
                'hosting': self.HOSTING_NAME,
                'message': f'Error: {str(e)}'
            }
    
    def _get_page_content(self, url: str) -> str:
        """Helper untuk fetch page content."""
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.text