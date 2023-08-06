#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from pathlib import Path
from typing import IO, Any, List, Optional, Union

from tgsdk import Document, InputFile, InputMedia, MessageEntity
from tgsdk.utils.get_input_file import get_input_file


class InputMediaDocument(InputMedia):
	__slots__ = ("media", "thumbnail", "caption", "parse_mode", "caption_entities", "disable_content_type_detection", "file_name")

	def __init__(
		self,
		media: Union[Union[str, bytes, Union[IO, "InputFile"], Path], Document],
		thumbnail: Optional[Union[str, bytes, Union[IO, "InputFile"], Path]] = None,
		caption: Optional[str] = None,
		parse_mode: Optional[str] = None,
		caption_entities: Optional[List[MessageEntity]] = None,
		disable_content_type_detection: Optional[bool] = None,
		file_name: Optional[str] = None,

		**_kwargs: Any
	):
		super().__init__(
			type="document",
			caption_entities=caption_entities
		)

		self.media = media
		self.thumbnail = thumbnail
		self.caption = caption
		self.parse_mode = parse_mode
		self.file_name = file_name
		self.disable_content_type_detection = disable_content_type_detection

		self.media = get_input_file(media, Document, as_attach=True, file_name=self.file_name)

		if thumbnail:
			self.thumbnail = get_input_file(thumbnail, as_attach=True)
