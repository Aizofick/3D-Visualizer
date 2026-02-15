import sys
import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH, HEIGHT = 800, 600

mode = 1

def init_gl():
    glViewport(0, 0, WIDTH, HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.05, 0.05, 0.08, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WIDTH / HEIGHT, 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_cube(x, y, z, size=1.0):
    s = size / 2.0
    v = [
        [x - s, y - s, z - s],
        [x + s, y - s, z - s],
        [x + s, y + s, z - s],
        [x - s, y + s, z - s],
        [x - s, y - s, z + s],
        [x + s, y - s, z + s],
        [x + s, y + s, z + s],
        [x - s, y + s, z + s],
    ]
    e = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    glBegin(GL_LINES)
    for a, b in e:
        glVertex3fv(v[a])
        glVertex3fv(v[b])
    glEnd()

def make_grid(level):
    cubes = []
    if level == 0:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        extent = 2.0
    else:
        n = level
        base = 2.0 / (n + 1)
        step = base * 1.6
        extent = 0.0
        for ix in range(-n, n + 1):
            for iy in range(-n, n + 1):
                for iz in range(-n, n + 1):
                    if (ix*ix + iy*iy + iz*iz) % 4 != 0:
                        continue
                    x = ix * step
                    y = iy * step
                    z = iz * step
                    cubes.append((x, y, z, base))
                    extent = max(
                        extent,
                        abs(x) + base,
                        abs(y) + base,
                        abs(z) + base
                    )
    if not cubes:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        extent = 2.0
    return cubes, extent

def make_menger(level):
    cubes = [(0.0, 0.0, 0.0, 2.0)]
    for _ in range(level):
        nxt = []
        for (cx, cy, cz, size) in cubes:
            s = size / 3.0
            offs = [-s, 0.0, s]
            for ix in offs:
                for iy in offs:
                    for iz in offs:
                        center_axis = (
                            (abs(ix) < 1e-6 and abs(iy) < 1e-6) or
                            (abs(ix) < 1e-6 and abs(iz) < 1e-6) or
                            (abs(iy) < 1e-6 and abs(iz) < 1e-6)
                        )
                        if center_axis:
                            continue
                        nx = cx + ix
                        ny = cy + iy
                        nz = cz + iz
                        nxt.append((nx, ny, nz, s))
        cubes = nxt

    extent = 0.0
    for (x, y, z, s) in cubes:
        extent = max(
            extent,
            abs(x) + s,
            abs(y) + s,
            abs(z) + s
        )
    if extent == 0.0:
        extent = 2.0
    return cubes, extent

def make_random(level, seed=1234):
    r = random.Random(seed + level)
    cubes = []
    if level == 0:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        extent = 2.0
        return cubes, extent

    n = 2 + level
    base = 2.0 / n
    step = base * 1.3
    p = max(0.15, 0.5 - level * 0.03)

    extent = 0.0
    for ix in range(-n, n+1):
        for iy in range(-n, n+1):
            for iz in range(-n, n+1):
                if r.random() > p:
                    continue
                x = ix * step
                y = iy * step
                z = iz * step
                cubes.append((x, y, z, base))
                extent = max(
                    extent,
                    abs(x) + base,
                    abs(y) + base,
                    abs(z) + base
                )
    if not cubes:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        extent = 2.0
    return cubes, extent

def make_sphere(level):
    cubes = []
    if level == 0:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        return cubes, 2.0

    n = 4 + level * 2
    base = 2.0 / n
    step = base * 1.4
    extent = 0.0
    for ix in range(-n, n+1):
        for iy in range(-n, n+1):
            for iz in range(-n, n+1):
                x = ix * step
                y = iy * step
                z = iz * step
                r = math.sqrt(x*x + y*y + z*z)
                if r > 2.0:
                    continue
                if (ix*ix + iy*iy + iz*iz) % 5 != 0:
                    continue
                cubes.append((x, y, z, base))
                extent = max(extent, r + base)
    if not cubes:
        cubes.append((0.0, 0.0, 0.0, 2.0))
        extent = 2.0
    return cubes, extent

def make_level(level, m):
    if m == 1:
        return make_grid(level)
    elif m == 2:
        return make_menger(level)
    elif m == 3:
        return make_random(level)
    elif m == 4:
        return make_sphere(level)
    else:
        return make_grid(level)

def draw_space(extent):
    size = extent * 2.5
    h = size * 0.6
    floor_y = -size * 0.6

    glLineWidth(1.0)

    glColor3f(0.2, 0.22, 0.28)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-size, floor_y, -size)
    glVertex3f(size, floor_y, -size)
    glVertex3f(size, floor_y, size)
    glVertex3f(-size, floor_y, size)
    glEnd()

    glColor3f(0.18, 0.2, 0.26)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-size, floor_y, -size)
    glVertex3f(size, floor_y, -size)
    glVertex3f(size, h, -size)
    glVertex3f(-size, h, -size)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(-size, floor_y, -size)
    glVertex3f(-size, floor_y, size)
    glVertex3f(-size, h, size)
    glVertex3f(-size, h, -size)
    glEnd()

    glBegin(GL_LINE_LOOP)
    glVertex3f(size, floor_y, -size)
    glVertex3f(size, floor_y, size)
    glVertex3f(size, h, size)
    glVertex3f(size, h, -size)
    glEnd()

def lerp(a, b, t):
    return a + (b - a) * t

def mix_levels(a, b, t):
    cubes_a, ext_a = a
    cubes_b, ext_b = b

    na = len(cubes_a)
    nb = len(cubes_b)
    n = min(na, nb)

    res = []
    for i in range(n):
        xa, ya, za, sa = cubes_a[i]
        xb, yb, zb, sb = cubes_b[i]
        x = lerp(xa, xb, t)
        y = lerp(ya, yb, t)
        z = lerp(za, zb, t)
        s = lerp(sa, sb, t)
        res.append((x, y, z, s))

    if nb > na and t > 0.1:
        extra = int((nb - na) * (t ** 2))
        extra = min(extra, nb - na)
        for i in range(extra):
            res.append(cubes_b[na + i])

    extent = lerp(ext_a, ext_b, t)
    return res, extent

def main():
    global mode

    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("cubes")

    init_gl()

    dist = 12.0
    yaw = 0.9
    pitch = -0.6
    mmb_orbit = False
    lmb_level = False
    last_mouse = (0, 0)
    last_lmb_x = 0

    target_level = 0.0
    current_level = 0.0
    morph_speed = 3.0

    cache = {}

    def get_level(level, m):
        if level < 0:
            level = 0
        key = (m, level)
        if key not in cache:
            cubes, ext = make_level(level, m)
            cache[key] = (cubes, ext)
        return cache[key]

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        t = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_q:
                    dist = max(2.0, dist - 0.5)
                if event.key == K_e:
                    dist = min(200.0, dist + 0.5)
                if event.key == K_1:
                    mode = 1
                if event.key == K_2:
                    mode = 2
                if event.key == K_3:
                    mode = 3
                if event.key == K_4:
                    mode = 4

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    lmb_level = True
                    last_lmb_x = event.pos[0]
                elif event.button == 2:
                    mmb_orbit = True
                    last_mouse = event.pos
                elif event.button == 4:
                    dist = max(2.0, dist * 0.9)
                elif event.button == 5:
                    dist = min(200.0, dist * 1.1)

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    lmb_level = False
                if event.button == 2:
                    mmb_orbit = False

            if event.type == MOUSEMOTION:
                mx, my = event.pos
                dx = mx - last_mouse[0]
                dy = my - last_mouse[1]

                if mmb_orbit:
                    yaw += dx * 0.01
                    pitch += dy * 0.01
                    pitch = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, pitch))
                    last_mouse = (mx, my)

                if lmb_level:
                    dx_lvl = mx - last_lmb_x
                    target_level += dx_lvl * 0.01
                    if target_level < 0:
                        target_level = 0
                    last_lmb_x = mx

        if abs(current_level - target_level) > 0.001:
            if current_level < target_level:
                current_level += morph_speed * dt
                if current_level > target_level:
                    current_level = target_level
            else:
                current_level -= morph_speed * dt
                if current_level < target_level:
                    current_level = target_level

        base_level = int(math.floor(current_level))
        if base_level < 0:
            base_level = 0
        next_level = base_level + 1
        lvl_t = current_level - base_level

        a = get_level(base_level, mode)
        b = get_level(next_level, mode)

        cubes, extent = mix_levels(a, b, lvl_t)

        if dist < extent * 1.2:
            dist = extent * 1.2

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        cx = math.cos(pitch)
        sx = math.sin(pitch)
        cy = math.cos(yaw)
        sy = math.sin(yaw)
        eye = (
            cx * sy * dist,
            sx * dist,
            cx * cy * dist
        )

        gluLookAt(
            eye[0], eye[1], eye[2],
            0.0, 0.0, 0.0,
            0.0, 1.0, 0.0
        )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_space(extent)

        glColor3f(0.9, 0.9, 1.0)
        glLineWidth(1.3)

        for (x, y, z, s) in cubes:
            phase = (x + y + z) * 0.5
            dx = 0.2 * math.sin(t*1.5 + phase)
            dy = 0.2 * math.sin(t*1.7 + phase*0.7)
            dz = 0.2 * math.sin(t*1.3 + phase*1.3)
            scale = 1.0 + 0.3 * math.sin(t*2.0 + phase*0.3)
            draw_cube(x + dx, y + dy, z + dz, s * scale)

        pygame.display.set_caption(
            f"cubes | mode={mode} level={current_level:.2f} dist={dist:.1f}"
        )
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
