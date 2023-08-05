import concurrent.futures
import asyncio

class FuturesStore:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        self.futures = {}

    def append(self, id:  str, func, *args, future_id=None, **kwargs):


        if future_id is None:
            # If no future_id is provided, store the function and arguments for later execution
            self.futures[id] = (func, args, kwargs)
        else:
            # If a future_id is provided, create a dependent future and store it for later execution
            dependent_future = (func, args, kwargs, future_id)
            self.futures[id] = dependent_future

        return id

    async def flush(self):
        async def run_task(future_id, future_details):
            if len(future_details) == 3:  # If there are no dependencies
                func, args, kwargs = future_details
                result = await func(*args, **kwargs)
            else:  # If there is a dependency
                func, args, kwargs, dependent_id = future_details
                if dependent_id in resolved_dependencies:  # If dependency is resolved
                    dependent_result = results[dependent_id]  # get the result from the parent future
                    result = await func(dependent_result, *args, **kwargs)
            results[future_id] = result
            resolved_dependencies.add(future_id)
            waiting_for_resolution.remove(future_id)

        results = {}
        resolved_dependencies = set()
        waiting_for_resolution = set(self.futures.keys())
        final_result = {'status': 'success'}

        try:
            tasks = [run_task(future_id, future_details) for future_id, future_details in self.futures.items()]
            await asyncio.gather(*tasks)
        except Exception as e:
            print(e)
            final_result['status'] = 'failed'
            final_result['error'] = str(e)
        
        self.futures.clear()

        return final_result



