"""PTR Command Line Interface module."""

import sys
from argparse import ArgumentParser
from pathlib import Path

from .agm import agm_simulation
from .esa.export import export_timeline
from .esa.pointing_tool import JUICE_POINTING_TOOL


def cli_juice_agm(argv=None):
    """CLI JUICE PTR validation with AGM.

    By default, the metakernel used by AGM is ``JUICE CREMA 5.1 150lb_23_1``.
    You can change this parameter with ``--mk`` flag.

    AGM produced CK file are cached but you can download
    it explicitly if you want with a ``--ck`` flag.

    """
    parser = ArgumentParser(description='Check ESA/JUICE PTR validity with AGM.')
    parser.add_argument('ptr', nargs='?', help='PTR/PTX input file.')
    parser.add_argument('--mk', metavar='METAKERNEL',
                        default='JUICE CREMA 5.1 150lb_23_1',
                        help='Metakernel to use with AGM '
                             '(default: "JUICE CREMA 5.1 150lb_23_1").')
    parser.add_argument('--endpoint', metavar='URL', default='JUICE_API',
                        help='AGM API endpoint URL (default: `JUICE_API`).')
    parser.add_argument('--quaternions', action='store_true',
                        help='Display computed quaternions (optional).')
    parser.add_argument('--ck', metavar='FILENAME',
                        help='CK output filename (optional).')
    parser.add_argument('--ptr-resolved', metavar='FILENAME',
                        help='Resolved PTR output filename (optional).')
    parser.add_argument('--log', action='store_true',
                        help='Display AGM log (optional).')
    parser.add_argument('--no-cache', action='store_false',
                        help='Disable cache (optional).')
    parser.add_argument('--show-contexts', action='store_true',
                        help='Show available metakernel contexts.')

    args, _ = parser.parse_known_args(argv)

    # List available context
    if args.show_contexts:
        sys.stdout.write('\n- '.join([
            'JUICE_API metakernel contexts available:',
            *[str(context) for context in JUICE_POINTING_TOOL]
        ]))
        sys.stdout.write('\n')
        return

    # Check if a PTR was supplied
    if not args.ptr:
        sys.stderr.write('PTR file is missing\n')
        sys.exit(1)

    # Check if the file exists
    if not Path(args.ptr).exists():
        sys.stderr.write(f'PTR not found: {args.ptr}\n')
        sys.exit(1)

    # Start AGM simulation
    res = agm_simulation(args.mk, args.ptr, args.endpoint, cache=args.no_cache)
    sys.stdout.write(f'AGM simulation: {res.status}\n')

    if res.success:
        if args.log:
            sys.stdout.write('Log:\n' + repr(res.log) + '\n')

        if args.quaternions:
            sys.stdout.write(f'Quaternions:\n{repr(res.quaternions)}\n')

        if args.ck:
            res.ck.save(args.ck)
            sys.stdout.write(f'AGM CK saved in `{args.ck}`.\n')

        if args.ptr_resolved:
            res.ptr_resolved.save(args.ptr_resolved)
            sys.stdout.write(f'AGM resolved PTR saved in `{args.ptr_resolved}`.\n')

    else:
        sys.stderr.write('Log:\n' + repr(res.log) + '\n')
        sys.exit(1)


def cli_ptr_to_seg(argv=None):
    """CLI to convert a PTR to a segmentation file."""
    parser = ArgumentParser(description='Convert PTR to segmentation file.')
    parser.add_argument('ptr', help='PTR/PTX input file.')
    parser.add_argument('-o', '--output', metavar='FILENAME', default=None,
                        help='Custom output filename (default: PTR filename).')
    parser.add_argument('--json', action='store_true',
                        help='Export as JSON (default CSV if not provided).')
    parser.add_argument('--subgroup', default='',
                        help='Subgroup field (default: `<EMPTY>`).')
    parser.add_argument('--source', default='GENERIC',
                        help='Source field (default: `GENERIC`).')
    parser.add_argument('--crema', default='CREMA_5_0',
                        help='Trajectory crema keyword in JSON export '
                        '(default: `CREMA_5_0`).')
    parser.add_argument('--timeline', default='LOCAL',
                        help='Timeline keyword in JSON export '
                        '(default: `LOCAL`).')

    args, _ = parser.parse_known_args(argv)

    # Check if the file exists
    if not (ptr := Path(args.ptr)).exists():
        sys.stderr.write(f'PTR not found: {ptr}\n')
        sys.exit(1)

    # Extract filename
    if args.output:
        fname = Path(args.output)
        if (ext := fname.suffix.lower()) not in ['.csv', '.json']:
            sys.stderr.write(
                f'Segmentation output file must be a CSV of JSON file. Provided: {ext}\n')
            sys.exit(1)
    else:
        ext = 'json' if args.json else 'csv'
        fname = ptr.parent / f'{ptr.stem}.{ext}'

    # Export PTR to segmentation
    export_timeline(fname, ptr, subgroup=args.subgroup, source=args.source,
                    crema=args.crema, timeline=args.timeline)

    sys.stdout.write(f'Segmentation saved in: {fname}\n')
