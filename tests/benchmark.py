"""
runs a set of GET calls against two different APIs and compares how long it takes.
Targeted at '/' and '/api' because this app returns different data for the two
"""
from timeit import default_timer as timer
import requests

num_iterations = 20
num_sets = 1
target_ip = "192.168.1.32"


def the_func(target_path, target_ip):
    url = "http://" + target_ip + target_path
    # print(url)
    requests.get(url)


def time_it(path, test_target_ip, test_num_sets, test_num_iterations):

    print(
        "Testing Path:"
        + path
        + " Sets:"
        + str(test_num_sets)
        + " iterations:"
        + str(test_num_iterations)
    )
    start = timer()
    for this_set in range(test_num_sets):
        for i in range(test_num_iterations):
            the_func(path, test_target_ip)
    end = timer()
    return end - start


run_time = time_it("/", target_ip, num_sets, num_iterations)
print(" Time:" + str(run_time), " - ", str(run_time / num_sets / num_iterations))

run_time = time_it("/?", target_ip, num_sets, num_iterations)
print(" Time:" + str(run_time), " - ", str(run_time / num_sets / num_iterations))

run_time = time_it("/?out_0=off&out_1=on", target_ip, num_sets, num_iterations)
print(" Time:" + str(run_time), " - ", str(run_time / num_sets / num_iterations))

run_time = time_it("/api/", target_ip, num_sets, num_iterations)
print(" Time:" + str(run_time), " - ", str(run_time / num_sets / num_iterations))
