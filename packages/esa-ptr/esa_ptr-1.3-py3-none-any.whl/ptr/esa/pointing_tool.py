"""ESA pointing tool API module."""

import json
from hashlib import md5
from pathlib import Path
from tempfile import gettempdir
from urllib import request


PT_CACHE = Path(gettempdir()) / 'pointing-tool-api-cache'
PT_CACHE.mkdir(parents=True, exist_ok=True)


def pt_api(url, use_cache=True):
    """Pointing tool API request.

    Parameters
    ----------
    url: str
        Endpoint URL to request.
    use_cache: bool, optional
        Cache the API request and fallback to the cache
        if the API resource is not available

    Returns
    -------
    list or dict
        Parsed JSON response.

    Raises
    ------
    FileNotFoundError
        If API service is not available and no cache was found.

    """
    try:
        with request.urlopen(url) as resp:
            data = json.loads(resp.read())

        if use_cache:
            pt_cache(url).write_text(json.dumps(data))

    except request.URLError:
        if use_cache and (cache := pt_cache(url)).exists():
            data = json.loads(cache.read_text())
        else:
            raise FileNotFoundError(
                'Pointing tool service unavailable and cache not found.'
            ) from None

    return data


def pt_cache(url) -> Path:
    """Pointing tool cache file based on URL."""
    return PT_CACHE / (md5(url.encode()).hexdigest() + '.json')


class PointingToolApi:
    """Pointing tool API object.

    Parameters
    ----------
    endpoint: str
        API endpoint url.
    cache: bool, optional
        Enable API caching (default: True).

    """
    def __init__(self, endpoint, use_cache=True):
        self.endpoint = endpoint
        self.use_cache = use_cache
        self._contexts = None

    def __str__(self):
        return self.endpoint

    def __repr__(self):
        contexts = '\n- '.join([
            'Contexts:',
            *[str(context) for context in self]
        ])
        return f'<{self.__class__.__name__}> {self} | {contexts}'

    def __contains__(self, item):
        for context in self.contexts:
            if context == item:
                return True
        return False

    def __getitem__(self, item):
        for context in self.contexts:
            if context == item:
                return context
        raise KeyError(f'Context: `{item}` not found.')

    def __len__(self):
        return len(self.contexts)

    def __iter__(self):
        return iter(self.contexts)

    @property
    def agm_url(self):
        """PT AGM endpoint URL."""
        return f'{self}/agm'

    @property
    def url_contexts(self):
        """PT trajectory contexts URL."""
        return f'{self}/assets/trajectory_contexts.json'

    @property
    def contexts(self):
        """Pointing tool context."""
        if self._contexts is None:
            self._contexts = self._load_contexts()
        return self._contexts

    def _load_contexts(self):
        """Load contexts list from the API."""
        return [
            PointingToolContext(self, **context)
            for context in reversed(pt_api(self.url_contexts, use_cache=self.use_cache))
        ]


class PointingToolContext:
    """Pointing tool API context object.

    Parameters
    ----------
    name: str
        API endpoint url.
    context: str
        API context key.

    """
    def __init__(self, api, name=None, context=None):
        self.api = api
        self.name = name
        self.context_id = context
        self._info = None

    def __str__(self):
        return self.name

    def __repr__(self):
        infos = '\n- '.join([
            f'{self}',
            *[f'{k}: {v}' for k, v in self.info.items() if not isinstance(v, list)]
        ])
        return f'<{self.__class__.__name__}> {infos}'

    def __eq__(self, other):
        return self.name == str(other) or self.context_id == str(other)

    @property
    def url(self):
        """Context definition URL."""
        return f'{self.api}/{self.context_id}/serviceinfo'

    @property
    def info(self):
        """Context infos."""
        if self._info is None:
            self._info = pt_api(self.url, use_cache=self.api.use_cache)
        return self._info

    @property
    def mk(self):
        """Context metakernel."""
        return self.info['metakernel']


JUICE_POINTING_TOOL = PointingToolApi('https://juicept.esac.esa.int')


POINTING_TOOL_ENDPOINTS = {
    'JUICE_API': JUICE_POINTING_TOOL,
}
