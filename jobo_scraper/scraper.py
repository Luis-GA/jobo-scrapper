from requests import Session
from bs4 import BeautifulSoup as bs

import logging

from .logging_messages import LOGIN_ERROR, SCRAPING_ERROR, SCRAPING_IMAGE_ERROR

LOGGER = logging.getLogger(__name__)


class JoboScraping:
    user = None
    password = None
    token = None
    session = Session()
    base_url = "https://madridcultura-jobo.shop.secutix.com/"
    events_url = f"{base_url}secured/list/events"
    login_url = f"{base_url}account/login"
    event_link = f"{base_url}secured/selection/event/date?productId="

    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password

    def _session_login(self, retries: int = 3):
        """Start a session in Jobo."""

        try:
            if not self.token:
                site = self.session.get(self.login_url)
                bs_content = bs(site.content, "html.parser")
                self.token = bs_content.find("input", {"name": "_csrf"})["value"]

            login_data = {
                "login": self.user,
                "password": self.password,
                "_csrf": self.token,
            }
            self.session.post(
                "https://madridcultura-jobo.shop.secutix.com/account/login", login_data
            )

        except Exception as exc:
            self.token = None

            LOGGER.warning(LOGIN_ERROR.format(exc, retries))
            if retries > 0:
                self._session_login(retries - 1)
            else:
                LOGGER.error(LOGIN_ERROR.format(exc, retries))
                raise exc

    def _image_scraper(self, image: str):
        """Scrap image URL."""
        try:
            for key, value in image.contents[1].attrs.items():
                if key.endswith("data-img-large"):
                    return value
        except Exception:
            LOGGER.error(SCRAPING_IMAGE_ERROR)
        # Default image
        return "https://i.ibb.co/N6Hy2TT/La-P-gina-de-Jobo-es-una-mierda.png"

    def _event_data_downloader(self):
        """Scrap the events webpage and list their attributes."""

        result_events = {}

        jobo_events_home_page = bs(
            str(self.session.get(self.events_url).content), "html.parser"
        )
        jobo_events = jobo_events_home_page.find_all(
            attrs={"class": "content product-with-logo"}
        )
        images = jobo_events_home_page.find_all(
            attrs={"class": "product_image_container product-image-scale-1"}
        )
        event_count = 0
        for jobo_event in jobo_events:
            try:
                available_link = jobo_event.find_all(
                    attrs={"class": "button action_buttons_0"}
                )
                if available_link:
                    id = jobo_event.find(href=True).attrs["href"].split("=")[-1]
                    event = {
                        "title": str(jobo_event.find(attrs={"class": "title"}).next),
                        "image": self._image_scraper(images[event_count]),
                        "place": str(jobo_event.find(attrs={"class": "site"}).next),
                        "link": self.event_link + id,
                        "days": str(jobo_event.find(attrs={"class": "day"}).string),
                        "description": str(
                            jobo_event.find(attrs={"class": "description"})
                            .contents[1]
                            .string
                        ),
                    }
                    result_events[event["title"]] = event
            except Exception as exc:
                LOGGER.error(SCRAPING_ERROR.format(exc))
                result_events["scraping_error"] = True
            event_count += 1

        return result_events

    def available_events(self) -> dict:
        """List all the available events."""
        # New Session builder
        self._session_login()
        # Scrap events
        return self._event_data_downloader()
