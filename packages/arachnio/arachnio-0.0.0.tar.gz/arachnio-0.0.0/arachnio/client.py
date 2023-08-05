import requests


class ArachnioException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ForbiddenArachnioException(ArachnioException):
    def __init__(self):
        super().__init__("Forbidden")


class UnauthorizedArachnioException(ArachnioException):
    def __init__(self):
        super().__init__("Unauthorized")


class ArachnioClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def parse_domain(self, domain):
        """ Works with any Arachnio plan. """
        response = requests.post(
            f"{self.base_url}/domains/parse",
            json={"hostname": domain},
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")
        return response.json()

    def parse_domain_batch(self, domains):
        """ Returns batch outputs in same order as input. Failed elements may be None in result.
        Works with Growth and Enterprise Arachnio plans only. """
        response = requests.post(
            f"{self.base_url}/domains/parse/batch",
            json={
                "entries": [
                    {"id": str(i), "domain": {"hostname": domains[i]}} for i in range(0, len(domains))
                ]
            },
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")

        data = response.json()

        entries = {e["id"]: {k: v for k, v in e.items() if k != "id"} for e in data["entries"]}

        return [entries[str(i)] if str(i) in entries else None for i in range(0, len(domains))]

    def parse_link(self, url):
        """ Works with any Arachnio plan. """
        response = requests.post(
            f"{self.base_url}/links/parse",
            json={"url": url},
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")
        return response.json()

    def parse_link_batch(self, urls):
        """ Returns batch outputs in same order as input. Failed elements may be None in result.
        Works with Growth and Enterprise Arachnio plans only. """
        response = requests.post(
            f"{self.base_url}/links/parse/batch",
            json={
                "entries": [
                    {"id": str(i), "link": {"url": urls[i]}} for i in range(0, len(urls))
                ]
            },
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")

        data = response.json()

        entries = {e["id"]: {k: v for k, v in e.items() if k != "id"} for e in data["entries"]}

        return [entries[str(i)] if str(i) in entries else None for i in range(0, len(urls))]

    def unwind_link(self, url):
        """ Works with any Arachnio plan. """
        response = requests.post(
            f"{self.base_url}/links/unwind",
            json={"url": url},
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")
        return response.json()

    def unwind_link_batch(self, urls):
        """ Returns batch outputs in same order as input. Failed elements may be None in result.
        Works with Growth and Enterprise Arachnio plans only. """
        response = requests.post(
            f"{self.base_url}/links/unwind/batch",
            json={
                "entries": [
                    {"id": str(i), "link": {"url": urls[i]}} for i in range(0, len(urls))
                ]
            },
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")

        data = response.json()

        entries = {e["id"]: {k: v for k, v in e.items() if k != "id"} for e in data["entries"]}

        return [entries[str(i)] if str(i) in entries else None for i in range(0, len(urls))]

    def extract_link(self, url):
        """ Works with any Arachnio plan. """
        response = requests.post(
            f"{self.base_url}/links/extract",
            json={"url": url},
            headers={
                "X-BLOBR-KEY": self.api_key
            })
        if response.status_code == 400 or response.status_code == 422:
            raise ValueError()
        if response.status_code == 401:
            raise UnauthorizedArachnioException()
        if response.status_code == 403:
            raise ForbiddenArachnioException()
        if response.status_code != 200:
            raise ArachnioException(f"Failed with status code {response.status_code}")
        return response.json()
