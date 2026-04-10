from typing import Any

from .text_decorations import html_decoration, markdown_decoration


def _join(*content: Any, sep: str = " ") -> str:
    pass


def text(*content: Any, sep: str = " ") -> str:
    """
    Join all elements with a separator

    :param content:
    :param sep:
    :return:
    """
    pass


def bold(*content: Any, sep: str = " ") -> str:
    """
    Make bold text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hbold(*content: Any, sep: str = " ") -> str:
    """
    Make bold text (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def italic(*content: Any, sep: str = " ") -> str:
    """
    Make italic text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hitalic(*content: Any, sep: str = " ") -> str:
    """
    Make italic text (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def code(*content: Any, sep: str = " ") -> str:
    """
    Make mono-width text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hcode(*content: Any, sep: str = " ") -> str:
    """
    Make mono-width text (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def pre(*content: Any, sep: str = "\n") -> str:
    """
    Make mono-width text block (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hpre(*content: Any, sep: str = "\n") -> str:
    """
    Make mono-width text block (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def underline(*content: Any, sep: str = " ") -> str:
    """
    Make underlined text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hunderline(*content: Any, sep: str = " ") -> str:
    """
    Make underlined text (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def strikethrough(*content: Any, sep: str = " ") -> str:
    """
    Make strikethrough text (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hstrikethrough(*content: Any, sep: str = " ") -> str:
    """
    Make strikethrough text (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def link(title: str, url: str) -> str:
    """
    Format URL (Markdown)

    :param title:
    :param url:
    :return:
    """
    pass


def hlink(title: str, url: str) -> str:
    """
    Format URL (HTML)

    :param title:
    :param url:
    :return:
    """
    pass


def blockquote(*content: Any, sep: str = "\n") -> str:
    """
    Make blockquote (Markdown)

    :param content:
    :param sep:
    :return:
    """
    pass


def hblockquote(*content: Any, sep: str = "\n") -> str:
    """
    Make blockquote (HTML)

    :param content:
    :param sep:
    :return:
    """
    pass


def hide_link(url: str) -> str:
    """
    Hide URL (HTML only)
    Can be used for adding an image to a text message

    :param url:
    :return:
    """
    pass
