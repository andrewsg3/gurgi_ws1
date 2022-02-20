import time
import threading
import concurrent.futures

#https://www.reddit.com/r/flask/comments/36ngb7/af_how_can_i_interrupt_an_infinite_while_loop_on/
#https://www.youtube.com/watch?v=IEEhzQoKtQU

start = time.perf_counter()



def do_something(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f"Done sleeping {seconds}."

# Method 1: use concurrent futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    ## Basic approach
    #f1 = executor.submit(do_something, 1)
    #f2 = executor.submit(do_something, 1)
    #print(f1.result())
    #print(f2.result())

    ## List comprehension
    # its = 10
    # results = [executor.submit(do_something, 1) for _ in range(its)]
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())

    ## List comprehension - variable length
    # secs = [5, 4, 3, 2, 1]
    # results = [executor.submit(do_something, sec) for sec in secs]
    # for f in concurrent.futures.as_completed(results):
    #     print(f.result())

    ## Use of executor.map
    # Makes it look like they completed at the same time.
    secs = [5,4,3,2,1]
    results = executor.map(do_something, secs) # Submits do_something with every value in secs as argument. 
    #Returns results in order they were started.
    for result in results:
        print(result)


# Method 2: use threads
# threads = []

# for _ in range(10):
#     t = threading.Thread(target=do_something, args=[1.5]) # Args is used to give an argument to the target function
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()


finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')