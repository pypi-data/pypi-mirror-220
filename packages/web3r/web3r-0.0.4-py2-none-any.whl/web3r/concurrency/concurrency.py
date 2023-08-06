from tqdm import tqdm
import concurrent.futures

class ConcurrentExecutor:
    def __init__(self, target_func):
        self.target_func = target_func

    def execute_concurrently(self, workers: int, items: list, desc: str):
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as thread_executor:
            list(tqdm(thread_executor.map(self.target_func, *zip(*items)), total=len(items), desc=f'Thread: {desc}'))
