"""
draw_points.py


created at 2026-05-21
"""

import matplotlib.pyplot as plt

c = -0.62772 - 0.42193j
z = 0 + 0j

n_values = []
abs_z_values = []

for n in range(300):
    z = z * z + c
    n_values.append(n)
    abs_z_values.append(abs(z))

plt.figure(figsize=(10, 6))  # 设置画布大小
plt.plot(n_values, abs_z_values, marker=".", linestyle="-", linewidth=1, color="b")

plt.title("Evolution of abs(z) over 300 iterations")
plt.xlabel("Iteration (n)")
plt.ylabel("abs(z)")

plt.grid(True)
plt.show()
