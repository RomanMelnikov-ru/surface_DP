import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import false

# Заголовок приложения
st.title("Визуализация критерия Друккера-Прагера")

# Слайдеры для прочностных параметров
c = st.slider("Удельное сцепление (c, кПа)", min_value=0.0, max_value=50.0, value=10.0, step=5.0)
phi = st.slider("Угол внутреннего трения (φ, град.)", min_value=0.0, max_value=35.0, value=20.0, step=1.0)

# Параметры критерия Друккера-Прагера
phi_rad = np.deg2rad(phi)
alpha = (2 * np.sin(phi_rad)) / (np.sqrt(3) * (3 - np.sin(phi_rad)))
k = (6 * c * np.cos(phi_rad)) / (np.sqrt(3) * (3 - np.sin(phi_rad)))

# Вершина конуса (должна быть в отрицательной области при c > 0)
sigma_vertex = -np.array([k / (3 * alpha), k / (3 * alpha), k / (3 * alpha)])

# Гидростатическая ось
t = np.linspace(-k / (3 * alpha), 100, 100)
hydrostatic_axis = np.array([t, t, t])

# Девиаторная плоскость (I1 = const) в положительной области (сжатие)
I1_plane = 200  # Значение I1 для девиаторной плоскости
radius = np.sqrt(2) * (k + alpha * I1_plane)  # Сжатие положительное

# Окружность в девиаторной плоскости
theta = np.linspace(0, 2 * np.pi, 100)
x_circle = radius * np.cos(theta)
y_circle = radius * np.sin(theta)

# Преобразование в 3D пространство главных напряжений
sigma1 = I1_plane / 3 + (x_circle / np.sqrt(2)) - (y_circle / np.sqrt(6))
sigma2 = I1_plane / 3 - (x_circle / np.sqrt(2)) - (y_circle / np.sqrt(6))
sigma3 = I1_plane / 3 + (2 * y_circle / np.sqrt(6))

# Создание поверхности конуса
u = np.linspace(0, 1, 100)  # Параметр для интерполяции
sigma1_cone = np.outer(1 - u, sigma1) + np.outer(u, sigma_vertex[0])
sigma2_cone = np.outer(1 - u, sigma2) + np.outer(u, sigma_vertex[1])
sigma3_cone = np.outer(1 - u, sigma3) + np.outer(u, sigma_vertex[2])

# Создание 3D графика с использованием Plotly
fig = go.Figure()

# Гидростатическая ось
fig.add_trace(go.Scatter3d(
    x=hydrostatic_axis[0], y=hydrostatic_axis[1], z=hydrostatic_axis[2],
    mode='lines',
    line=dict(color='gray', width=2, dash='longdash'),
    name='Гидростатическая ось'
))

# Девиаторная плоскость с окружностью
fig.add_trace(go.Scatter3d(
    x=sigma1, y=sigma2, z=sigma3,
    mode='lines',
    line=dict(color='orange', width=2),
    name='Девиаторная плоскость (окружность)'
))

# Поверхность конуса
fig.add_trace(go.Surface(
    x=sigma1_cone, y=sigma2_cone, z=sigma3_cone,
    colorscale='Oranges',
    opacity=0.5,
    name='Поверхность конуса',
    showscale=False
))

# Вершина конуса
fig.add_trace(go.Scatter3d(
    x=[sigma_vertex[0]], y=[sigma_vertex[1]], z=[sigma_vertex[2]],
    mode='markers',
    marker=dict(color='orange', size=3),
    name='Вершина конуса'
))

# Оси координат
fig.add_trace(go.Scatter3d(
    x=[0, 50], y=[0, 0], z=[0, 0],
    mode='lines',
    line=dict(color='red', width=3),
    name='Ось σ1 (красная)'
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 50], z=[0, 0],
    mode='lines',
    line=dict(color='blue', width=3),
    name='Ось σ2 (синяя)'
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[0, 50],
    mode='lines',
    line=dict(color='green', width=3),
    name='Ось σ3 (зеленая)'
))

# Настройка макета
fig.update_layout(
    scene=dict(
        xaxis_title='σ1',
        yaxis_title='σ2',
        zaxis_title='σ3',
        aspectmode='cube',

    ),
    margin=dict(l=0, r=0, b=0, t=0),
    showlegend=False
)

# Отображение графика в Streamlit
st.plotly_chart(fig, use_container_width=False)
