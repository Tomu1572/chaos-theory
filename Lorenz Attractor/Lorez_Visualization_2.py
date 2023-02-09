import numpy as np
import matplotlib.pyplot as plt

# chaotic solution
σ = 10
ρ = 28
β = 8 / 3

dt = 0.01  # is the sample rate in seconds.
x = 20000

dxdt = np.empty(x + 1)
dydt = np.empty(x + 1)
dzdt = np.empty(x + 1)

# Initial values
dxdt[0], dydt[0], dzdt[0] = (0.0, 1.0, 1.05)

for i in range(x):
    dxdt[i + 1] = dxdt[i] + σ * (dydt[i] - dxdt[i]) * dt
    dydt[i + 1] = dydt[i] + (dxdt[i] * (ρ - dzdt[i]) - dydt[i]) * dt
    dzdt[i + 1] = dzdt[i] + (dxdt[i] * dydt[i] - β * dzdt[i]) * dt

fig = plt.figure(figsize=(16, 16),dpi=400)
ax = fig.add_subplot(projection='3d')
ax.plot(dxdt, dydt, dzdt, lw=0.5)
ax.set_xlabel("X Axis")
ax.set_ylabel("Y Axis")
ax.set_zlabel("Z Axis")
ax.set_title("Lorenz Attractor")
plt.show()