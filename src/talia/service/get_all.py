"""This is a file which is imported by the main file and ONLY
 the main file. This avoids circular imports and allows
 the list of services to be created

All services imported should be in alphabetical order"""

from talia.service import (
    gerald_response,
    ping_response
)