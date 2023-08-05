import json
import re

from requests.cookies import RequestsCookieJar
from requests import Session

from .auth_token import AuthToken


USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    ),
}


class Client:
    sess: Session
    domain: str = "garmin.com"
    auth_token: AuthToken | None = None
    username: str | None = None

    def __init__(self, **kwargs):
        self.auth_token = None
        self.sess = Session()
        self.sess.headers.update(USER_AGENT)
        self.configure(**kwargs)

    def configure(
        self,
        /,
        auth_token: AuthToken | None = None,
        username: str | None = None,
        domain: str | None = None,  # Set to "garmin.cn" for China
    ):
        if auth_token:
            self.auth_token = auth_token
        if username:
            self.username = username
        if domain:
            self.domain = domain

    @property
    def username(self) -> str:
        if hasattr(self, "_username") and self._username:
            return self._username
        resp = self.get("connect", "/modern")
        m = re.search(r'userName":"(.+?)"', resp.text)
        if not m:
            raise Exception("Couldn't find username")
        self._username = m.group(1)
        return self._username

    def request(
        self,
        method: str,
        subdomain: str,
        path: str,
        /,
        api: bool = False,
        headers: dict = {},
        **kwargs,
    ):
        url = f"https://{subdomain}.{self.domain}{path}"
        if api:
            if self.auth_token and self.auth_token.expired:
                self.auth_token.refresh(client=self)
            headers["Authorization"] = str(self.auth_token)
            headers["di-backend"] = f"connectapi.{self.domain}"
        resp = self.sess.request(
            method,
            url,
            headers=headers,
            **kwargs,
        )
        resp.raise_for_status()
        return resp

    def get(self, *args, **kwargs):
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request("POST", *args, **kwargs)

    def login(self, *args):
        if not self.auth_token:
            self.cookies = RequestsCookieJar()  # Clear cookies
            token = AuthToken.login(*args, client=self)
            self.auth_token = token
        else:
            self.auth_token.refresh(client=self)

    def connectapi(self, path: str, **kwargs):
        return self.get("connect", path, api=True, **kwargs).json()

    def save_session(self, path: str):
        with open(path, "w") as f:
            json.dump(self.sess.cookies.get_dict(), f)

    def resume_session(self, path: str):
        with open(path) as f:
            cookies = json.load(f)
        self.sess.cookies.update(cookies)


client = Client()
