from functools import wraps
import time
from .builder import context_name, DataFrame
from datetime import datetime
from .file_mgt import get_datetime_str


def recursive_records_count(count, data):
    if isinstance(data, dict):
        if context_name in data:
            count += len(data[context_name])
        else:
            print("not acceptable context_name")
            # raise ValueError()
            return count

    elif isinstance(data, DataFrame):
        count += data.shape[0]
    elif isinstance(data, str):
        count += 0
    elif isinstance(data, list):
        for item in data:
            count = recursive_records_count(count, item)
    else:
        raise ValueError("currently only accept list, str, json and pandas data type")
    
    return count



def transform_wrapper(func):
    """
    Usage
    ----------------------------
    class Calculator:
        @transform_wrapper
        def calculate_something(self, num):
            total = sum((x for x in range(0, num**2)))
            return total

        def __repr__(self):
            return f'calc_object:{id(self)}'
    Reference
    ---------------------------
    https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        self = args[0]

        # Calculate the execution time
        start_time = time.perf_counter()
        self.start_datetime = get_datetime_str(format="%Y-%m-%d %H:%M:%S")

        # print processing label
        print(f"Processing {self.node_name}, started at {self.start_datetime} ...") if self.print_task_result else ""

        # execute the transform function
        result = func(*args, **kwargs)

        # Calcuate the end time
        end_time = time.perf_counter()
        total_time = end_time - start_time
        self.end_datetime = get_datetime_str(format="%Y-%m-%d %H:%M:%S")
        # print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')


        # Adding the execution time to the transformer
        self.total_time = total_time
        
        # print(self)
        # parallelTransformer will make it run double times, not solved yet

        #count the number of records in input and output of the func:
        self.total_input = recursive_records_count(0, args[1])
        self.total_output = recursive_records_count(0, result)

        if self.node_name:
            print(f"    - take time {total_time:.4f} seconds, total input records {self.total_input}, total output records {self.total_output}") if self.print_task_result else ""

            # print(f"stop with breakpoint at {transformer.node_name}") if self.print_task_result else ""
        # print(f"{self.node_name}: take time {total_time:.4f} seconds, total input records {self.total_input}, total output records {self.total_output}")

        return result

    return func_wrapper


