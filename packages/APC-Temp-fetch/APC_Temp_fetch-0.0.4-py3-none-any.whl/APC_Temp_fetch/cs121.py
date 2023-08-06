import requests
from collections.abc import Iterable
from typing import Dict, List
from .base import ATF_LOGGER, ApcKind

def mangle_subpart(sp: str) -> str:
    # e.g. parts look like: ['"><b>L1:', '</b>10', '%</td><td class="']
    return sp.removeprefix(' width="100%" colspan=3').removeprefix('>').replace('<b>', '').replace('</b>', '').removesuffix('</tr>').removesuffix('<td class=').removesuffix('</td>')

def mangle_line(l: str) -> tuple[str, List[List[str]]]:
    l = l.split('_dw')[1]
    lkey = l.split('("')[1].split('")')[0]
    lvalue = map(lambda p: map(mangle_subpart, p.split('&nbsp;')), l.split('"mainb"')[1:])
    return (lkey, [[j for j in i] for i in lvalue])

class Cs121(ApcKind):
    @staticmethod
    def parse(rlns: Iterable[str]) -> Dict[str, List[List[str]]]:
        tmp = map(mangle_line, filter(lambda l: ('_dw' in l) and ('&nbsp;' in l), rlns))
        return {key: value for key, value in tmp}

    def fetch(self, user: str, password: str):
        # we ignore user and password
        rlns = self.urlway(0, F'http://{self._host}/main.shtml', requests.get, stream = True).iter_lines(decode_unicode=True)
        upsst = self.parse(rlns)
        ATF_LOGGER.debug(F'{self._host}: [result] {repr(upsst)}')
        return upsst

    @staticmethod
    def extract(upsst: Dict[str, List[List[str]]]) -> str:
        return upsst["UPS Temperature"][0][1]
