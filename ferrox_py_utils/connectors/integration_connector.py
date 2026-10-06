import asyncio
from collections.abc import Callable, Coroutine
from functools import wraps
from typing import Any, TypeVar, cast

from ferrox_py.concurrency.singleflight import SingleflightManager
from ferrox_py.core.errors import FerroxError
from ferrox_py.resilience.circuit_breaker import DistributedCircuitBreaker
from ferrox_py.security.distributed_locks import DistributedLockManager
from ferrox_py.security.rate_limiting import DistributedRateLimiter

T = TypeVar("T")

class IntegrationConnector:
    """Base class for integration connectors"""
    
    def __init__(self, 
                 lock_manager: DistributedLockManager, 
                 rate_limiter: DistributedRateLimiter, 
                 circuit_breaker: DistributedCircuitBreaker,
                 singleflight_manager: SingleflightManager) -> None:
        self.lock_manager = lock_manager
        self.rate_limiter = rate_limiter
        self.circuit_breaker = circuit_breaker
        self.singleflight_manager = singleflight_manager
        
def connector_policy(provider: str, max_concurrency: int = 1, daily_quota: int = 30000, failure_budget: int = 200) -> Callable[..., Any]:
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(self: IntegrationConnector, tenant_id: str, *args: Any, **kwargs: Any) -> T:
            # Check rate limiting daily quota
            allowed = await self.rate_limiter.check_and_consume(
                key=f"{provider}:{tenant_id}", 
                max_concurrency=max_concurrency, 
                daily_limit=daily_quota, 
                priority="interactive"
            )
            
            if not allowed:
                raise FerroxError(message=f"Daily quota exceeded for provider {provider}", status_code=429)
                
            # Circuit Breaker execution block
            async def breaker_execution() -> T:
                # Concurrency limit via Lock
                lock_key = f"lock:{provider}:{tenant_id}"
                async with self.lock_manager.acquire(lock_key, timeout_ms=max_concurrency*5000):
                    return await func(self, tenant_id, *args, **kwargs)

            return cast(T, await self.circuit_breaker.call(tenant_id, provider, breaker_execution))
            
        return wrapper
    return decorator

def resilient_sync(singleflight: bool = True, retry: int = 3, backoff: str = "exponential") -> Callable[..., Any]:
    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(self: IntegrationConnector, tenant_id: str, *args: Any, **kwargs: Any) -> T:
            async def execute_with_retries() -> T:
                last_error: Exception | None = None
                for attempt in range(retry):
                    try:
                        return await func(self, tenant_id, *args, **kwargs)
                    except Exception as e:
                        last_error = e
                        if attempt < retry - 1:
                            delay = 2 ** attempt if backoff == "exponential" else 1
                            await asyncio.sleep(delay)
                if last_error:
                    raise last_error
                raise RuntimeError("Unexpected retry failure")
                
            if singleflight:
                key = f"sync:{func.__name__}:{tenant_id}"
                return cast(T, await self.singleflight_manager.do(key, execute_with_retries))
            else:
                return await execute_with_retries()
                
        return wrapper
    return decorator
