import math
# power screw calculations
#  ref: https://roymech.org/Useful_Tables/Cams_Springs/Power_Screws_1.html

class PowerScrew:
    """
    A class for Power Screw calculations
    ...
    Attributes
    ----------
    

    Methods
    -------
    get_tr():
        Returns Raising torque in Nm
    get_tl():
        Returns Lowering torque in Nm
    get_eff():
        Returns screw efficiency
    """
    def __init__(self, dm, w, mus, l, th, dmc, muc):
        """
        Parameters
        ----------
        dm : float
            Mean screw dia in m
        w : float
            Load on screw in N
        mus : float
            screw cof
        l : float
            lead in m
        th : float
            screw thread half angle in radian
        dmc : float
            mean collar dia in m
        muc : float
            collar cof
        """
        self.dm = dm
        self.w = w
        self.mus = mus
        self.l = l
        self.th = th
        self.dmc = dmc
        self.muc = muc

    def get_tr(self):
        """
        Returns
        -------
        float
        Returns Raising torque in Nm
        """
        ans = 0
        try:
            alp = math.atan(self.l / (math.pi * self.dm))
            thn = math.atan(math.cos(alp) * math.tan(self.th))
            ans = 0.5 * self.dm * self.w * (self.mus + math.cos(thn) * math.tan(alp)) / (math.cos(thn) - \
                self.mus * math.tan(alp)) + 0.5 * self.w * self.dmc * self.muc
        except Exception as e:
            print(e)
            ans = 0
        return ans  # in Nm


    def get_tl(self):
        """
        Returns
        -------
        float
        Returns Lowering torque in Nm
        """
        ans = 0
        try:
            alp = math.atan(self.l / (math.pi * self.dm))
            thn = math.atan(math.cos(alp) * math.tan(self.th))
            ans = 0.5 * self.dm * self.w * (self.mus - math.cos(thn) * math.tan(alp)) / (math.cos(thn) + \
                self.mus * math.tan(alp)) + 0.5 * self.w * self.dmc * self.muc
        except Exception as e:
            print(e)
            ans = 0
        return ans  # in Nm


    def get_eff(self):
        """
        Returns
        -------
        float
        Returns screw efficiency
        """
        ans = 0
        try:
            alp = math.atan(self.l / (math.pi * self.dm))
            thn = math.atan(math.cos(alp) * math.tan(self.th))
            denominator = self.dm * (self.mus + math.cos(thn) * math.tan(alp)) / (math.cos(thn) - \
                self.mus * math.tan(alp)) + self.dmc * self.muc
            numerator = self.dm * math.tan(alp)
            ans = numerator / denominator
        except Exception as e:
            print(e)
            ans = 0
        return ans


# ps = PowerScrew(0.1, 10000, 0.05, 0.025, 30*math.pi/180, 0.15, 0.05)
# tr = ps.get_tr()
# tl = ps.get_tl()
# eff = ps.get_eff()
# print(tr)
# print(tl)
# print(eff)