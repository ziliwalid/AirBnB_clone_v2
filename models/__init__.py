#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import getenv from os


if getenv("HBNB_TYPE_STORAGE") == "db":
	from models.engine.db_storage import DBStoarage
	storage = DBStorage()
else:
	from models.engine.file_storage import FileStorage
	storage = FileStorage()
storage.reload()
