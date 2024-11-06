import numpy as np
import matplotlib.pyplot as plt

# Параметры модели
n = 50  # количество грузиков
m = 1.0  # масса каждого грузика
k = 10.0  # коэффициент упругости "веревки"
F0 = 1.0  # амплитуда внешней силы
omega = 0.5  # начальная частота внешней силы
delta_omega = 0.05  # шаг изменения частоты
timestep = 0.01  # временной шаг
duration = 100  # продолжительность симуляции

# Начальные условия (можно взять случайные малые колебания)
x = np.zeros(n)  # положения грузиков по x
y = np.zeros(n)  # положения грузиков по y

# Скорости и ускорения
vx = np.zeros(n)
vy = np.zeros(n)
ax = np.zeros(n)
ay = np.zeros(n)

# Функция для обновления сил и ускорений с учетом внешней силы
def update_forces(omega, t):
    global ax, ay
    # Внешняя сила действует на первый грузик по оси y
    external_force = F0 * np.sin(omega * t)
    ay[0] += external_force / m

    # Обновляем силы и ускорения для каждого грузика
    for i in range(1, n - 1):
        # Сила между грузиками, упругость (простая модель)
        force_y = -k * (y[i] - y[i - 1]) - k * (y[i] - y[i + 1])
        ay[i] = force_y / m

# Основной цикл симуляции
time_steps = int(duration / timestep)
amplitudes = []

for t_step in range(time_steps):
    t = t_step * timestep
    # Обновляем силы и ускорения
    update_forces(omega, t)
    
    # Обновляем положения и скорости
    vx += ax * timestep
    vy += ay * timestep
    x += vx * timestep
    y += vy * timestep
    
    # Сохраняем амплитуду центрального грузика для анализа резонанса
    amplitudes.append(abs(y[n // 2]))  # например, для центрального грузика

    # Визуализация в реальном времени (опционально)
    if t_step % 100 == 0:  # обновляем график каждые 100 шагов
        plt.clf()
        plt.plot(y, 'o-')
        plt.ylim(-5, 5)
        plt.pause(0.01)

    # Увеличиваем частоту через заданный интервал времени
    if t_step % (time_steps // 10) == 0:
        omega += delta_omega

plt.show()

# Построение графика амплитуд для анализа резонанса
plt.plot(amplitudes)
plt.xlabel('Time steps')
plt.ylabel('Amplitude of central mass')
plt.show()