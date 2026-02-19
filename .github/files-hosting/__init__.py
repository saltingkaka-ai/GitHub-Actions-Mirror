"""
Files Hosting Handlers Package
=============================

Cara menambahkan hosting baru:
1. Buat file baru di folder ini (e.g., newhosting.py)
2. Inherit dari BaseHostingHandler
3. Implementasikan get_direct_link()
4. Definisikan HOSTING_NAME dan DOMAINS
"""

from .base import BaseHostingHandler

__all__ = ['BaseHostingHandler']