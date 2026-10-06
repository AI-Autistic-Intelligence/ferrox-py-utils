import asyncio
from collections.abc import Callable
from typing import Any

from ferrox_py.core.errors import FerroxError
from ferrox_py.core.provider import injectable


class PipelineStep:
    def __init__(self, name: str, execute_fn: Callable[[Any], Any]):
        self.name = name
        self.execute_fn = execute_fn

@injectable()
class PipelineOrchestrator:
    async def execute_pipeline(self, name: str, initial_data: Any, steps: list[PipelineStep]) -> Any:
        print(f"Starting Pipeline: {name}")
        current_data = initial_data
        
        for step in steps:
            print(f"  -> Executing Step: {step.name}")
            try:
                if asyncio.iscoroutinefunction(step.execute_fn):
                    current_data = await step.execute_fn(current_data)
                else:
                    current_data = step.execute_fn(current_data)
            except Exception as e:
                raise FerroxError(message=f"Pipeline '{name}' failed at step '{step.name}': {e}", status_code=500)
                
        print(f"Pipeline '{name}' finished successfully.")
        return current_data
