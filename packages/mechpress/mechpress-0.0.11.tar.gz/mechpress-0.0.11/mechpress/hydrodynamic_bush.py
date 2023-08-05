import math

class HydrodynamicBush:
    """
    A class for hydrodynamic bush calculations
    ...
    
    Attributes
    ----------
    

    Methods
    -------
    hyd_dyn_bush():
        Returns dictioanry of important bearing parameters like  Eccentricity ratio, 
        Sommerfeld number, film thickness, attitude angle and required oil flow
    """
    def __init__(self, w, d, l, c, rpm, mu):
        """
        Parameters
        ----------
        w : float
            load in N
        d : float
            bush dia in m
        l : float
            bush width in m
        c : float
            diameteral clearance in m
        rpm : float
            rpm
        mu : float
            dynamic viscosity in Pa.s
        """
        self.w = w
        self.d = d
        self.l = l
        self.c = c
        self.rpm = rpm
        self.mu = mu

    def hyd_dyn_bush(self):
        """
        Returns
        -------
        dictionary
        Returns dictioanry of important bearing parameters like  Eccentricity ratio ('e'), 
        Sommerfeld number ('s'), film thickness in m ('h_min'), 
        attitude angle in radian ('phi') and required oil flow in m3/s ('q')
        """
        r = self.d / 2  # radius in m
        pl = self.w / (self.d * self.l)  # project load N/m2
        ns = self.rpm / 60  # rps
        omg = 2 * math.pi * self.rpm / 60  # ang vel
        s = (self.mu * ns / pl) * (r / self.c)**2  # sommerfeld no
        e = get_e(s, self.d, self.l)  # ecc ratio
        phi = math.atan((math.pi * (1 - e**2)**0.5) / (4 * e))  # atitude ang in rad
        u = r * omg  # linear surface speed
        q = e * u * self.l * self.c  # flow in m3/s
        h_min = self.c * (1 - e)  # min film thk in m
        ans_dic = {
            'e': e,
            's': s,
            'phi': phi,
            'q': q,
            'h_min': h_min,
        }
        return ans_dic



def get_e(s, d, l):
    """
    Parameters
    ----------
    s : float
        Sommerfeld number
    d : float
        bush dia in m
    l : float
        bush width in m

    Returns
    -------
    float
    Returns eccentricity ratio
    """
    e = 0.999
    err = 0.0001
    s_this = get_s(e, d, l)
    
    while abs(s - s_this) >= err or e < 0:
        e = e - err
        s_this = get_s(e, d, l)
    
    return round(e, 3)


def get_s(e, d, l):
    """
    Parameters
    ----------
    e : float
        eccentricity ratio
    d : float
        bush dia in m
    l : float
        bush width in m

    Returns
    -------
    float
    Returns Sommerfeld number
    """
    n1 = (1 - e**2)
    n2 = (d / l)
    d1 = math.pi * e
    d2 = math.pi**2 * (1 - e**2)
    d3 = 16 * e**2
    s_this = n1**2 * n2**2 / (d1 * (d2 + d3)**0.5)
    return s_this


# for testing program
# bush = HydrodynamicBush(1000000, 1, 0.5, 0.001, 50, 0.1275)
# ans_dic = bush.hyd_dyn_bush()
# print(ans_dic)
