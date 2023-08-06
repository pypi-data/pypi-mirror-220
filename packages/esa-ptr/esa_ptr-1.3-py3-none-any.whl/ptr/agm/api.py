"""AGM API module."""

import json
from datetime import datetime
from urllib import request

from .cache import AGM_CACHE
from .results import AGMResults
from ..esa.pointing_tool import POINTING_TOOL_ENDPOINTS


def agm_api(metakernel, ptr, endpoint, cache=True):
    """Call AGM through a REST API.

    Parameters
    ----------
    metakernel: str
        Metakernel id.
    ptr: str
        Pointing Timeline Request.
    endpoint: str, optional
        Explicit AGM URL endpoint. You can also use the mission
        names listed in ``POINTING_TOOL_ENDPOINTS`` like ``'JUICE_API'``.
    cache: bool, optional
        Use cache the response if present locally.

    Raises
    ------
    ValueError
        If the URL endpoint is unknown.

    """
    if endpoint in POINTING_TOOL_ENDPOINTS:
        pointing_tool = POINTING_TOOL_ENDPOINTS[endpoint]

        # Get metakernel from the pointing tool contexts (if present)
        if metakernel in pointing_tool:
            metakernel = pointing_tool[metakernel].mk

        url = pointing_tool.agm_url

    elif '://' in endpoint:
        url = endpoint

    else:
        raise ValueError(f'Unknown endpoint: {endpoint}')

    fname = AGM_CACHE(metakernel, ptr, url)

    if cache and fname.exists():
        return AGMResults(fname)

    payload = json.dumps({
        'metakernel': metakernel,
        'ptr_content': str(ptr),
    }).encode('utf-8')

    req = request.Request(url, data=payload)

    with request.urlopen(req) as resp:
        results = {
            'endpoint': url,
            'metakernel': metakernel,
            'ptr': str(ptr).strip(),
            'results': json.load(resp),
            'created': datetime.now().isoformat(timespec='seconds'),
            'cache': {
                'location': str(AGM_CACHE),
                'md5_hash': fname.stem,
            } if cache else False,
        }

    if cache:
        with fname.open('w', encoding='utf-8') as f:
            json.dump(results, f)

    return AGMResults(results)
