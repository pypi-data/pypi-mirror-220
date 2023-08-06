import requests
from urllib.parse import urljoin
from .base import ATF_LOGGER, ApcKind, AuthError, NullAuth
from .frmnc import Frmnc

class Frmnc666(ApcKind):
    def fetch(self, user: str, password: str):
        base_url = "http://" + self._host
        s = requests.Session()
        s.auth = NullAuth()
        r = self.urlway(0, base_url, s.get, stream=True)
        forml = next(filter(lambda value: "name=\"frmLogin\"" in value, r.iter_lines(decode_unicode=True)))
        forml = next(filter(lambda value: "action=" in value, forml.split())).split('=', 2)[1].split('"', 3)[1]

        r = self.urlway(1, urljoin(base_url, forml), s.post, stream=True, data = {
            'login_username': user,
            'login_password': password,
        })
        if (r.status_code == 403) or (r.url == urljoin(base_url, forml)):
            del r, s
            raise AuthError()
        del forml

        try:
            r = self.urlway(2, urljoin(r.url, "upstat.htm"), s.get)
            upsst = Frmnc.parse(r.iter_lines(decode_unicode=True))
        finally:
            self.urlway(3, urljoin(r.url, "logout.htm"), s.get)
            del r, s

        ATF_LOGGER.debug(F'{self._host}: [result] {repr(upsst)}')
        return upsst

    @staticmethod
    def extract(upsst) -> str: return upsst['Internal Temperature'].replace('&deg;C', '')
