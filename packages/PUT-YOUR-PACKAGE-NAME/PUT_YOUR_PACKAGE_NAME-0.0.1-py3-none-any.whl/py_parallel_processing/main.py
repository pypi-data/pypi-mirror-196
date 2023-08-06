

def py_parallel_pools(some_func, params):
    """
    함수를 병렬처리하는 함수입니다.

    Args:
        some_func: 병렬처리할 함수
        params: 함수의 인자로 사용될 리스트

    Returns:
        병렬처리된 함수의 반환값들을 리스트 형태로 반환합니다.
    """
    from pathos.pools import ProcessPool
    from tqdm import tqdm

    with ProcessPool() as pool:
        # 함수를 병렬처리하면서 진행상황 바(progress bar)를 표시합니다.
        return_variables = list(
            tqdm(pool.imap(some_func, params), total=len(params)))
        # 반환값이 None인 경우는 리스트에서 제외합니다.
        return_variables = [i for i in return_variables if i is not None]
    return return_variables
