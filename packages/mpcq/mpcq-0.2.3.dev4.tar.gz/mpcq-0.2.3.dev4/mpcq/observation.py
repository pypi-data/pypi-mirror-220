import dataclasses
import decimal
from enum import Enum
from typing import Optional

import astropy.time


class ObservationStatus(Enum):
    Published = 1
    Pending = 2
    IsolatedTrackletFile = 3

    @classmethod
    def _from_db_value(cls, val: str):
        return {
            "P": ObservationStatus.Published,
            "p": ObservationStatus.Pending,
            "I": ObservationStatus.IsolatedTrackletFile,
        }[val]


@dataclasses.dataclass
class Observation:
    """
    Represents a single entry in the MPC Observations 'obs_sbn' table.
    """

    # The internal primary key, an opaque integer.
    mpc_id: int

    # See ObservationStatus.
    status: ObservationStatus

    # The three-character code which identifies the observatory which
    # made the observation.
    obscode: str

    # The single-character code which identifies which filter was used
    # when observing.
    filter_band: str

    # An identifier for the object being observed, for example '2022 AJ2'.
    unpacked_provisional_designation: str

    # The time of the observation. This is submitted to MPC, and does
    # not have a well-defined meaning. In general, it ought to be the
    # midpoint of the exposure that the observation came from, but
    # sometimes it seems to be the start of the exposure. For
    # observations which come from stacks of multiple exposures it is
    # even less well-defined.
    timestamp: astropy.time.Time

    # Right ascension of the observation in the J2000 frame.
    ra: decimal.Decimal
    # Error in the right ascension.
    ra_rms: Optional[decimal.Decimal]

    # Declination of the observation in the J2000 frame.
    dec: decimal.Decimal
    # Error in the declination.
    dec_rms: Optional[decimal.Decimal]

    # Observed magnitude of the object.
    mag: Optional[decimal.Decimal]
    # Error in the magnitude estimate.
    mag_rms: Optional[decimal.Decimal]

    # Submission Properties
    # MPC-assigned ID for the submission
    submission_id: str

    # Time when the observation was first submitted to MPC and ingested
    # Apparently this can be None... maybe for older observations???
    created_at: Optional[astropy.time.Time]
    # Time when the last update to this observations was made, None if
    # never updated beyond initial creation
    updated_at: Optional[astropy.time.Time]
