import numpy as np
import matplotlib.pyplot as plt
import mplcursors


def spring_force(k, x):
    return -k * x


def simulate(params):
    k = params["k"]
    m = params["m"]
    c = params["c"]
    dt = 0.01
    x = -0.03
    v = 0
    times = []
    positions = []
    velocities = []
    crossing_times = []
    for step in range(300):
        force = spring_force(k, x)
        damper_F = -c * v
        Fb = force + damper_F
        a = Fb / m
        v = v + a * dt
        dx = v * dt
        old_x = x
        x = x + dx
        t = (step + 1) * dt
        if old_x < 0 and x >= 0:
            crossing_times.append(t)
        times.append(t)
        positions.append(x)
        velocities.append(v)
    return {
        "times": times,
        "positions": positions,
        "velocities": velocities,
        "crossing_times": crossing_times,
    }

setup_a = {"m": 16, "k": 1600, "c": 40}
text = input("M (кг) and damper (Н·с/м) , for exampele > ")
parts = text.split()
m = float(parts[0])
c = float(parts[1])
setup_b = {"m": m, "k": setup_a["k"], "c": c}
results = {
    "Исходный набор": simulate(setup_a),
    "Твой набор": simulate(setup_b),
}

for name, result in results.items():
    crossing_times = result["crossing_times"]
    print(name)
    if len(crossing_times) >= 2:
        periods = np.diff(crossing_times)
        period = np.mean(periods)
        frequency = 1 / period
        print("period, с", round(period, 3))
        print("frequency, Гц", round(frequency, 3))
    else:
        print("Evaluation of the period via two passes from the midpoint.")
    plt.plot(result["times"], result["positions"], label=name)
plt.xlabel("Times, с")
plt.ylabel("Positions, м")
plt.title("Free Fluctions")
plt.legend()
mplcursors.cursor(hover=True)
plt.show()
