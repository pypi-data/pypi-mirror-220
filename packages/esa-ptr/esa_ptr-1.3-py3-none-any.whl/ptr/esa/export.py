"""ESA export functions."""

from datetime import datetime
from json import dumps
from pathlib import Path

from ..datetime import iso
from ..ptx import read_ptr


def export_timeline(fname, ptr, subgroup='', source='GENERIC', **kwargs):
    """Export a PTR observation blocks into segments.

    CSV and JSON files are natively compatible with the JUICE timeline tool:

    .. code-block:: text

        https://juicesoc.esac.esa.int/tm/?trajectory=CREMA_5_0

    Parameters
    ----------
    fname: str or pathlib.Path
        Output filename. Currently, only ``.json`` and ``.csv`` are supported.

    ptr: str or pathlib.Path
        PTR text or file name.

    subgroup: str, optional
        Subgroup keyword (default: ``<EMPTY>``).

    source: str, optional
        Source / working group entry (default: ``GENERIC``).

    **kwargs:
        JSON output extra keywords, defaults:
        - ``crema = 'CREMA_5_0'``
        - ``timeline = 'LOCAL'``
        - ``creation_date = None``
        - ``overwritten = False``

    Returns
    -------
    pathlib.Path
        Output filename.

    Raises
    ------
    ValueError
        If the provided filename does not end with ``.json`` or ``.csv``.

    See Also
    --------
    extract_segments
    format_csv
    format_json

    """
    # Parse PTR
    ptr = read_ptr(ptr)

    # Extract segments list: [[NAME, START_TIME, STOP_TIME, SUBGROUP, SOURCE], ...]
    segments = extract_segments(ptr, subgroup=subgroup, source=source)

    # Export in a output file
    fname = Path(fname)
    ext = fname.suffix.lower()

    if ext == '.csv':
        content = format_csv(segments)

    elif ext == '.json':
        content = format_json(segments, fname.stem, **kwargs)

    else:
        raise ValueError('The output file must be a JSON or a CSV file.')

    # Create parents folder if needed
    fname.parent.mkdir(parents=True, exist_ok=True)

    # Save the segments content
    fname.write_text(content, encoding='utf-8')

    return fname


def extract_segments(ptr, subgroup='', source='GENERIC'):
    """Extract PTR observation blocks as segment windows.

    Segment format:

    ``[NAME, START_TIME, STOP_TIME, SUBGROUP, SOURCE]``

    Parameters
    ----------
    ptr: PointingRequestMessage
        Parsed pointing request message.
    subgroup: str, optional
        Subgroup keyword (default: ``<EMPTY>``).
    source: str, optional
        Source / working group entry (default: ``GENERIC``).

    Returns
    -------
    list
        List of segments.

    Note
    ----
    - The ``NAME`` keyword is extracted from the comment ``OBS_NAME``
      in the metadata comment properties if present or set to
      ``PTR_OBS_BLOCK`` if not present.
      If a ``OBS_ID`` comment property is present, if will be appended
      to the ``NAME`` as ``{OBS_NAME}_{OBS_ID}``.

    - ``START`` and ``STOP`` times are return as ISO format: ``2032-07-08T15:53:52.350Z``

    - The ``SUBGROUP`` is optional.

    - The ``SOURCE`` can be empty. If a PTR block has the ``PRIME`` property in the
      metadata, ``SOURCE`` uses that value for the given block.

    See Also
    --------
    export_timeline

    """
    segments = []
    for block in ptr:
        # Assign the default source to the segment source.
        seg_source = source
        seg_name = 'PTR_OBS_BLOCK'
        seg_subgroup = subgroup

        # Check if the block contains information about the observation
        if meta := block.metadata:
            prop = meta.properties

            if 'OBS_NAME' in prop:
                seg_subgroup = prop['OBS_NAME']
                seg_name = prop['OBS_NAME']

            if 'PRIME' in prop:
                seg_source = prop['PRIME']
                if seg_source != 'SOC':
                    seg_name = f"{prop['PRIME']}_PRIME_OBSERVATION"
                else:
                    seg_name = prop['OBS_NAME']

        # Append
        segments.append([
            seg_name,
            iso(block.start.datetime),
            iso(block.end.datetime),
            seg_subgroup,
            seg_source,
        ])

    return segments


def format_csv(segments, header='# name, t_start, t_end, subgroup, source'):
    """Format segments as a CSV string.

    Parameters
    ----------
    segments: list
        List of events as: ``[NAME, START_TIME, STOP_TIME, SUBGROUP, SOURCE]``
    header: str, optional
        Optional file header.

    Returns
    -------
    str
        Formatted CSV string.

    Note
    ----
    The delimiter is a comma character (``,``).

    """
    if header:
        segments = [header.split(', ')] + segments

    return '\n'.join([','.join(event) for event in segments])


def format_json(segments, fname, crema='CREMA_5_0',
                timeline='LOCAL', creation_date=None,
                overwritten=False):
    """Format segments as a JSON string.

    Parameters
    ----------
    segments: list
        List of events as: ``[NAME, START_TIME, STOP_TIME, SUBGROUP, SOURCE]``
    crema: str, optional
        Top level ``crema`` keyword.
    timeline: str, optional
        Top level ``timeline`` keyword.
    creation_date: str or datetime.datetime, optional
        File creation datetime in ISO format. If none provided (default),
        the current datetime will be used.
    overwritten: bool, optional
        Segment event ``overwritten`` keyword.

    Returns
    -------
    str
        Formatted JSON string.

    Note
    ----
    The ``SUBGROUP`` field is used to store the name that will be displayed in the
    JUICE timeline tool. If none is provided, the ``NAME`` field will be used instead.

    """
    return dumps({
        'creationDate': iso(creation_date if creation_date else datetime.now()),
        'name': fname,
        'segments': [
            {
                'start': start,
                'end': stop,
                'segment_definition': name,
                'name': subgroup if subgroup else name,
                'overwritten': overwritten,
                'timeline': timeline,
                'source': source,
                'resources': [],
            }
            for name, start, stop, subgroup, source in segments
        ],
        'segmentGroups': [],
        'trajectory': crema,
        'localStoragePk': '',
    })
