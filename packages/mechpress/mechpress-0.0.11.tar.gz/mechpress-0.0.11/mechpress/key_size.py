class KeySize:
	"""
    A class for finding key sizes
    ...
    
    Attributes
    ----------
    


    Methods
    -------
    get_key_data():
        Returns dictionary of key width ('b') in mm, key height ('h') in mm,
        keyway depth in shaft ('ds') in mm and keyway depth in hub ('dh') in mm 
    """
	def __init__(self, d):
		"""
        Parameters
        ----------
		d : float
        	shft dia in mm
		"""
		self.d = d

	def get_key_data(self):
		"""
		Returns
		-------
		dictionary
		Returns dictionary of key width ('b') in mm, key height ('h') in mm,
        keyway depth in shaft ('ds') in mm and keyway depth in hub ('dh') in mm 
		"""
		b = 0
		h = 0
		ds = 0
		dh = 0

		if self.d > 6 and self.d <= 8:
			b = 2
			h = 2
			ds = 1.2
			dh = 1
		elif self.d > 8 and self.d <= 10:
			b = 3
			h = 3
			ds = 1.8
			dh = 4
		elif self.d > 10 and self.d <= 12:
			b = 4
			h = 4
			ds = 2.5
			dh = 1.8
		elif self.d > 12 and self.d <= 17:
			b = 5
			h = 5
			ds = 3
			dh = 2.3
		elif self.d > 17 and self.d <= 22:
			b = 6
			h = 6
			ds = 3.5
			dh = 2.8
		elif self.d > 22 and self.d <= 30:
			b = 8
			h = 7
			ds = 4
			dh = 3.3
		elif self.d > 30 and self.d <= 38:
			b = 10
			h = 8
			ds = 5
			dh = 3.3
		elif self.d > 38 and self.d <= 44:
			b = 12
			h = 8
			ds = 5
			dh = 3.3
		elif self.d > 44 and self.d <= 50:
			b = 14
			h = 9
			ds = 5.5
			dh = 3.8
		elif self.d > 50 and self.d <= 58:
			b = 16
			h = 10
			ds = 6
			dh = 4.3
		elif self.d > 58 and self.d <= 65:
			b = 18
			h = 11
			ds = 7
			dh = 4.4
		elif self.d > 65 and self.d <= 75:
			b = 20
			h = 12
		elif self.d > 75 and self.d <= 85:
			b = 22
			h = 14
			ds = 7.5
			dh = 4.9
		elif self.d > 85 and self.d <= 95:
			b = 25
			h = 14
			ds = 9
			dh = 5.4
		elif self.d > 95 and self.d <= 110:
			b = 28
			h = 16
			ds = 10
			dh = 6.4
		elif self.d > 110 and self.d <= 130:
			b = 32
			h = 18
			ds = 11
			dh = 7.4
		elif self.d > 130 and self.d <= 150:
			b = 36
			h = 20
			ds = 12
			dh = 8.4
		elif self.d > 150 and self.d <= 170:
			b = 40
			h = 22
			ds = 13
			dh = 9.4
		elif self.d > 170 and self.d <= 200:
			b = 45
			h = 25
			ds = 15
			dh = 10.4
		elif self.d > 200 and self.d <= 230:
			b = 50
			h = 28
			ds = 17
			dh = 11.4
		elif self.d > 230 and self.d <= 260:
			b = 56
			h = 32
			ds = 20
			dh = 12.4
		elif self.d > 260 and self.d <= 290:
			b = 63
			h = 32
			ds = 20
			dh = 12.4
		elif self.d > 290 and self.d <= 330:
			b = 70
			h = 36
			ds = 22
			dh = 14.4
		elif self.d > 330 and self.d <= 380:
			b = 80
			h = 40
			ds = 25
			dh = 15.4
		elif self.d > 380 and self.d <= 440:
			b = 90
			h = 45
			ds = 28
			dh = 17.4
		elif self.d > 440 and self.d <= 500:
			b = 100
			h = 50
			ds = 31
			dh = 18.5
		else:
			b = 0
			h = 0
			ds = 0
			dh = 0

		ans_dic = {
			'b':b,
			'h':h,
			'ds':ds,
			'dh':dh,
		}

		return ans_dic


# test program
# ks= KeySize(100)
# answer_dic = ks.get_key_data()
# key_width = answer_dic['b']
# key_height = answer_dic['h']
# keyway_depth_shaft = answer_dic['ds']
# keyway_depth_hub = answer_dic['dh']
# print("key width:", key_width)
# print("key height", key_height)
# print("keyway depth in shaft", keyway_depth_shaft)
# print("keyway depth in hub", keyway_depth_hub)
