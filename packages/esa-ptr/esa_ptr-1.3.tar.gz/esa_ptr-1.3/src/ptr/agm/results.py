"""AGM results module."""

import json
import re
from html import escape
from pathlib import Path
from urllib import request

from ..datetime import dt
from ..html import HTMLCollapsible, html


class AGMResults:
    """AGM results object.

    Parameters
    ----------
    results: dict or pathlib.Path
        AGM formatted results.

    """

    def __init__(self, results):
        if isinstance(results, Path):
            with results.open('r') as fp:
                self.data = json.load(fp)

        elif isinstance(results, dict):
            self.data = results

        else:
            raise TypeError('Results must be a pathlib.Path or a dict. '
                            f'`{results.__class__.__name__}` provided.')

        # Parse the data content
        self.ptr = AGMResultsPTR(self['ptr'])
        self.status = AGMResultsStatus(self['results']['success'])

        session_id = self['results'].get('session_id')

        if self.status.success:
            self.log = AGMResultsLog(self['results']['output'], session_id=session_id)
            self.ck = AGMResultsCK(self)
            self.ptr_resolved = AGMResultsResolvedPTR(self)
            self.quaternions = AGMResultsQuaternions(self['results']['quaternions'])
        else:
            self.log = AGMResultsLog(self['results']['errors'], session_id=session_id)
            self.ck = None
            self.ptr_resolved = None
            self.quaternions = None

    def __str__(self):
        return json.dumps(self.data, indent=4)

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def _repr_html_(self):
        return '\n'.join([
            html(self.status),
            '<hr/>',
            html(HTMLCollapsible(
                ('Input Parameters', AGMInputParameters(self)),
                ('Output Results', AGMOutputResults(self) if self.status.success else ''),
                ('Log', self.log, '' if self.status.success else 'expand'),
            )),
        ])

    def __iter__(self):
        if self.status.success:
            return iter(self.ck)  # Load-able by spiceypy
        raise IOError('Simulation failed. No CK available')

    def __getitem__(self, item):
        try:
            return self.data[item]
        except KeyError:
            raise KeyError(f'`{item}` is not present in the results.') from None

    @property
    def success(self) -> bool:
        """Results status success flag."""
        return self.status.success


class AGMInputParameters:
    """AGM input parameters."""
    def __init__(self, res):
        self.endpoint = res['endpoint']
        self.mk = res['metakernel']
        self.ptr = res.ptr

    def __repr__(self):
        return str({
            'endpoint': self.endpoint,
            'metakernel': self.mk,
            'ptr': self.ptr,
        })

    def _repr_html_(self):
        return '\n'.join([
            '<ul style="color:#777">',
            f'<li><b>AGM Endpoint:</b> <code>{self.endpoint}</code></li>',
            f'<li><b>Metakernel:</b> <code>{self.mk}</code></li>'
            '</ul>',
            HTMLCollapsible(('PTR input:', self.ptr, 'expand')).html,
        ])


class AGMOutputResults:
    """AGM output results."""
    def __init__(self, res):
        self.ck = res.ck
        self.ptr_resolved = res.ptr_resolved
        self.quaternions = res.quaternions

    def __repr__(self):
        return str({
            'ck': self.ck,
            'ptr_resolved': self.ptr_resolved,
            'quaternions': self.quaternions,
        })

    def _repr_html_(self):
        return '\n'.join([
            '<ul style="color:#777">',
            f'<li><b>CK:</b> <code>{self.ck}</code></li>',
            f'<li><b>Resolved PTR:</b> <code>{self.ptr_resolved}</code></li>',
            '</ul>',
            HTMLCollapsible(('Quaternions', self.quaternions)).html,
        ])


class AGMResultsPTR:
    """AGM PTR object."""
    def __init__(self, ptr):
        self.ptr = ptr

    def __repr__(self):
        return self.ptr

    def _repr_html_(self):
        return f'<pre><code>{escape(self.ptr)}</code></pre>'


class AGMResultsQuaternions:
    """AGM results quaternions object."""
    HTML_MAX_LINES = 25

    def __init__(self, quaternions):
        self._raw = quaternions

        self.data = [
            [dt(time), (float(qx), float(qy), float(qz), float(qw))]
            for line in quaternions.splitlines()[1:]  # Skip header
            for time, qx, qy, qz, qw in [line.split(',')]
        ]

    def __repr__(self):
        return '\n'.join(
            f'{t} | {x:.16f} | {y:0.16f} | {z:.16f} | {w:.16f}'
            for t, (x, y, z, w) in self.data
        )

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def _repr_html_(self):
        header = '<tr><th>time</th><th>qx</th><th>qy</th><th>qz</th><th>qw</tr>'
        lines = ''.join([
            f'<tr><td><em>{t}</em></td><td>{x}</td>'
            f'<td>{y}</td><td>{z}</td><td>{w}</td></tr>'
            for t, (x, y, z, w) in self.data[:self.HTML_MAX_LINES]
        ])

        if len(self) > self.HTML_MAX_LINES:
            lines += (
                '<tfoot>'
                '<tr><td>&hellip;</td><td>&hellip;</td><td>&hellip;</td>'
                '<td>&hellip;</td><td>&hellip;</td></tr>'
                '<tr><td colspan="5" style="text-align: center;">'
                '<em>Use <code>print()</code> to display all elements.</em>'
                '</td></tr></tfoot>'
            )

        return '<table>' + header + lines + '</table>'


class AGMResultsFile:
    """AGM results file object (CK or resolved PTR)."""
    EXT = None   # File extension
    PATH = None  # Results path key

    def __init__(self, res):
        if cache := res['cache']:
            self.fname = Path(cache['location']) / (cache['md5_hash'] + self.EXT)
        else:
            key = res['results'][self.PATH].split('/')[1]
            self.fname = Path(f'AGM_{key}{self.EXT}')

        if '://' in (url := res['endpoint']):
            protocol, uri = url.split('://')
            self.url = protocol + '://' + uri.split('/')[0] + res['results'][self.PATH]
        else:
            self.url = None

    def __str__(self):
        return str(self.fname) if self.fname.exists() else self.url

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __iter__(self):
        if not self.fname.exists():
            self.download()

        yield str(self.fname)  # Load-able by spiceypy

    def download(self):
        """Download the file."""
        if self.url is None:
            raise ValueError('Endpoint is not a remote URL.')

        # Download the file
        request.urlretrieve(self.url, self.fname)

        return self.fname

    def save(self, fout, overwrite=False):
        """Save the file into an new location."""
        fout = Path(fout)

        if not overwrite and fout.exists():
            raise FileExistsError(fout)

        for f in self:
            content = Path(f).read_bytes()
            fout.write_bytes(content)

        self.fname = fout
        return self.fname


class AGMResultsCK(AGMResultsFile):
    """AGM results CK object."""
    EXT = '.ck'
    PATH = 'ck_path'


class AGMResultsResolvedPTR(AGMResultsFile):
    """AGM results resolved PTR object."""
    EXT = '.ptx'
    PATH = 'ptr_resolved_path'

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}\n\n{self.content}'

    @property
    def content(self):
        """Resolved PTR file content."""
        if not self.fname.exists():
            self.download()
        return self.fname.read_text(encoding='utf-8')


class AGMResultsLog:
    """AGM results log object."""
    HTML_MAX_LINES = 25
    line = re.compile(r'\[(\w+)\]\s*<([\w\s><]+)>\s*([\w\s\/\.\:+\-_"]+)')

    def __init__(self, log, session_id=None):
        self.log = [
            (flag, tag.replace('AGE> <', ''), msg)
            for line in log.replace('\\"', '"').split('\n')
            for flag, tag, msg in self.line.findall(line)
        ]

        self.session_id = session_id

    def __repr__(self):
        return '\n'.join(' | '.join(line) for line in self.log)

    def _repr_html_(self):
        session_id = (
            '<ul style="color:#777">'
            f'<li><b>Session ID:</b> <code>{self.session_id}</code></li>'
            '</ul>\n'
        ) if self.session_id is not None else ''

        lines = ''.join([
            f'<tr><td>{flag}</td><td>{tag}</td>'
            f'<td style="text-align: left;"><em>{escape(msg)}</em></td></tr>'
            for flag, tag, msg in self.log[:self.HTML_MAX_LINES]
        ])

        if len(self) > self.HTML_MAX_LINES:
            lines += (
                '<tfoot>'
                '<tr><td>&hellip;</td><td>&hellip;</td>'
                '<td style="text-align: left;">&hellip;</td></tr>'
                '<tr><td colspan="3" style="text-align: center;">'
                '<em>Use <code>print()</code> to display all elements.</em>'
                '</td></tr></tfoot>'
            )

        return session_id + '<table>' + lines + '</table>'

    def __len__(self):
        return len(self.log)

    def __iter__(self):
        return iter(self.log)

    def __getitem__(self, item):
        return self.log[item]


class AGMResultsStatus:
    """AGM results status object"""
    def __init__(self, success):
        self.success = success

    def __repr__(self):
        return 'Success' if self.success else 'Failure'

    def _repr_html_(self):
        return (
            f'<p><span style="color: {self.color}">{self.symbol}</span> <b>{self}</b></p>'
        )

    @property
    def failure(self):
        """Failure flag."""
        return not self.success

    @property
    def symbol(self):
        """Status symbol."""
        return '✔' if self.success else '✘'

    @property
    def color(self):
        """Status color."""
        return '#2ca02c' if self.success else '#d62728'
