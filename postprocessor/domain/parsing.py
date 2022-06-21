import re

from schemas import Extra


def get_links(text: str):
    """Находит ссылки в тексте"""
    pattern = r'(https?://[^\s]+)'
    links = re.findall(pattern, text)

    result = []
    for link in links:
        result.append(
            Extra(text=link, offset=text.find(link), length=len(link))
        )

    return result


def get_hashtags(text):
    """Находит хештеги в тексте"""
    pattern = r'(#[a-zA-Zа-яА-Я]{0,30})'
    links = re.findall(pattern, text)

    result = []
    for link in links:
        result.append(
            Extra(text=link, offset=text.find(link), length=len(link))
        )

    return result


def get_extra(text: str):
    """Находит в тексте экстра-данные: ссылки, упоминания и т.д."""
    extra = []

    extra += get_links(text)
    extra += get_hashtags(text)

    return extra
