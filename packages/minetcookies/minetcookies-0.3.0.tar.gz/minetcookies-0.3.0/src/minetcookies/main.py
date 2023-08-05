import subprocess
import sys
from pathlib import Path

import yaml


default_yaml = """
---
buzzsumo:
  token: "MY_BZ_TOKEN"
crowdtangle:
  token: "MY_CT_TOKEN"
  rate_limit: 10
facebook:
  cookie: "MY_FACEBOOK_COOKIE"
instagram:
  cookie: "MY_INSTAGRAM_COOKIE"
mediacloud:
  token: "MY_MC_TOKEN"
tiktok:
  cookie: "MY_TIKTOK_COOKIE"
twitter:
  cookie: "MY_TWITTER_COOKIE"
  api_key: "MY_API_KEY"
  api_secret_key: "MY_API_SECRET_KEY"
  access_token: "MY_ACCESS_TOKEN"
  access_token_secret: "MY_ACCESS_TOKEN_SECRET"
youtube:
  key: "MY_YT_API_KEY"
  """

home = Path.home()
configfile = home / ".minetrc"

if not configfile.exists():
    configfile.write_text(default_yaml)

config = yaml.safe_load(configfile.read_text())


class UndefinedCookie(Exception):
    pass


class NotLoggedIn(Exception):
    pass


def CookieChecker(cookie:str, media:str):
    media_spec = {
        "twitter": "_twitter_sess=",
        "instagram": "sessionid=",  # "ds_user_id="
        "facebook": "c_user=",
        "tiktok": "sessionid=",
    }
    if cookie is None or cookie == "" or cookie.startswith("MY"):
        raise UndefinedCookie(f"Le cookie pour {media} n'est pas défini")

    if media_spec[media] not in cookie:
        raise NotLoggedIn(f"Le cookie pour {media} n'est pas valide")


def minettest():
    try:
        subprocess.run(["minet", "--version"], capture_output=True)
    except FileNotFoundError:
        raise RuntimeError("Minet n'est pas installé")
        # args = "curl -sSL https://raw.githubusercontent.com/medialab/minet/master/scripts/install.sh | bash".split(" ")
        # subprocess.run(args, capture_output=True)


def get(media: str, key: str):
    return config[media][key]


def set(media: str, key: str, value: str):
    config[media][key] = value


def save():
    configfile.write_text(yaml.dump(config))


def recover_cookies(media: str):
    bros = ['chrome', 'firefox', 'chromium', 'edge']
    loggedout = False
    for navigator in bros:
        cookie = subprocess.run(["minet", "cookies", navigator, "--url", f"https://www.{media}.com"],
                                capture_output=True)
        cookie = cookie.stdout.decode("utf-8").strip()

        try:
            CookieChecker(cookie, media)
            break
        except UndefinedCookie:
            continue
        except NotLoggedIn:
            loggedout = True
            continue
    else:
        if loggedout:
            raise RuntimeError(
                f"Vous êtes déconnecté de {media}.com veillez à vous connecter puis réessayez.\n(Navigateurs supportés : {bros})")
        raise RuntimeError(
            f"Aucun cookie trouvé pour {media} veillez à vous connecter sur https://www.{media}.com puis réessayez.\n(Navigateurs supportés : {bros})")

    set(media, "cookie", cookie)
    save()

    print(f"Cookie for {media} saved")


def main(query: list = None):
    if query is None:
        args = sys.argv[1:]
    else:
        args = query.copy()

    query = " ".join(args)

    minettest()

    query = query.split(" ")
    media = query[0]

    if media in ["instagram", "tiktok", "twitter", "facebook"]:
        key = "cookie"
    else:
        raise NotImplementedError

    actualcookie = get(media, key)
    if actualcookie.startswith("MY_") or actualcookie == "":
        recover_cookies(media)

    if len(args) == 1:
        newcookie = get(media, key)
        if newcookie == actualcookie:
            print(f"Cookie for {media} unchanged ({actualcookie})")
        else:
            print(f"Cookie for {media} replaced from {actualcookie} to {get(media, key)}")
        print("No additional arguments given, exiting")
        return

    outp = Path(args[2])

    print(outp.expanduser().resolve().as_posix())


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
