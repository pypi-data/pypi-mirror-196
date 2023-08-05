class MetricThread:
	"""
    A class for Metric thread dimensions
    ...

    Attributes
    ----------


    Methods
    -------
    get_ext_dmin():
        Returns minimum dameter of external threads in mm

    get_int_dmin():
        Returns minimum dameter of internal threads in mm
    """
	def __init__(self, d, p):
		"""
        Parameters
        ----------
		d : float
        	major dia in mm
	    p : float
	        pitch in mm
		"""
		self.d = d
		self.p = p

	def get_ext_dmin(self):
		"""
		Returns
		-------
		float
		Returns minimum dameter of external threads in mm
		"""
		return self.d - 1.227 * self.p

	def get_int_dmin(self):
		"""
		Returns
		-------
		float
		Returns minimum dameter of internal threads in mm
		"""
		return self.d - 1.083 * self.p

# program test
# my_screw = MetricThread(24, 3)
# print(my_screw.get_ext_dmin())
# print(my_screw.get_int_dmin())
