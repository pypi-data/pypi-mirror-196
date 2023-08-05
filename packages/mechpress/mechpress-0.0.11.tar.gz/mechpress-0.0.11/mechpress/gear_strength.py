import math

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



class GearStrength:
	"""
    1. A class to find pinion torque (in Nm) in a Gear-Pinion mesh
    2. Program works on linear interpolation only
    3. Few set points are calculated using actual program
    4. Based on these setpoints, user defined points are interpolated to find torque
    5. This program works for module 6 to 25 only
    6. Face width is considered 15 time of module
    7. Pressure angle of 20 deg is considered
    8. Helix angle set points are 0, 10, 20 and 30 deg
    9. Gear ratio set points are 3 and 5
    10. Pinion teeth set points are 17 and 31
    11. +0.3 correction factor in pinon and -0.3 in gear is considered
    12. Results are accurate if input values are near set points 
    13. There is no option to input correction factor
    14. Pinion material EN24 UTS 890MPa, Endurance 310 MPa and Surface hardness 255 HB
    15. Gear material IS 2708 casting with UTS 690 MPa, Endurance 235 MPa and Surface hardness 210 HB
    16. In case of gear ratios < 2, it is recommended to use EN24 gear for which output of this program is not valid
    17. Gear and Pinion surfaces are not hardened and not ground
    18. Gear and Pinion quality class 7 is considered
    19. Calculations are done on 100 rpm gear speed
    20. When z is small, failure criterion is pitting, when z is large (~27 above), failure criterion is bending
    21. Above effect is more pronounced in helical gears
    22. If your gear is driving another gear, FOS is reduced by 13%. To avoid failure, reduce torque by 13%
    23. Above effect is valid in bending only, there is no effect on FOS in pitting
    24. For gears rotating in both direction, FOS is reduced by 20%. So reduce torque by 20%
    25. For both direction rotation and gear driving another gear, FOS is reduced by 30%. So to avoid failure reduce torque by 30%

    ...

    Attributes
	----------
	gear_dic : dictionary
	    A dictionary which holds gear strength data at setpoints

    Methods
    -------
    get_torque():
        Returns the allowable pinion torque in Nm
    """

	gear_dic = {

	1 : {
		'm':8,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':2941.17, # tooth load is in kgf

	},

	2 : {
		'm':8,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':5967.74,

	},

	3 : {
		'm':8,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':3529.41,

	},

	4 : {
		'm':8,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':6895.16,

	},

	5 : {
		'm':8,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':3765.44,

	},

	6 : {
		'm':8,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':8021.41,

	},

	7 : {
		'm':8,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':4561.97,

	},

	8 : {
		'm':8,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':9371.55,

	},

	9 : {
		'm':8,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':4422.08,

	},

	10 : {
		'm':8,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':9396.92,

	},

	11 : {
		'm':8,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':5389.41,

	},

	12 : {
		'm':8,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':10988.34,

	},

	13 : {
		'm':8,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':5412.65,

	},

	14 : {
		'm':8,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':11314.2,

	},

	15 : {
		'm':8,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':6558.86,

	},

	16 : {
		'm':8,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':11872.93,

	},

	17 : {
		'm':10,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':4764.71,

	},

	18 : {
		'm':10,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':9483.87,

	},

	19 : {
		'm':10,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':5705.88,

	},

	20 : {
		'm':10,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':10838.7,

	},

	21 : {
		'm':10,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':6140.57,

	},

	22 : {
		'm':10,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':12897.8,

	},

	23 : {
		'm':10,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':7472.95,

	},

	24 : {
		'm':10,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':15185.1,

	},

	25 : {
		'm':10,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':7241.16,

	},

	26 : {
		'm':10,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':15156.3,

	},

	27 : {
		'm':10,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':8788.89,

	},

	28 : {
		'm':10,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':17460.1,

	},

	29 : {
		'm':10,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':8813.08,

	},

	30 : {
		'm':10,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':18214.5,

	},

	31 : {
		'm':10,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':10290.4,

	},

	32 : {
		'm':10,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':17935.1,

	},

	33 : {
		'm':12,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':7107.84,

	},

	34 : {
		'm':12,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':13924.7,

	},

	35 : {
		'm':12,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':8431.37,

	},

	36 : {
		'm':12,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':75698.9,

	},

	37 : {
		'm':12,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':9172.23,

	},

	38 : {
		'm':12,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':19060.8,

	},

	39 : {
		'm':12,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':11103.2,

	},

	40 : {
		'm':12,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':22343.5,

	},

	41 : {
		'm':12,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':10778.8,

	},

	42 : {
		'm':12,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':22330.3,

	},

	43 : {
		'm':12,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':12989.9,

	},

	44 : {
		'm':12,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':24300.7,

	},

	45 : {
		'm':12,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':13075.3,

	},

	46 : {
		'm':12,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':26492.9,

	},

	47 : {
		'm':12,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':15792.2,

	},

	48 : {
		'm':12,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':24863.3,

	},

	49 : {
		'm':14,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':9831.93,

	},

	50 : {
		'm':14,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':19124.42,

	},

	51 : {
		'm':14,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':11680.67,

	},

	52 : {
		'm':14,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':21382.49,

	},

	53 : {
		'm':14,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':12827.33,

	},

	54 : {
		'm':14,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':26458.2,

	},

	55 : {
		'm':14,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':15475.55,

	},

	56 : {
		'm':14,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':29998.06,

	},

	57 : {
		'm':14,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':15714.19,

	},

	58 : {
		'm':14,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':30962.22,

	},

	59 : {
		'm':14,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':18162.13,

	},

	60 : {
		'm':14,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':31958.21,

	},

	61 : {
		'm':14,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':18339.36,

	},

	62 : {
		'm':14,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':35080.02,

	},

	63 : {
		'm':14,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':22050.9,

	},

	64 : {
		'm':14,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':32645.57,

	},

	65 : {
		'm':16,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':13161.76,

	},

	66 : {
		'm':16,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':25161.29,

	},

	67 : {
		'm':16,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':15588.23,

	},

	68 : {
		'm':16,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':27862.90,

	},

	69 : {
		'm':16,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':17089.31,

	},

	70 : {
		'm':16,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':34905.08,

	},

	71 : {
		'm':16,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':20637.51,

	},

	72 : {
		'm':16,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':37843.62,

	},

	73 : {
		'm':16,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':20106.65,

	},

	74 : {
		'm':16,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':41073.66,

	},

	75 : {
		'm':16,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':24252.36,

	},

	76 : {
		'm':16,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':40353.73,

	},

	77 : {
		'm':16,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':24452.48,

	},

	78 : {
		'm':16,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':44558.40,

	},

	79 : {
		'm':16,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':29483.07,

	},

	80 : {
		'm':16,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':41136.20,

	},

	81 : {
		'm':20,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':21176.47,

	},

	82 : {
		'm':20,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':39548.38,

	},

	83 : {
		'm':20,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':24941.17,

	},

	84 : {
		'm':20,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':42967.74,

	},

	85 : {
		'm':20,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':27748.40,

	},

	86 : {
		'm':20,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':56070.50,

	},

	87 : {
		'm':20,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':33425.53,

	},

	88 : {
		'm':20,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':55339.84,

	},

	89 : {
		'm':20,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':32557.58,

	},

	90 : {
		'm':20,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':64111.28,

	},

	91 : {
		'm':20,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':39190.70,

	},

	92 : {
		'm':20,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':58867.19,

	},

	93 : {
		'm':20,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':39684.34,

	},

	94 : {
		'm':20,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':65873.80,

	},

	95 : {
		'm':20,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':47580.45,

	},

	96 : {
		'm':20,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':59867.49,

	},

	97 : {
		'm':25,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':34070.59,

	},

	98 : {
		'm':25,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':61677.42,

	},

	99 : {
		'm':25,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':39811.76,

	},

	100 : {
		'm':25,
		'h':0,
		'zp':31,
		'zg':155,
		'tl':63406.45,

	},

	101 : {
		'm':25,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':44953.58,

	},

	102 : {
		'm':25,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':87578,

	},

	103 : {
		'm':25,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':53944.29,

	},

	104 : {
		'm':25,
		'h':10,
		'zp':31,
		'zg':155,
		'tl':79648.71,

	},

	105 : {
		'm':25,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':52755.45,

	},

	106 : {
		'm':25,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':93678.26,

	},

	107 : {
		'm':25,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':63191.56,

	},

	108 : {
		'm':25,
		'h':20,
		'zp':31,
		'zg':155,
		'tl':84560.21,

	},

	109 : {
		'm':25,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':64228.52,

	},

	110 : {
		'm':25,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':95430.40,

	},

	111 : {
		'm':25,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':75395.15,

	},

	112 : {
		'm':25,
		'h':30,
		'zp':31,
		'zg':155,
		'tl':84926.36,

	},

	113 : {
		'm':6,
		'h':0,
		'zp':17,
		'zg':51,
		'tl':1568.63,
	},

	114 : {
		'm':6,
		'h':0,
		'zp':31,
		'zg':93,
		'tl':3225.81,
	},
	115 : {
		'm':6,
		'h':0,
		'zp':17,
		'zg':85,
		'tl':1862.75,
	},

	116 : {
		'm':6,
		'h':0,
		'zp':31,
		'zg':115,
		'tl':3763.44,
	},
	117 : {
		'm':6,
		'h':10,
		'zp':17,
		'zg':51,
		'tl':2027.55,
	},

	118 : {
		'm':6,
		'h':10,
		'zp':31,
		'zg':93,
		'tl':4288.68,
	},
	119 : {
		'm':6,
		'h':10,
		'zp':17,
		'zg':85,
		'tl':2413.74,
	},

	120 : {
		'm':6,
		'h':10,
		'zp':31,
		'zg':115,
		'tl':5082.88,
	},
	121 : {
		'm':6,
		'h':20,
		'zp':17,
		'zg':51,
		'tl':2395.29,
	},

	122 : {
		'm':6,
		'h':20,
		'zp':31,
		'zg':93,
		'tl':5052.11,
	},
	123 : {
		'm':6,
		'h':20,
		'zp':17,
		'zg':85,
		'tl':2855.93,
	},

	124 : {
		'm':6,
		'h':20,
		'zp':31,
		'zg':115,
		'tl':5961.49,
	},
	125 : {
		'm':6,
		'h':30,
		'zp':17,
		'zg':51,
		'tl':2886.75,
	},

	126 : {
		'm':6,
		'h':30,
		'zp':31,
		'zg':93,
		'tl':6052.87,
	},
	127 : {
		'm':6,
		'h':30,
		'zp':17,
		'zg':85,
		'tl':3481.08,
	},

	128 : {
		'm':6,
		'h':30,
		'zp':31,
		'zg':115,
		'tl':6937.52,
	},


	}

	def __init__(self, m, h, zp, zg):
		"""
        Parameters
        ----------
		m : int
        	normal module. Only allowable values are 8, 10, 12, 14, 16, 20, 25
	    h : float
	        helix angle in degrees
	    zp : float
	        Number of teeth in Pinion
	    zg : float
	        Number of teeth in Gear
		"""
		self.m = m
		self.h = h
		self.zp = zp
		self.zg = zg

		self.gr = self.zg / self.zp

	def get_torque(self):
		"""
		Returns
		-------
		float
		Returns allowable pinion torque in Nm
		"""

		# h0
		h0gr3_x17 = 17
		h0gr3_y17 = 0
		h0gr3_x31 = 31
		h0gr3_y31 = 0

		h0gr5_x17 = 17
		h0gr5_y17 = 0
		h0gr5_x31 = 31
		h0gr5_y31 = 0

		# h10
		h10gr3_x17 = 17
		h10gr3_y17 = 0
		h10gr3_x31 = 31
		h10gr3_y31 = 0

		h10gr5_x17 = 17
		h10gr5_y17 = 0
		h10gr5_x31 = 31
		h10gr5_y31 = 0

		# h20
		h20gr3_x17 = 17
		h20gr3_y17 = 0
		h20gr3_x31 = 31
		h20gr3_y31 = 0

		h20gr5_x17 = 17
		h20gr5_y17 = 0
		h20gr5_x31 = 31
		h20gr5_y31 = 0

		# h30
		h30gr3_x17 = 17
		h30gr3_y17 = 0
		h30gr3_x31 = 31
		h30gr3_y31 = 0

		h30gr5_x17 = 17
		h30gr5_y17 = 0
		h30gr5_x31 = 31
		h30gr5_y31 = 0


		# finding for h0
		for this_key, this_val in self.gear_dic.items():
			this_m = this_val['m']
			this_h = this_val['h']
			this_zp = this_val['zp']
			this_zg = this_val['zg']
			this_tl = this_val['tl']


			this_gr = int(this_zg / this_zp)

			if this_m == self.m:
				#h0
				if this_h == 0:
					if this_gr == 3:
						if this_zp == 17:
							h0gr3_y17 = this_tl
					if this_gr == 3:
						if this_zp == 31:
							h0gr3_y31 = this_tl

					if this_gr == 5:
						if this_zp == 17:
							h0gr5_y17 = this_tl
					if this_gr == 5:
						if this_zp == 31:
							h0gr5_y31 = this_tl

				#h10
				if this_h == 10:
					if this_gr == 3:
						if this_zp == 17:
							h10gr3_y17 = this_tl
					if this_gr == 3:
						if this_zp == 31:
							h10gr3_y31 = this_tl

					if this_gr == 5:
						if this_zp == 17:
							h10gr5_y17 = this_tl
					if this_gr == 5:
						if this_zp == 31:
							h10gr5_y31 = this_tl

				#h20
				if this_h == 20:
					if this_gr == 3:
						if this_zp == 17:
							h20gr3_y17 = this_tl
					if this_gr == 3:
						if this_zp == 31:
							h20gr3_y31 = this_tl

					if this_gr == 5:
						if this_zp == 17:
							h20gr5_y17 = this_tl
					if this_gr == 5:
						if this_zp == 31:
							h20gr5_y31 = this_tl

				#h30
				if this_h == 30:
					if this_gr == 3:
						if this_zp == 17:
							h30gr3_y17 = this_tl
					if this_gr == 3:
						if this_zp == 31:
							h30gr3_y31 = this_tl

					if this_gr == 5:
						if this_zp == 17:
							h30gr5_y17 = this_tl
					if this_gr == 5:
						if this_zp == 31:
							h30gr5_y31 = this_tl


		#h0
		h0_x3 = self.zp
		h0_y3 = Line(h0gr3_x17, h0gr3_y17, h0gr3_x31, h0gr3_y31).get_y(h0_x3)

		h0_x5 = self.zp
		h0_y5 = Line(h0gr5_x17, h0gr5_y17, h0gr5_x31, h0gr5_y31).get_y(h0_x5)

		h0_x = self.gr
		h0_y = Line(3, h0_y3, 5, h0_y5).get_y(h0_x)


		#h10
		h10_x3 = self.zp
		h10_y3 = Line(h10gr3_x17, h10gr3_y17, h10gr3_x31, h10gr3_y31).get_y(h10_x3)

		h10_x5 = self.zp
		h10_y5 = Line(h10gr5_x17, h10gr5_y17, h10gr5_x31, h10gr5_y31).get_y(h10_x5)

		h10_x = self.gr
		h10_y = Line(3, h10_y3, 5, h10_y5).get_y(h10_x)

		#h20
		h20_x3 = self.zp
		h20_y3 = Line(h20gr3_x17, h20gr3_y17, h20gr3_x31, h20gr3_y31).get_y(h20_x3)

		h20_x5 = self.zp
		h20_y5 = Line(h20gr5_x17, h20gr5_y17, h20gr5_x31, h20gr5_y31).get_y(h20_x5)

		h20_x = self.gr
		h20_y = Line(3, h20_y3, 5, h20_y5).get_y(h20_x)

		#h30
		h30_x3 = self.zp
		h30_y3 = Line(h30gr3_x17, h30gr3_y17, h30gr3_x31, h30gr3_y31).get_y(h30_x3)

		h30_x5 = self.zp
		h30_y5 = Line(h30gr5_x17, h30gr5_y17, h30gr5_x31, h30gr5_y31).get_y(h30_x5)

		h30_x = self.gr
		h30_y = Line(3, h30_y3, 5, h30_y5).get_y(h30_x)

		y = 0

		if self.h >= 0 and self.h < 10:
			y = Line(0, h0_y, 10, h10_y).get_y(self.h)
		elif self.h >= 10 and self.h < 20:
			y = Line(10, h10_y, 20, h20_y).get_y(self.h)
		else:
			y = Line(20, h20_y, 30, h30_y).get_y(self.h)

		pcd_p = self.m * self.zp / math.cos(self.h * math.pi / 180)
		torque_p = y * pcd_p / 2000
		
		return torque_p * 10  # pinion torque in Nm


# program test
# gso = GearStrength(6, 0, 17, 51)
# trq_p = gso.get_torque()
# print(round(trq_p,0))

