def euler_cromer(dt, *objects):
    """
    Funksjon som utfører euler cromers metode på objektene som sendes inn i funksjonen

    Parametre:
        dt: float
            En skalar som definerer tidssteget som brukes i hver oppdatering.
    Argumenter:
        *objects: vpython objekt
            Et objekt fra vpython biblioteket. I dette tilfellet er det objektene som skal oppdatere sin posisjon og hastighet.
            NB: objektene må ha definert en akselerasjon på forhånd som:

            obj.a = vpython.vector --- altså et vektor objekt.

            Er du usikker på hvordan å bruke *args (argumenter) se python dokumentasjonen her: https://docs.python.org/3.4/tutorial/controlflow.html#keyword-arguments
    """
    for obj in objects:
        obj.vel = obj.vel + obj.a * dt
        obj.pos = obj.pos + obj.vel * dt