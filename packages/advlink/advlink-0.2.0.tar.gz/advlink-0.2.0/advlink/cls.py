import aiohttp
import aiofiles
import json
from importlib import metadata
import yarl
from typing import TypeVar
import asyncio
import io
import os
LINK = TypeVar("LINK", bound="Link")
class Link:
	"""
	The :class:`Link` class for the `advlink` package containing your :prop:`url`.
	"""
	def __init__(self, url: str, *, session: aiohttp.ClientSession = None, session2: aiohttp.ClientSession = None, loop: asyncio):
		self.session = aiohttp.ClientSession(auto_decompress=False) or session
		self.session2 = aiohttp.ClientSession() or session2
		self.url = url
		self.__aenter__ = self.session2.get(self.url).__aenter__
		self.__aexit__ = self.session2.get(self.url).__aexit__

	async def img(self, bytesio: bool = True):
		"""Fetches an image from the url."""
		async with self.session.get(self.url) as r:
			if bytesio:
				return await r.read()

	async def json(self) -> dict:
		"""Fetches a json instance from the url."""
		async with self.session2.get(self.url) as r:
			return await json.loads(await r.text())

	async def text(self):
		"""Fetches a :class:`str` from the url."""
		async with self.session2.get(self.url) as r:
			return await r.text()
	
	def __str__(self) -> str:
		return self.url

	def __hash__(self):
		return hash(self)

	def __eq__(self, __o: LINK) -> bool:
		return self.url == __o.url

	def __ne__(self, __o: LINK) -> bool:
		return self.url != __o.url

	async def savestr(self, fp: os.PathLike):
		"""Saves a link's text to a file"""
		async with aiofiles.open(fp, "w") as f:
			async with self.session2.get(self.url) as r:
				return await f.write(await r.text())

	async def saveimg(self, fp: os.PathLike):
		"""Saves the link's image to a file"""
		async with aiofiles.open(fp, "wb") as f:
			async with self.session.get(self.url) as r:
				return await f.write(await r.real_url)

	@property
	def yarlURL(self):
		e = yarl.URL(self.url)
		return e

__version__ = metadata.version("advlink")
"""The version of the package"""

# python3 -m twine upload --repository pypi dist/*