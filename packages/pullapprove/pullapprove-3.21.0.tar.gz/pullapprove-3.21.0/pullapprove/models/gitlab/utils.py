import re


def shorten_report_url(url: str) -> str:
    truncated = url
    truncated = re.sub("url=.+/reports/", r"t=", truncated)
    truncated = re.sub("fingerprint=", "f=", truncated)
    return truncated
