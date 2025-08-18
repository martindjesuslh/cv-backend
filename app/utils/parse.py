from http.cookies import SimpleCookie, Morsel
from typing import Dict, Any


class ParseData:
    @staticmethod
    def parse_http_cookie(cookie_str: str) -> Dict[str, Dict[str, Any]]:
        cookie = SimpleCookie()

        cookies_dict: Dict[str, Dict[str, Any]] = {}

        for line in cookie_str.strip().split("\n"):
            parts = line.split("\t")

            if len(parts) >= 7:
                (
                    cookie_name,
                    cookie_value,
                    domain,
                    path,
                    expires,
                    secure,
                    httponly,
                ) = parts[:7]

                cookie[cookie_name] = cookie_value

                morsel: Morsel = cookie[cookie_name]
                morsel["domain"] = domain if domain != "-" else ""
                morsel["path"] = path if path != "-" else ""
                morsel["expires"] = expires if expires != "-" else ""
                morsel["secure"] = True if secure == "✓" else False
                morsel["httponly"] = True if httponly == "✓" else False

                cookies_dict[cookie_name] = {
                    "value": morsel.value,
                    "domain": morsel["domain"],
                    "path": morsel["path"],
                    "expires": morsel["expires"],
                    "secure": morsel["secure"],
                    "httponly": morsel["httponly"],
                }

        return cookies_dict
