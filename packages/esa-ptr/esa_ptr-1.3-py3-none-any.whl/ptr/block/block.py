"""PTR blocks module."""

from ..datetime.window import WithDatetimeWindow
from ..element import Element
from ..metadata import WithMetadata


class ElementBlock(Element, WithDatetimeWindow, WithMetadata):
    """PTR block element.

    Parameters
    ----------
    ref: str
        Block reference attribute.
    start: string, datetime.datetime or numpy.datetime64
        Block start time.
    end: string, datetime.datetime or numpy.datetime64
        Block end time.
    *elements:
        Other block elements.

    metadata: str, int, float, ptr.Element, tuple or list, optional
        Block metadata element(s).
    description: str or list, optional
        Block description, put as a xml-comment on top of the element.
    **attrs:
        Block keywords attributes.

    """

    def __init__(self, ref, start, end, *elements,
                 metadata=None, description=None, **attrs):
        super().__init__('block', ref=ref, description=description, **attrs)

        if metadata:
            self.add_metadata(metadata)

        self.set_window(start, end)

        for element in elements:
            self.append(element)

        # Freeze the top element list
        self.freeze()

        # Init parents timelines list
        self._timelines = []

    def link_timeline(self, timeline):
        """Link a parent timeline to a block."""
        self._timelines.append(timeline)

    def unlink_timeline(self, timeline):
        """Unlink a parent timeline to a block."""
        self._timelines.remove(timeline)

    def edit(self, *, start=None, end=None):
        """Edit block temporal window boundaries.

        Parameters
        ----------
        start: str, datetime.datetime or datetime.timedelta
            Start time absolute or relative offset.

        end: str, datetime.datetime or datetime.timedelta
            End time absolute or relative offset.

        Raises
        ------
        BlockOverlapError
            If the new block is not compatible with its
            parent timelines.

        Warning
        -------
        This operation change the duration of the block.

        """
        # Store original start and end times
        original_start, original_end = self.start.iso, self.end.iso

        # Edit times
        super().edit(start=start, end=end)

        # Tag the new block (to avoid block duplicates)
        self.attrs['block'] = 'new'

        # Check if the new block is compatible with their parent timeline
        for timeline in self._timelines:
            for block in timeline:
                if block != self and block & self:
                    # Untag the new block
                    del self.attrs['block']

                    # Set error message
                    err_msg = f'New block:\n{self}\n\nintersects:\n\n{block}'

                    # Fallback to the original datetime
                    super().edit(start=original_start, end=original_end)

                    # Raise overlap error
                    raise BlockOverlapError(err_msg)

            # Re-sort the blocks in chronological order
            timeline.sort()

        # Untag the new block
        del self.attrs['block']

        return self

    def offset(self, offset, *, ref='start'):
        """Offset block temporal window.

        Parameters
        ----------
        offset: str datetime.timedelta or datetime.datetime
            Global or relative offset.

        ref: str, optional
            Boundary reference for relative offset.
            Only ``start|end|center`` are accepted

        Raises
        ------
        BlockOverlapError
            If the new block is not compatible with its
            parent timelines.

        Note
        ----
        This operation does not change the duration of the block.

        """
        # Store original start and end times
        original_start, original_end = self.start.iso, self.end.iso

        # Offset times
        super().offset(offset, ref=ref)

        # Tag the new block
        self.attrs['block'] = 'new'

        # Check if the new block is compatible with their parent timeline
        for timeline in self._timelines:
            for block in timeline:
                if block != self and block & self:
                    # Untag the new block
                    del self.attrs['block']

                    # Set error message
                    err_msg = f'New block:\n{self}\n\nintersects:\n\n{block}'

                    # Fallback to the original datetime
                    super().edit(start=original_start, end=original_end)

                    # Raise overlap error
                    raise BlockOverlapError(err_msg)

            # Re-sort the blocks in chronological order
            timeline.sort()

        # Untag the new block
        del self.attrs['block']

        return self

    def split(self, time, *, gap=None, ref='start'):
        """Split block in two blocks.

        Parameters
        ----------
        time: str or datetime.datetime
            Splitting datetime.

        gap: str, optional
            Time delta gap between the blocks.

        ref: str, optional
            Reference location of the gap with respect to provided time.
            Only ``start|end|center`` are accepted

        Returns
        -------
        ElementBlock, ElementBlock
            Two copy of the original block in each time window.

        Raises
        ------
        KeyError
            If the reference keyword is invalid.
        ValueError
            If the gap is too large for the block.

        Warning
        -------
        This operation change the duration of the block.

        """
        block_1, block_2 = super().split(time, gap=gap, ref=ref)

        for timeline in self._timelines:
            for i, block in enumerate(timeline):
                if block == self:
                    # Remove the old block from the timeline
                    timeline.pop(i)
                    break

            # Insert the new blocks (re-sorted internally)
            timeline.append(block_1)
            timeline.append(block_2)

        return block_1, block_2


class BlockOverlapError(Exception):
    """Block overlap error."""
