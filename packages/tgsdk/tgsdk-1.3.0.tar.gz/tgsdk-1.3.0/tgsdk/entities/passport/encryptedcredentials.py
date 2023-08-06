#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import Any

from tgsdk import TelegramEntity


class EncryptedCredentials(TelegramEntity):
	__slots__ = ("data", "hash", "secret")

	def __init__(
		self,
		data: str,
		hash: str,
		secret: str,

		**_kwargs: Any
	):
		self.data = data
		self.hash = hash
		self.secret = secret
