import sys

from Services.Task_creater import create_random_tasks
from Services.task_manager import TaskManager
from Utils.Random_utils import Random_util
from Utils.layout_utils import create_layout_env, distance_between
from containers import Container


def sort():
    rand = Random_util(0)
    (layout, delivery_sports, number_of_grounds, number_of_customers), truck_pos = create_layout_env(15, 5, rand, 1, 0.5, True)

    tasks = create_random_tasks(delivery_sports, 100, load_img=False)

    manager = TaskManager()

    sorted_tasks = manager.sort_tasks(tasks)

    prev = sys.maxsize
    for task in sorted_tasks:
        dist = distance_between(truck_pos, (task.rect.x, task.rect.y))
        assert dist <= prev
        prev = dist



if __name__ == "__main__":
    # setup dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    sort()
    print("Everything is correct")