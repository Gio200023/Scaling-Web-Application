import matplotlib.pyplot as plt

# Sample data
current_sessions = [294, 1000, 977, 934, 949, 925, 935, 979, 963, 984, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 2, 2, 1, 1, 200, 200, 200, 200, 0, 239, 232, 221, 228, 236, 405, 394, 383, 392, 400, 410, 386, 381, 377, 393, 421, 381, 379, 382, 390, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 126, 126, 125, 125, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 128, 128, 127, 127, 151, 150, 150, 40, 399, 399, 398, 399, 399, 398, 399, 399, 398, 504, 503, 503, 504, 503, 503, 504, 503, 503, 504, 503, 503, 2, 2, 2, 2, 19, 18, 19, 18, 19, 18, 42, 41, 242, 239, 223, 218, 2]
response_times = [0, 0, 35, 277, 518, 949, 1316, 1430, 1616, 1732, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 49, 112, 68, 16, 0, 48, 90, 53, 22, 0, 152, 150, 209, 113, 0, 299, 270, 263, 248, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3430, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 395, 405, 0]
containers = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1]

# Plotting
plt.figure(figsize=(14, 7))

# Current Sessions Plot
plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
plt.plot(current_sessions, label='Current Sessions', color='blue')
plt.title('Current Sessions Over Time')
plt.xlabel('Time (in arbitrary units)')
plt.ylabel('Number of Sessions')

# Response Times Plot
plt.subplot(3, 1, 2)
plt.plot(response_times, label='Response Times', color='red')
plt.title('Response Times Over Time')
plt.xlabel('Time (in arbitrary units)')
plt.ylabel('Response Time (ms)')

# Containers Plot
plt.subplot(3, 1, 3)
plt.plot(containers, label='Number of Containers', color='green')
plt.title('Number of Containers Over Time')
plt.xlabel('Time (in arbitrary units)')
plt.ylabel('Number of Containers')

plt.tight_layout()  # Adjust subplots to fit into figure area.
plt.show()

# print("Plot 1: Displays the fluctuation in the number of current sessions, highlighting system load.")
# print("Plot 2: Shows how response times vary, which can indicate the system's ability to handle increased load.")
# print("Plot 3: Illustrates the number of containers utilized over time, reflecting the system's scaling behavior.")