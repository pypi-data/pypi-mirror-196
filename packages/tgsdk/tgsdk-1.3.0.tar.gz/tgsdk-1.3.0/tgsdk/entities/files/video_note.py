#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from tgsdk import TelegramEntity

from .photosize import PhotoSize

if TYPE_CHECKING:
	from tgsdk import Bot, File


class VideoNote(TelegramEntity):
	"""
	https://core.telegram.org/bots/api#videonote

	"""
	__slots__ = ("file_id", "file_unique_id", "length", "duration", "thumbnail", "file_size", "bot")

	def __init__(
		self,
		file_id: str,
		file_unique_id: str,
		length: int,
		duration: int,
		thumbnail: Optional[PhotoSize] = None,
		file_size: Optional[int] = None,

		bot: Optional["Bot"] = None,

		**_kwargs: Any
	):
		self.file_id = file_id
		self.file_unique_id = file_unique_id
		self.length = length
		self.duration = duration
		self.thumbnail = thumbnail
		self.file_size = file_size

		self.bot = bot

	@classmethod
	def de_json(cls, data: Optional[Dict] = None) -> Union["VideoNote", None]:
		"""

		:param data:
		:return:
		"""
		if not data:
			return None

		data["thumbnail"] = PhotoSize.de_json(data.get("thumbnail"))

		return cls(**data)

	def get_file(self, timeout: float = None, kwargs: Dict = None) -> "File":
		"""

		:param timeout:
		:param kwargs:
		:return:
		"""
		return self.bot.get_file(file_id=self.file_id, timeout=timeout, kwargs=kwargs)
