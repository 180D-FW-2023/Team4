import numpy as np
import matplotlib.pyplot as plt

def latency_meas_comp(file_name, title, fit):
    list = []
    with open(file_name, "r") as f:
        list = f.readlines()
    lines = []
    for line in list:
        if len(line) < 5:
            continue
        if line[1] == ":" and line[4] == ":":
            line = line.rstrip()
            line = float(line[5:])
            lines.append(line)
    np_time = np.array(lines)
    print(file_name)
    print("Average Latency: " + str(np.mean(np_time)))
    print("Min Latency: " + str(np.min(np_time)))
    print("Max Latency: " + str(np.max(np_time)))
    print("Amount of Data Points: " + str(len(np_time)))
    np_data_pts = np.arange(len(np_time)) * 50
    plt.scatter(np_data_pts, np_time, c="b")
    if fit:
        a, b = np.polyfit(np_data_pts, np_time, 1)
        plt.plot(np_data_pts, a*np_data_pts+b, c="r")
        print("Line of Best Fit: latency = " + str(a) + " * number of data points + " + str(b))
    plt.xlabel("number of data points")
    plt.ylabel("latency (s)")
    plt.title(title)
    plt.show()
    print()

def latency_meas_recv_send(file_name, title):
    list = []
    with open(file_name, "r") as f:
        list = f.readlines()
    lines = []
    for line in list:
        if len(line) < 5:
            continue
        if line[1] == ":" and line[4] == ":":
            line = line.rstrip()
            line = float(line[5:])
            lines.append(line)
    np_time = np.array(lines)
    print(file_name)
    print("Average Latency: " + str(np.mean(np_time)))
    print("Min Latency: " + str(np.min(np_time)))
    print("Max Latency: " + str(np.max(np_time)))
    print("Amount of Data Points: " + str(len(np_time)))

    time_stamps = lines[::-1]
    for i in range(len(time_stamps)):
        time_stamps[i] = sum(time_stamps[i:])
    time_stamps = time_stamps[::-1]
    np_time_stamps = np.array(time_stamps)
    plt.scatter(np_time_stamps, np_time)
    plt.xlabel("time (s)")
    plt.ylabel("latency (s)")
    plt.title(title)
    plt.show()

    print()

# Parallel vs NonParallel
latency_meas_comp("latency_server_comp_parallel.txt", "Latency of Computation for Step Count: Parallelization", False)
latency_meas_comp("latency_server_comp.txt", "Latency of Computation for Step Count: No Parallelization", False)
latency_meas_recv_send("latency_server_recv_parallel.txt", "Latency of Server Receiving Accelerometer Data: Parallelization")
latency_meas_recv_send("latency_server_recv.txt", "Latency of Server Receiving Accelerometer Data: No Parallelization")

# Current No Parallel
latency_meas_comp("latency_server_comp.txt", "Latency of Computation for Step Count", True)
latency_meas_recv_send("latency_server_recv.txt", "Latency of Server Receiving Accelerometer Data")
latency_meas_recv_send("latency_pi_send.txt", "Latency of Pi Sending Accelerometer Data")
latency_meas_recv_send("latency_pi_recv.txt", "Latency of Pi Receiving Step Count Data")