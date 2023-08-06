# -*- coding: utf-8 -*-

from inspect import iscoroutinefunction
from typing import Any

from ffstreamer.module.errors import (
    ModuleCallbackCoroutineError,
    ModuleCallbackNotFoundError,
)
from ffstreamer.module.mixin._module_base import ModuleBase
from ffstreamer.module.variables import NAME_ON_FRAME


class ModuleFrame(ModuleBase):
    @property
    def has_on_frame(self) -> bool:
        return self.has(NAME_ON_FRAME)

    def on_frame(self, data: Any) -> Any:
        callback = self.get(NAME_ON_FRAME)
        if callback is None:
            raise ModuleCallbackNotFoundError(self.module_name, NAME_ON_FRAME)

        if iscoroutinefunction(callback):
            raise ModuleCallbackCoroutineError(self.module_name, NAME_ON_FRAME)

        return callback(data)
