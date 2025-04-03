import matplotlib.pyplot as plt


processors = [1, 2, 4, 8, 16]
runtimes = [130, 66, 34, 19, 11]

# Calculate speedup and cost
speedup = [runtimes[0] / t for t in runtimes]
cost = [p * t for p, t in zip(processors, runtimes)]

# Plot speedup
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(processors, speedup, marker='o', color='b', label='Speedup')
plt.xlabel('Number of Processors (P)')
plt.ylabel('Speedup')
plt.title('Parallel Speedup')
plt.grid(True)
plt.legend()

# Plot cost
plt.subplot(1, 2, 2)
plt.plot(processors, cost, marker='o', color='r', label='Cost')
plt.xlabel('Number of Processors (P)')
plt.ylabel('Cost (P * T_P)')
plt.title('Parallel Cost')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()