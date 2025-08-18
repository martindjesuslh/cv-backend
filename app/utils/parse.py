from http.cookies import SimpleCookie, Morsel
from typing import Dict, Any
from pydantic import BaseModel


class ParseData:
    @staticmethod
    def parse_http_cookie(cookie_str: str) -> Dict[str, str]:
        cookies_dict: Dict[str, str] = {}

        for line in cookie_str.strip().split("\n"):
            parts = line.split("\t")

            if len(parts) >= 2:
                cookie_name = parts[0]
                cookie_value = parts[1]
                cookies_dict[cookie_name] = cookie_value

        return cookies_dict

    @staticmethod
    def parse_http_cookie_detailed(cookie_str: str) -> Dict[str, Dict[str, Any]]:
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

    @staticmethod
    def pydantic_to_dict(obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return ParseData.pydantic_to_dict(obj.model_dump(mode="python"))
        elif isinstance(obj, dict):
            return {
                key: ParseData.pydantic_to_dict(value) for key, value in obj.items()
            }
        elif isinstance(obj, (list, tuple, set)):
            return [ParseData.pydantic_to_dict(item) for item in obj]
        elif hasattr(obj, "__str__") and not isinstance(
            obj, (str, int, float, bool, type(None))
        ):
            return str(obj)
        else:
            return obj
