from typing import Dict, Union
from hedra.core.graphs.events.base_event import BaseEvent
from hedra.core.graphs.hooks.registry.registry_types import ValidateHook
from collections import defaultdict
from hedra.core.graphs.hooks.registry.registry_types.hook import Hook
from hedra.logging import HedraLogger



class BaseHookVaidator:

    def __init__(self, metadata_string: str) -> None:
        self.logger = HedraLogger()
        self.logger.initialize()
        self.metadata_string: str = metadata_string
        self.hooks_by_name: Dict[str, Hook] = {}
        self.hooks_by_stage = defaultdict(dict)

    async def validate(self, hook: Union[ValidateHook, BaseEvent]):
        pass