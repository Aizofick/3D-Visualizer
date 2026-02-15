# cubes

Минимальное 3D‑приложение на Python + PyGame + PyOpenGL, рисующее анимированный «фрактал» из кубов.  
Форма структуры и уровень детализации плавно меняются, кубы слегка пульсируют и смещаются, создавая ощущение живого объекта.

---

## Установка

### Требования

- Python 3.8+ (рекомендуется 3.10+).
- Установленные пакеты:
  - `pygame`
  - `PyOpenGL`
  - `PyOpenGL_accelerate`

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## или вручную

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
```

---

# Управление (RU)

## Клавиатура
- Esc — выход из приложения.
- Q — приближение камеры (zoom in).
- E — отдаление камеры (zoom out).

## Смена типа структуры
- 1 — режим 1: решётка из кубов.
- 2 — режим 2: менгер‑подобный куб.
- 3 — режим 3: случайный «пористый» объём.
- 4 — режим 4: шарообразная структура из кубов.

## Мышь
- ЛКМ (зажать) + движение по оси X — изменение уровня фрактала (детализация/сложность).
- СКМ (зажать колёсико) + движение — вращение камеры вокруг сцены.
- Колесо вверх — быстрый zoom in.
- Колесо вниз — быстрый zoom out.

---

# Controls (EN)

## Keyboard
- Esc — exit application.
- Q — zoom in (move camera closer).
- E — zoom out (move camera farther).

## Fractal type
- 1 — mode 1: grid of cubes.
- 2 — mode 2: Menger-like cube.
- 3 — mode 3: random porous volume.
- 4 — mode 4: spherical cube structure.

## Mouse
- LMB (hold) + move along X — change fractal level (detail/complexity).
- MMB (hold wheel button) + move — orbit camera around the scene.
- Mouse wheel up — fast zoom in.
- Mouse wheel down — fast zoom out.

---
