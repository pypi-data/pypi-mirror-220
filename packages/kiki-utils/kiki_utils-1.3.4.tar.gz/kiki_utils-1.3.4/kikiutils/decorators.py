import time

from asyncio import create_task, sleep, Task
from functools import wraps
from inspect import iscoroutinefunction
from threading import Timer
from typing import Any, Callable, Coroutine, Optional, overload

from .typehint import P, T


def debounce(delay: float | int):
    """Defers the execution of a function until it is not called again within the specified time since the last call.

    Supports async and sync function.
    """

    def decorator(view_func: Callable[P, T]) -> Callable[P, None]:
        if iscoroutinefunction(view_func):
            task: Optional[Task] = None

            @wraps(view_func)
            def awrapped_view(*args, **kwargs):
                nonlocal task

                if task is not None:
                    task.cancel()

                async def aexec():
                    await sleep(delay)
                    await view_func(*args, **kwargs)

                task = create_task(aexec())
            return awrapped_view

        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            def exec():
                view_func(*args, **kwargs)

            if hasattr(wrapped_view, '_timer'):
                wrapped_view._timer.cancel()

            wrapped_view._timer = Timer(delay, exec)
            wrapped_view._timer.start()
        return wrapped_view
    return decorator


@overload
def show_cost_time(view_func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, T]]: ...
@overload
def show_cost_time(view_func: Callable[P, T]) -> Callable[P, T]: ...
def show_cost_time(view_func):
    """Run the function and show cost time.

    Supports async and sync function.
    """

    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            se = time.time()
            result = await view_func(*args, **kwargs)
            print(f'Function {view_func.__name__} cost time is {time.time() - se} s')
            return result
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        se = time.time()
        result = view_func(*args, **kwargs)
        print(f'Function {view_func.__name__} cost time is {time.time() - se} s')
        return result
    return wrapped_view


@overload
def try_and_get_bool(view_func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, bool]]: ...
@overload
def try_and_get_bool(view_func: Callable[P, T]) -> Callable[P, bool]: ...
def try_and_get_bool(view_func):
    """Run the function use try/catch.

    Returns False if there was an error. Otherwise return True.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                await view_func(*args, **kwargs)
                return True
            except:
                return False
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            view_func(*args, **kwargs)
            return True
        except:
            return False
    return wrapped_view


@overload
def try_and_get_data(view_func: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, Coroutine[Any, Any, Optional[T]]]: ...
@overload
def try_and_get_data(view_func: Callable[P, T]) -> Callable[P, Optional[T]]: ...
def try_and_get_data(view_func):
    """Run the function use try/catch.

    Returns None if there was an error. Otherwise return the function result.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                return await view_func(*args, **kwargs)
            except:
                pass
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except:
            pass
    return wrapped_view
