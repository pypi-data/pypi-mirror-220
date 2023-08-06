from .parser import parse as _parse
from .result import GitUrlParsed

__author__ = "Michal Nowikowski"
__email__ = "godfryd@gmail.com"
__version__ = "1.0.0"


def parse(url, check_domain=True):
    return GitUrlParsed(_parse(url, check_domain))


def validate(url, check_domain=True):
    return parse(url, check_domain).valid
