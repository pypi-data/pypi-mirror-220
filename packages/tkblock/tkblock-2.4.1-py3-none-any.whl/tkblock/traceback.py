#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# kuri_pome
"""TracebackCatch"""
import os
import traceback
import threading

from .logger import create_logger, FileKind


class TracebackCatch:
    """例外の情報をlogファイル出力する"""

    logger = None

    def __init__(self, func, subst, widget):
        """Store FUNC, SUBST and WIDGET as members."""
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        """call"""
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except SystemExit as e:
            raise e
        except:
            TracebackCatch.logger.error(
                "----------------------------------------------"
            )
            TracebackCatch.logger.error(traceback.format_exc())
            TracebackCatch.logger.error(f"threading.enumerate: {threading.enumerate()}")
            self.widget._report_exception()

    def init_logger(file_path=f"{os.getcwd()}/error.log", rotate_max_bytes=1024 * 1024):
        TracebackCatch.logger = create_logger(
            __name__,
            level="debug",
            is_stream_handler=False,
            is_file_handler=True,
            file_kind=FileKind.ROTATE,
            file_path=file_path,
            rotate_max_bytes=rotate_max_bytes,
        )
