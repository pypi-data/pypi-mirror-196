from cloudscraper import create_scraper
from .utils import *
import requests
import json


class Telegraph:
    """
    Description: interface to telegraph api
    Usage: `Telegraph(mirror="https://tg.foxe6.cf")`

    :param mirror: telegraph mirror url (server requires account to proxy request)
    """
    def __init__(
            self,
            *,
            title="test",
            author="foxe6",
            author_url="https://tg.foxe6.cf",
            mirror="https://tg.foxe6.cf" # type: str
    ) -> None:
        self.title = title
        self.author = author
        self.author_url = author_url
        # Description: pixiv mirror url (server requires account to proxy request)
        # Usage: `[instance].mirror`
        self.mirror = mirror # type: str
        self.content = []
        self.s = create_scraper()

    def save(self, Data, title, author, author_url, save_hash, page_id):
        r= self.s.post(self.mirror+"/save", files={
            "Data": ("content.html", Data, "plain/text"),
            "title": (None, title),
            "author": (None, author),
            "author_url": (None, author_url),
            "save_hash": (None, save_hash),
            "page_id": (None, page_id),
        })
        r=r.json()
        return r

    def publish(self):
        def loop(e):
            if isinstance(e, list):
                return list(map(loop, e))
            elif isinstance(e, dict):
                return {k: loop(v) for k, v in e.items()}
            elif isinstance(e, TGE):
                return loop(e.obj)
            else:
                return e
        data = self.content
        data = json.dumps(loop(data))
        return self.save(
            Data=data,
            title=self.title,
            author=self.author,
            author_url=self.author_url,
            save_hash="",
            page_id=0,
        )

    def strong(
            self,
            *args,
            **kwargs
    ):
        t = STRONG(*args, **kwargs)
        return t

    def em(
            self,
            *args,
            **kwargs
    ):
        t = EM(*args, **kwargs)
        return t

    def a(
            self,
            *args,
            **kwargs
    ):
        t = A(*args, **kwargs)
        return t

    def p(
            self,
            *args,
            **kwargs
    ):
        t = P(*args, **kwargs)
        self.content.append(t)
        return t

    def blockquote(
            self,
            *args,
            **kwargs
    ):
        t = BLOCKQUOTE(*args, **kwargs)
        self.content.append(t)
        return t

    def aside(
            self,
            *args,
            **kwargs
    ):
        t = ASIDE(*args, **kwargs)
        self.content.append(t)
        return t

    def h3(
            self,
            *args,
            **kwargs
    ):
        t = H3(*args, **kwargs)
        self.content.append(t)
        return t

    def h4(
            self,
            *args,
            **kwargs
    ):
        t = H4(*args, **kwargs)
        self.content.append(t)
        return t

    def figure(
            self,
            *args,
            **kwargs
    ):
        t = FIGURE(*args, **kwargs)
        self.content.append(t)
        return t






