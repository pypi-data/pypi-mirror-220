import re
import sys
import datetime
from .exceptions import UnknownDateFormat

from typing import Any, List, Dict, Optional

# PYTHON_VERSION = sys.version_info[0]


class Domain:
    # mandatory fields we expect always to be present (but can be None or '')
    name: Optional[str] = None
    tld: Optional[str] = None
    registrar: Optional[str] = None
    registrant_country: Optional[str] = None

    creation_date = None
    expiration_date = None
    last_updated = None

    status: Optional[str] = None
    statuses: List[str] = []

    dnssec: bool = False
    name_servers: List[str] = []

    # optional fields
    owner: Optional[str] = None
    abuse_contact = None
    reseller = None
    registrant = None
    admin = None
    emails: List[str] = []

    def _cleanupArray(
        self,
        data: List[str],
    ) -> List[str]:
        if "" in data:
            index = data.index("")
            data.pop(index)
        return data

    def _doNameservers(
        self,
        data: Dict[str, Any],
    ) -> None:
        tmp: List[str] = []
        for x in data["name_servers"]:
            if isinstance(x, str):
                tmp.append(x.strip().lower())
                continue
            # not a string but an array
            for y in x:
                tmp.append(y.strip().lower())

        self.name_servers = []
        for x in tmp:
            x = x.strip(" .")  # remove any leading or trailing spaces and/or dots
            if x:
                if " " in x:
                    x, _ = x.split(" ", 1)
                    x = x.strip(" .")

                x = x.lower()
                if x not in self.name_servers:
                    self.name_servers.append(x)
        self.name_servers = sorted(self.name_servers)

    def _doStatus(
        self,
        data: Dict[str, Any],
    ) -> None:
        self.status = data["status"][0].strip()
        self.statuses = sorted(  # sorted added to get predictable output during test
            list(  # list(set(...))) to deduplicate results
                set(
                    [s.strip() for s in data["status"]],
                ),
            ),
        )
        if "" in self.statuses:
            self.statuses = self._cleanupArray(self.statuses)

    def _doOptionalFields(
        self,
        data: Dict[str, Any],
    ) -> None:
        # optional fiels
        if "owner" in data:
            self.owner = data["owner"][0].strip()

        if "abuse_contact" in data:
            self.abuse_contact = data["abuse_contact"][0].strip()

        if "reseller" in data:
            self.reseller = data["reseller"][0].strip()

        if "registrant" in data:
            self.registrant = data["registrant"][0].strip()

        if "admin" in data:
            self.admin = data["admin"][0].strip()

        if "emails" in data:
            self.emails = sorted(  # sorted added to get predictable output during test
                list(  # list(set(...))) to deduplicate results
                    set(
                        [s.strip() for s in data["emails"]],
                    ),
                ),
            )
            if "" in self.emails:
                self.emails = self._cleanupArray(self.emails)

    def __init__(
        self,
        data: Dict[str, Any],
        whois_str: Optional[str] = None,
        verbose: bool = False,
        include_raw_whois_text: bool = False,
        return_raw_text_for_unsupported_tld: bool = False,
        exeptionStr: Optional[str] = None,
    ):
        if include_raw_whois_text and whois_str is not None:
            self.text = whois_str

        if exeptionStr is not None:
            self._exception = exeptionStr
            return

        self.name = data["domain_name"][0].strip().lower()
        self.tld = data["tld"].lower()

        if return_raw_text_for_unsupported_tld is True:
            return

        # process mandatory fields that we expact always to be present even if we have None or ''
        self.registrar = data["registrar"][0].strip()
        self.registrant_country = data["registrant_country"][0].strip()

        # date time items
        self.creation_date = str_to_date(data["creation_date"][0], self.tld, verbose=verbose)
        self.expiration_date = str_to_date(data["expiration_date"][0], self.tld, verbose=verbose)
        self.last_updated = str_to_date(data["updated_date"][0], self.tld, verbose=verbose)

        self.dnssec = data["DNSSEC"]
        self._doStatus(data)
        self._doNameservers(data)

        # optional fiels
        self._doOptionalFields(data)


# http://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_FORMATS = [
    "%d-%b-%Y",  # 02-jan-2000
    "%d-%m-%Y",  # 02-01-2000
    "%d.%m.%Y",  # 02.02.2000
    "%d/%m/%Y",  # 01/06/2011
    "%Y-%m-%d",  # 2000-01-02
    "%Y.%m.%d",  # 2000.01.02
    "%Y/%m/%d",  # 2005/05/30
    "%b-%Y",  # aug-1996
    "before %b-%Y",  # before aug-1996
    "before %Y%m%d",  # before 19950101
    "%Y.%m.%d %H:%M:%S",  # 2002.09.19 13:00:00
    "%Y%m%d %H:%M:%S",  # 20110908 14:44:51
    "%Y-%m-%d %H:%M:%S",  # 2011-09-08 14:44:51
    "%Y-%m-%d %H:%M:%S%z",  # 2025-04-27 02:54:19+03:00
    "%Y-%m-%d %H:%M:%S %z",  # 2020-05-18 01:30:25 +0200
    "%Y-%m-%d %H:%M:%S CLST",  # 2011-09-08 14:44:51 CLST CL
    "%Y-%m-%d %H:%M:%S.%f",  # 2011-09-08 14:44:51 CLST CL
    "%d.%m.%Y  %H:%M:%S",  # 19.09.2002 13:00:00
    "%d-%b-%Y %H:%M:%S %Z",  # 24-Jul-2009 13:20:03 UTC
    "%Y/%m/%d %H:%M:%S (%z)",  # 2011/06/01 01:05:01 (+0900)
    "%Y/%m/%d %H:%M:%S",  # 2011/06/01 01:05:01
    "%a %b %d %H:%M:%S %Z %Y",  # Tue Jun 21 23:59:59 GMT 2011
    "%a %b %d %Y",  # Tue Dec 12 2000
    "%Y-%m-%dT%H:%M:%S",  # 2007-01-26T19:10:31
    "%Y-%m-%dT%H:%M:%SZ",  # 2007-01-26T19:10:31Z
    "%Y-%m-%dt%H:%M:%S.%fz",  # 2007-01-26t19:10:31.00z
    "%Y-%m-%dT%H:%M:%S%z",  # 2011-03-30T19:36:27+0200
    "%Y-%m-%dT%H:%M:%S.%f%z",  # 2011-09-08T14:44:51.622265+03:00
    "%Y-%m-%dt%H:%M:%S.%f",  # 2011-09-08t14:44:51.622265
    "%Y-%m-%dt%H:%M:%S",  # 2007-01-26T19:10:31
    "%Y-%m-%dt%H:%M:%SZ",  # 2007-01-26T19:10:31Z
    "%Y-%m-%dt%H:%M:%Sz",  # 2007-01-26T19:10:31Z
    "%Y-%m-%dt%H:%M:%S.%fz",  # 2007-01-26t19:10:31.00z
    "%Y-%m-%dt%H:%M:%S%z",  # 2011-03-30T19:36:27+0200
    "%Y-%m-%dt%H:%M:%S.%f%z",  # 2011-09-08T14:44:51.622265+03:00
    "%Y%m%d",  # 20110908
    "%Y. %m. %d.",  # 2020. 01. 12.
    "before %b-%Y",  # before aug-1996
    "%a %d %b %Y",  # Tue 21 Jun 2011
    "%A %d %b %Y",  # Tuesday 21 Jun 2011
    "%a %d %B %Y",  # Tue 21 June 2011
    "%A %d %B %Y",  # Tuesday 21 June 2011
    "%Y-%m-%d %H:%M:%S (%Z+0:00)",  # 2007-12-24 10:24:32 (gmt+0:00)
    "%d-%m-%Y %H:%M:%S %Z+1",  # 19-04-2021 13:56:51 GMT+1
    "%B %d %Y",  # January 01 2000
    "%Y-%b-%d",  # 2021-Oct-18
    "%d/%m/%Y %H:%M:%S",  # 08/09/2011 14:44:51
    "%m/%d/%Y",  # 03/28/2013
    "%d %b %Y",  # 28 jan 2021
    "%d-%b-%Y %H:%M:%S",  # 30-nov-2009 17:00:58
    "%Y%m%d%H%M%S",  # 20071224102432 used in edu_ua
    "%Y-%m-%d %H:%M:%S (%Z%z)",  # .tw uses (UTC+8) but we need (UTC+0800) for %z match
    "%d %B %Y at %H:%M:%S.%f",  # 07 january 2020 at 23:38:30.772
    "%Y-%m-%d %H:%M:%S.%f %Z",  # 2022-09-18 22:38:18.0 UTC (sn Senegal),
    "%a %b %d %H:%M:%S %Y",  # Thu Oct 21 05:54:20 2032 (kg Kyrgyzstan)
    "%m-%d-%Y",  # 03-28-2013 # is ambivalent for all days <=12
]

CUSTOM_DATE_FORMATS = {
    "ml": "%m/%d/%Y",
}


def str_to_date(
    text: str,
    tld: Optional[str] = None,
    verbose: bool = False,
) -> Optional[datetime.datetime]:
    text = text.strip().lower()

    if verbose:
        print(f"tld: {tld}; str_to_date: {text}", file=sys.stderr)

    noDate = [
        "not defined",
        "n/a",
        "none",
    ]
    if not text or text in noDate:
        return None

    # replace japan standard time to +0900 (%z format)
    text = text.replace("(jst)", "(+0900)")
    text = re.sub(r"(\+[0-9]{2}):([0-9]{2})", "\\1\\2", text)

    # text = re.sub(r"(\+[0-9]{2})$", "\\1:00", text)
    # text = re.sub(r"(\+[0-9]{2})$", "\\100", text) # python 3.6 does not parse : in the timezone offset
    if re.search(r"(\+[0-9]{2})$", text):
        text = text + "00"

    # strip trailing space and comment
    text = re.sub(r"(\ #.*)", "", text)

    # tw uses UTC+8, but strptime needs UTC+0800), note we are now lower case
    r = r"\(utc([-+])(\d)\)"
    if re.search(r, text):
        text = re.sub(r, "(utc\\g<1>0\\g<2>00)", text)

    # hack for 1st 2nd 3rd 4th etc
    # better here https://stackoverflow.com/questions/1258199/python-datetime-strptime-wildcard
    text = re.sub(r"(\d+)(st|nd|rd|th) ", r"\1 ", text)

    # Remove consecutive whitespace
    text = re.sub(r"\s\s+", r" ", text)

    # 07 january 2020 at 23:38:30.772
    # %d %B %Y at %H:%M %S.%f
    if tld and tld in CUSTOM_DATE_FORMATS:
        return (
            datetime.datetime.strptime(
                text,
                CUSTOM_DATE_FORMATS[tld],
            )
            .astimezone()
            .replace(tzinfo=None)
        )

    for f in DATE_FORMATS:
        try:
            if verbose:
                print(f"try with {f} on text: {text}", file=sys.stderr)
            z = datetime.datetime.strptime(text, f)
            z = z.astimezone()
            z = z.replace(tzinfo=None)
            return z
        except ValueError as v:
            if verbose:
                print(f"{v}", file=sys.stderr)
            pass

    raise UnknownDateFormat("Unknown date format: '%s'" % text)
