#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import Any, List, Optional, Union

from tgsdk import Audio, InputFile, InputMedia, MessageEntity
from tgsdk.utils.get_input_file import get_input_file


class InputMediaAudio(InputMedia):
	__slots__ = ("media", "thumbnail", "caption", "parse_mode", "caption_entities", "duration", "performer", "title", "file_name")

	def __init__(
		self,
		media: Union[InputFile, Audio],
		thumbnail: Optional[InputFile] = None,
		caption: Optional[str] = None,
		parse_mode: Optional[str] = None,
		caption_entities: Optional[List[MessageEntity]] = None,
		duration: Optional[int] = None,
		performer: Optional[int] = None,
		title: Optional[str] = None,
		file_name: Optional[str] = None,

		**_kwargs: Any
	):
		super().__init__(
			type="audio",
			caption_entities=caption_entities
		)

		self.media = media
		self.thumbnail = thumbnail
		self.caption = caption
		self.parse_mode = parse_mode
		self.file_name = file_name

		if isinstance(media, Audio):
			self.media = media.file_id  # type: str

			self.title = media.title
			self.duration = media.duration
			self.performer = media.performer
		else:
			self.media = get_input_file(media, as_attach=True, file_name=self.file_name)

			self.title = title
			self.duration = duration
			self.performer = performer

		if thumbnail:
			self.thumbnail = get_input_file(thumbnail, as_attach=True)
