class Line:
	"""
    A class for linear interpolation
    ...
    
    Attributes
    ----------
    

    Methods
    -------
    get_y(x):
        Returns y value corrosponding to given x value on line
    """
	def __init__(self, x1, y1, x2, y2):
		"""
        Parameters
        ----------
		x1 : float
        	x value of first point on line
	    y1 : float
	        y value of first point on line
	    x2 : float
	        x value of second point on line
	    y2 : float
	        y value of second point on line
		"""
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def get_y(self, x):
		"""
		Parameters
		----------
		x : float
		    x value corrosponding to which y value is required in equation of line

		Returns
		-------
		float
		Returns y value corrosponding to given x value on line
		"""
		y = (x - self.x1) * (self.y2 - self.y1) / (self.x2 - self.x1) + self.y1
		return y


# my_line = Line(5, 5, 10, 10)
# print(my_line.get_y(20))