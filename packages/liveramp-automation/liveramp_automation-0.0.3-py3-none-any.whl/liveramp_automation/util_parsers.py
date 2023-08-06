from ctypes import cast
from typing import Dict, Any

from pytest_bdd.parsers import StepParser
import parse as base_parse

EXTRA_TYPES = {}


class ParseUtils(StepParser):
    """parse step parser."""

    # This is a Factory method pattern to parse the steps in the BDD scenarios
    def __init__(self, name, *args):
        """Compile parse expression."""
        super(ParseUtils, self).__init__(name)
        self.parser = base_parse.compile(self.name, *args, extra_types=EXTRA_TYPES)

    def parse_arguments(self, name: str) -> dict[str, Any]:
        """Get step arguments.
        :return: `dict` of step arguments
        """
        return cast(Dict[str, Any], self.parser.parse(name).named)

    def is_matching(self, name):
        """Match given name with the step name."""
        try:
            return bool(self.parser.parse(name))
        except ValueError:
            return False
