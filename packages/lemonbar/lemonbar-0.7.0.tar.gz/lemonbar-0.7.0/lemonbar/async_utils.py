import asyncio
from typing import TypeVar, Coroutine, Tuple, List, Iterable, Awaitable

T = TypeVar('T')
V = TypeVar('V')


async def gather_if(gathers: Iterable[Tuple[Coroutine, Coroutine]]) -> List[T]:
    """
    Effectively gathers coroutine results if they pass a certain condition

    :param gathers: An iterable of tuples (condition, gather_if_passed)
    :return: A list of the all the second coroutine results
      that passed the condition returned from the first coroutine
    """
    conditional_tasks: Iterable[Tuple[Coroutine, Coroutine]] \
        = [(condition, gather) for condition, gather in gathers]

    conditional_results = await asyncio.gather(*[task for task, _ in conditional_tasks])

    gather_tasks: List[Coroutine] = []
    for index, (conditional_task, gather) in enumerate(conditional_tasks):
        task_result = conditional_results[index]
        if task_result:
            gather_tasks.append(gather)

    return await asyncio.gather(*gather_tasks)


async def state_kept_await(state: T, coroutine: Awaitable[V]) -> Tuple[T, V]:
    try:
        return state, await coroutine
    except Exception as e:
        return state, e
