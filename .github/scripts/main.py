#!/usr/bin/env python3
"""
File Mirror Main Script
=======================

Script utama untuk mendeteksi tipe hosting dan mendistribusikan
ke handler yang sesuai.

Usage:
    python main.py <url> [filename]
    python main.py "https://anonfiles.com/xxxxx/file.zip" "myfile.zip"
"""

import sys
import os
import importlib
import pkgutil
from pathlib import Path
from typing import Optional, List, Type
from urllib.parse import urlparse

# Add files-hosting to path
sys.path.insert(0, str(Path(__file__).parent))

from files-hosting.base import BaseHostingHandler


class MirrorDispatcher:
    """Dispatcher utama yang mengelola semua hosting handlers."""
    
    def __init__(self):
        self.handlers: List[Type[BaseHostingHandler]] = []
        self._load_handlers()
    
    def _load_handlers(self):
        """Dynamically load semua handler dari folder files-hosting."""
        import files-hosting
        
        # Scan semua module di files-hosting
        for importer, modname, ispkg in pkgutil.iter_modules(files-hosting.__path__):
            if modname.startswith('_') or modname == 'base':
                continue
            
            try:
                module = importlib.import_module(f'files-hosting.{modname}')
                
                # Cari class yang inherit dari BaseHostingHandler
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        issubclass(attr, BaseHostingHandler) and 
                        attr is not BaseHostingHandler):
                        self.handlers.append(attr)
                        print(f"✓ Loaded handler: {attr.HOSTING_NAME}")
                        
            except Exception as e:
                print(f"✗ Failed to load {modname}: {e}")
    
    def detect_hosting(self, url: str) -> Optional[Type[BaseHostingHandler]]:
        """
        Deteksi hosting berdasarkan URL.
        Returns handler class atau None jika tidak ada yang match.
        """
        # Cek direct link terlebih dahulu (bukan file hosting)
        if self._is_direct_link(url):
            return None  # Akan gunakan direct download
        
        # Cek setiap handler
        for handler_class in self.handlers:
            if handler_class.can_handle(url):
                return handler_class
        
        return None
    
    def _is_direct_link(self, url: str) -> bool:
        """
        Deteksi apakah URL sudah direct link (bukan page hosting).
        """
        # Cek ekstensi file umum di URL path
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        # List ekstensi yang menandakan direct file
        file_extensions = (
            '.zip', '.rar', '.7z', '.tar', '.gz',
            '.mp4', '.mkv', '.avi', '.mov',
            '.mp3', '.flac', '.wav', '.aac',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx',
            '.jpg', '.jpeg', '.png', '.gif', '.webp',
            '.exe', '.msi', '.dmg', '.apk',
            '.iso', '.img', '.bin'
        )
        
        # Jika URL mengandung ekstensi file dan tidak ada path page umum hosting
        has_file_ext = any(path.endswith(ext) for ext in file_extensions)
        
        # Cek indicators page hosting (biasanya tidak ada di direct link)
        hosting_indicators = ['/file/', '/view/', '/download?', '/v/', '/d/']
        looks_like_page = any(ind in url for ind in hosting_indicators)
        
        return has_file_ext and not looks_like_page
    
    def mirror(self, url: str, filename: Optional[str] = None) -> dict:
        """
        Main entry point untuk mirroring file.
        """
        print(f"\n{'='*60}")
        print(f"🔍 URL: {url}")
        print(f"{'='*60}\n")
        
        # Deteksi hosting
        handler_class = self.detect_hosting(url)
        
        if handler_class is None:
            # Treat sebagai direct link
            print("📥 Mode: Direct Download (bukan file hosting dikenal)")
            return self._direct_download(url, filename)
        
        # Gunakan handler spesifik
        print(f"🌐 Hosting terdeteksi: {handler_class.HOSTING_NAME}")
        handler = handler_class()
        
        # Progress callback
        def progress(downloaded, total):
            if total > 0:
                percent = (downloaded / total) * 100
                mb = downloaded / (1024 * 1024)
                print(f"\r⏳ Progress: {percent:.1f}% ({mb:.2f} MB / {total/(1024*1024):.2f} MB)", 
                      end='', flush=True)
        
        print("🔗 Mengambil direct link...")
        result = handler.download(url, filename, progress_callback=progress)
        print()  # New line after progress
        
        return result
    
    def _direct_download(self, url: str, filename: Optional[str] = None) -> dict:
        """Download langsung tanpa parsing."""
        import requests
        
        try:
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
            })
            
            response = session.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Tentukan filename
            if not filename:
                cd = response.headers.get('content-disposition', '')
                if 'filename=' in cd:
                    filename = cd.split('filename=')[-1].strip('"\'')
                else:
                    filename = os.path.basename(urlparse(url).path) or 'downloaded_file'
            
            download_dir = Path("downloads")
            download_dir.mkdir(exist_ok=True)
            file_path = download_dir / filename
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r⏳ Progress: {percent:.1f}%", end='', flush=True)
            
            print()
            
            return {
                'success': True,
                'file_path': str(file_path),
                'file_size': downloaded,
                'hosting': 'direct',
                'message': f'Berhasil download: {filename}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'file_path': None,
                'file_size': 0,
                'hosting': 'direct',
                'message': f'Error: {str(e)}'
            }


def main():
    """Entry point."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <url> [filename]")
        print("Example: python main.py 'https://anonfiles.com/xxxxx/file.zip' 'backup.zip'")
        sys.exit(1)
    
    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Jika running di GitHub Actions, ambil dari env
    if not url and os.getenv('INPUT_URL'):
        url = os.getenv('INPUT_URL')
    if not filename and os.getenv('INPUT_FILENAME'):
        filename = os.getenv('INPUT_FILENAME')
    
    if not url:
        print("❌ Error: URL tidak ditemukan")
        sys.exit(1)
    
    # Initialize dispatcher
    dispatcher = MirrorDispatcher()
    
    if not dispatcher.handlers:
        print("⚠️ Warning: Tidak ada handler yang loaded")
    
    # Execute mirror
    result = dispatcher.mirror(url, filename)
    
    # Output result
    print(f"\n{'='*60}")
    if result['success']:
        print(f"✅ SUCCESS")
        print(f"📁 File: {result['file_path']}")
        print(f"📊 Size: {result['file_size'] / (1024*1024):.2f} MB")
        print(f"🌐 Source: {result['hosting']}")
    else:
        print(f"❌ FAILED")
        print(f"💬 {result['message']}")
        sys.exit(1)
    print(f"{'='*60}\n")
    
    # GitHub Actions output
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.getenv('GITHUB_OUTPUT'), 'a') as f:
            f.write(f"file_path={result['file_path']}\n")
            f.write(f"success={str(result['success']).lower()}\n")


if __name__ == "__main__":
    main()