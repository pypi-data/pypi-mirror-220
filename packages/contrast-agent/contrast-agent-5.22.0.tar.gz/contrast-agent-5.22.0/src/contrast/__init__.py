# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import print_function
import os
import sys
from contrast.agent.assess.string_tracker import StringTracker
from contrast.utils.context_tracker import ContextTracker
from contrast.version import __version__

from contrast.assess_extensions import cs_str

CS__CONTEXT_TRACKER = ContextTracker()

STRING_TRACKER = StringTracker()

# PERF: These values are constant for the lifetime of the agent,
# so we compute them only once instead of potentially computing
# them hundreds of times.
AGENT_CURR_WORKING_DIR = os.getcwd()
SORTED_SYS_PATH = sorted(sys.path, key=len, reverse=True)

# --- import aliases ---

from contrast.agent.assess.utils import get_properties  # noqa

TELEMETRY = None


def telemetry_disabled() -> bool:
    return os.environ.get("CONTRAST_AGENT_TELEMETRY_OPTOUT", "").lower() in [
        "1",
        "true",
    ]


def get_canonical_version() -> str:
    return ".".join(__version__.split(".")[:3])
