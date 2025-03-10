import matplotlib.pyplot as plt

# Use inline plotting
%matplotlib inline


# Create a simple plot
plt.plot([0, 1], [0, 1])
plt.title('Simple Line Plot')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid()
plt.show()  # Display the plot
