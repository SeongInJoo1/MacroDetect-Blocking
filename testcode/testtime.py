import time

# Get the current time as a Unix timestamp
current_time = time.time()

# Convert the Unix timestamp to a local time string
local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))

# Print the local time
print("The current time is:", local_time)
time.sleep(5)

times = time.time()

# Convert the Unix timestamp to a local time string
local = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(times))

# Print the local time
print("The last time is:", local)

a = local_time - local
print(a)


