#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import Any, List, Optional, Union

from tgsdk import InputFile, InputMedia, MessageEntity, Video
from tgsdk.utils.get_input_file import get_input_file


class InputMediaVideo(InputMedia):
	__slots__ = ("media", "thumbnail", "caption", "parse_mode", "caption_entities", "width", "height", "duration", "supports_streaming", "file_name", "has_spoiler")

	def __init__(
		self,
		media: Union[InputFile, Video],
		thumbnail: Optional[InputFile] = None,
		caption: Optional[str] = None,
		parse_mode: Optional[str] = None,
		caption_entities: Optional[List[MessageEntity]] = None,
		width: Optional[int] = None,
		height: Optional[int] = None,
		duration: Optional[int] = None,
		supports_streaming: Optional[bool] = None,
		file_name: Optional[str] = None,
		has_spoiler: Optional[bool] = None,

		**_kwargs: Any
	):
		super().__init__(
			type="video",
			caption_entities=caption_entities
		)

		self.media = media
		self.thumbnail = thumbnail
		self.caption = caption
		self.parse_mode = parse_mode
		self.file_name = file_name
		self.supports_streaming = supports_streaming
		self.has_spoiler = has_spoiler

		if isinstance(media, Video):
			self.media = media.file_id  # type: str

			self.width = media.width
			self.height = media.height
			self.duration = media.duration
		else:
			self.media = get_input_file(media, as_attach=True, file_name=self.file_name)

			self.width = width
			self.height = height
			self.duration = duration

		if thumbnail:
			self.thumbnail = get_input_file(thumbnail, as_attach=True)
