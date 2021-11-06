from vpython import *
from math import sqrt, pi
from util import euler_cromer
from random import randint

# konstant
G = 6.67e-11

# tidsbetingelser
t = 0
dt = 2e4

# Konstante størrelser
M_SUN = 1.9891e30
SUN_RADIUS = 6.95500e8

# Sol-aktig-farge funnet: https://www.colorcombos.com/colors/FCD440
SUN_COLOR = vec(252, 212, 64) / 100

# massen
m15 = 15 * M_SUN
m8 = 8 * M_SUN

# avstand
d = 1.5e11 # m

# total masse
M = m15 + m8

# radius for sirkulær bane
r15 = (m8 * d) / M
r8 = (m15 * d) / M

# perioden til systemet forutsatt at banene er sirkulære
T = sqrt(4 * pi ** 2 * d ** 3 / (G * M))

# hastigheter
v15 = 2 * pi * r15 / T
v8 = 2 * pi * r8 / T

# animasjonsvinduet
screen = canvas()

# animasjonsobjekter
CM = sphere(radius=SUN_RADIUS, make_trail=True, color=color.red)
M15 = sphere(pos=vec(-r15, 0, 0), vel=vec(0, v15, 0), radius=SUN_RADIUS * 15, make_trail=True, color=SUN_COLOR)
M8 = sphere(pos=vec(r8, 0, 0), vel=vec(0, -v8, 0), radius=SUN_RADIUS * 8, make_trail=True, color=SUN_COLOR)

# Fragmentene i eksplosjonen
N_fragmenter = 10
fragmenter = [sphere(pos=vec(0, 0, 0), vel=vec(0, 0, 0), radius=M15.radius / N_fragmenter, make_trail=False, visible=False, a=vec(0, 0, 0)) for _ in range(N_fragmenter)]

# loop i 5 perioder
while t < 5 * T:

    # relativ posisjon
    r = M15.pos - M8.pos

    # kraft
    F = -G * m15 * m8 / r.mag2 * r.hat

    # akselerasjoner
    M15.a = F / m15
    M8.a = - F / m8
    
    # sett massesenter-objektets posisjon til det utregnede massesenteret
    CM.pos = (m15 * M15.pos + m8 * M8.pos) / M

    # eksplosjonen som skjer etter 1 periode.
    if t > T and t < T + dt:

        # setter massen of radius til å være 3 * solas
        m15 = 3 * M_SUN
        M15.radius = 3 * SUN_RADIUS
        M15.color = color.red

        # itererer over hvert fragment
        for fragment in fragmenter:

            # setter posisjonen til nåværende posisjon til M15
            fragment.pos = M15.pos

            # gjør fragmentene synlige og slik at de tegner banene sine
            fragment.make_trail = True
            fragment.visible = True
            
            # setter hastigheten til en tilfeldig vektor opp til fem ganger større enn M15's hastighet. Merk at dette er en sfærisk symmetrisk eksplosjon (Når N_fragmenter er stor nok).
            fragment.vel = vec(randint(-5, 5), randint(-5, 5), randint(-5, 5)) * M15.vel.mag

    # gjør fragmentene usynlige igjen etter 20% av neste periode.
    if t > T + .2 * T:
        for fragment in fragmenter:
            fragment.visible = False

    # oppdater bevegelse av solene og fragmentene
    euler_cromer(dt, M15, M8, *fragmenter)

    # sett raten og oppdater tidssteget
    rate(30)
    t += dt

    # sett midten av animasjonsvinduet til massesenterets posisjon
    screen.center = CM.pos

print("Animation done")