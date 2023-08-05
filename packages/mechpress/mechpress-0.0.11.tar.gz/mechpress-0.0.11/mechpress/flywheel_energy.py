import math

class FlywheelEnergy:
	"""
    A class for calculation of flywheel of a mechanical press
    ...
    About Units
	* all length in mm
	* power in kW
	* torque in Nm
	* time in sec
	* inertia in kgm2
	* input angle in deg
	* input speed in rpm

    Methods
    -------
    get_spm_lst():
    	list of spm from min to max separated by 1
    get_spm_cyc_min_lst():
    	list of min spm in a cycle from min to max spm separated by 1
    get_spm_cyc_max_lst():
    	list of max spm in a cycle from min to max spm separated by 1
    get_energy_lst():
    	energy at each spm
    get_dw_pc_lst():
    	list of % speed reduction in a cycle for min to max spm
    get_t_mot_lst():
    	list of available motor torque from min to max spm
    get_energy_sspm1_lst():
    	list of energy values from min to max spm in sspm mode for sspm1 
    get_energy_sspm2_lst():
    	list of energy values from min to max spm in sspm mode for sspm1 
    get_n_mot_min():
    	rpm of motor at min press spm
    get_n_mot_max():
    	rpm of motor at max press spm
    get_npc_mot_min():
    	% of motor rated speed when press is set at min spm
    get_npc_mot_max():
    	% of motor rated speed when press is set at max spm
    get_v_belt():
    	linear speed of belt
    get_n_fw_max():
    	flywheel rpm when press is running at max spm
    get_spm_press_bas():
    	press spm when motor is running at rated rpm
    get_energy_max_cap():
    	max theoritically delieverable enenrgy calculated by the multiplication of a constant, 
    	driveshaft torque and forming angle. This ignores all other things like motor power, inertia etc. 
    """
	def __init__(self, pcd_fw, pcd_pu, gr_press, pow_mot, n_mot_rtd, j_mot, j_fw, 
		th_form, spm_min, spm_max, dw_pc, eff, sspm1, sspm2, trq_ds, energy_limit):
		"""
        Parameters
        ----------
		pcd_fw : float
        	flywheel pcd in mm
	    pcd_pu : float
	        pulley pcd in mm
	    gr_press : float
	        press gear ratio (only gears, not flywheel-pulley)
	    pow_mot : float
	        motor power in kW
	    n_mot_rtd : float
	        motor rated rpm
	    j_mot : float
	        motor inertia in kgm2
	    j_fw : float
	        flywheel inertia in kgm2
	    th_form : float
	        forming duration angle in degree
	    spm_min : float
	        min spm of press
	    spm_max : float
	        max spm of press
	    dw_pc : float
	        percentage speed reduction of flywheel in 1 stroke (0.2 generally)
	    eff : float
	        overall efficiency (0.85 generally)
	    sspm1 : float
	        sspm value 1 (8 generally)
	    sspm2 : float
	        sspm value 2 (12 generally)
	    trq_ds : float
	        approximate driveshaft torque in Nm (10000 to 150000)
	    energy_limit : float
	        max energy limit in kJ. Graph will not exceed beyond this 
	        limit even if mathematically possible

		"""
		self.pcd_fw = pcd_fw  # flywheel pcd
		self.pcd_pu = pcd_pu  # pulley pcd
		self.gr_press = gr_press  # press gear ratio
		self.pow_mot = pow_mot  # motor power in kw
		self.n_mot_rtd = n_mot_rtd  # rated rpm of motor
		self.j_mot = j_mot  # motor inertia in kgm2
		self.j_fw = j_fw  # flywheel inertia in kgm2
		self.th_form = th_form  # angle of forming in deg
		self.spm_min = spm_min
		self.spm_max = spm_max
		self.dw_pc = dw_pc  # system efficiency
		self.eff = eff  # system efficiency
		self.sspm1 = sspm1
		self.sspm2 = sspm2
		self.trq_ds = trq_ds  # driveshaft's design torque in Nm
		self.energy_limit = energy_limit  # user defined limit of energy deliever capacity

		self.DW_PC_CONST = dw_pc

		# declare all list
		self.spm_lst = []
		self.energy_lst = []
		self.dw_pc_lst = []
		self.t_mot_lst = []
		self.spm_cyc_min_lst = []
		self.spm_cyc_max_lst = []
		self.energy_sspm1_lst = []
		self.energy_sspm2_lst = []

		# clear all list
		self.spm_lst.clear()
		self.energy_lst.clear()
		self.dw_pc_lst.clear()
		self.t_mot_lst.clear()
		self.spm_cyc_min_lst.clear()
		self.spm_cyc_max_lst.clear()
		self.energy_sspm1_lst.clear()
		self.energy_sspm2_lst.clear()

		
		# calculations
		self.gr_fwp = self.pcd_fw/self.pcd_pu  # flywheel - pulley gr
		self.w_mot_rtd = 2 * math.pi * self.n_mot_rtd / 60  # ang rated speed of motor
		self.t_mot_rtd = (self.eff) * self.pow_mot * 1000 / self.w_mot_rtd  # motor rated torque in Nm (multiplied by efficiency)
		self.j_m_tot = self.j_mot + self.j_fw / self.gr_fwp**2
		self.th_form_rad = self.th_form * math.pi / 180  # angle of forming in rad
		self.th_acc = 360 - self.th_form  # accelerating angle where flywheel can store energy
		self.th_acc_rad = self.th_acc * math.pi / 180  # angle of forming in rad
		self.energy_max_cap = self.trq_ds * (self.th_form_rad * self.gr_fwp * self.gr_press) / 1000  # maximum energy (in kJ) which can be delievered considering limitation of driveshaft torque and forming angle

		
		for spm in range(self.spm_min, self.spm_max + 1):
			# dw_pc = str_to_float(dw_pc_ent.get())  # allowable % slowdown in motor speed
			self.dw_pc = self.DW_PC_CONST
			t_cycle = (60/spm) # cycle time in s

			t_form = (self.th_form/360) * t_cycle  # forming time
			t_acc = t_cycle - t_form  # acc time in sec (from eof to next cycle sof)

			n_fw = spm * self.gr_press  # flywheel speed in rpm
			n_mot = n_fw * self.gr_fwp  # motor speed in rpm
			w_mot = 2 * math.pi * n_mot / 60  # ang rated speed of motor

			# to find out the allowable motor torque at current motor speed
			t_mot = 0  # allowable motor torque at current speed
			# if n_mot < n_mot_rtd:
			# 	if n_mot < 0.4 * n_mot_rtd:
			# 		t_mot = t_mot_rtd - (0.4 * n_mot_rtd / (0.5 * t_mot_rtd)) * (0.4 * n_mot_rtd - n_mot)
			# 	else:
			# 		t_mot = t_mot_rtd
			# else:
			# 	t_mot = (eff) * pow_mot * 1000 / w_mot
			if n_mot < self.n_mot_rtd:
				t_mot = self.t_mot_rtd
			else:
				t_mot = (self.eff) * self.pow_mot * 1000 / w_mot

			alp_mot = t_mot / self.j_m_tot  # ang acc at motor in rad/s2


			# to find out the percentage reduction in speed permitted at the current spm
			wf = (2 * w_mot + alp_mot * t_acc) / 2  # final speed of motor
			wi = wf - alp_mot * t_acc  # initial speed of motor
			r = 1 - wi/wf  # percentage reduction in speed

			# if conditions permit lower '% speed reduction' than given in input, we will consider that lower value
			if r < self.dw_pc:
				self.dw_pc = r

			n_mot_sof_all = spm * self.gr_press * self.gr_fwp * (2 / (2 - self.dw_pc))
			w_mot_sof_all = 2 * math.pi * n_mot_sof_all / 60  # motor w at End Of Forming (allowable)

			n_mot_eof_all = (1 - self.dw_pc) * n_mot_sof_all  # motor rpm at End Of Forming (allowable)
			w_mot_eof_all = 2 * math.pi * n_mot_eof_all / 60  # motor w at End Of Forming (allowable)

			e_fw = 0.5 * self.j_m_tot * (w_mot_sof_all**2 - w_mot_eof_all**2) / 1000  # work energy supplied by flywheel in kJ
			e_mot = t_mot * (self.th_form_rad * self.gr_fwp * self.gr_fwp) / 1000  # torque x angle = energy delievered by motor directly in forming zone
			e_tot = min(e_fw + e_mot, self.energy_max_cap, self.energy_limit)  # # total work energy in kJ in continuous mode. It s the minimum of available energy or delieverable energy)

			# spm variation in a cycle
			spm_cyc_min = n_mot_eof_all / (self.gr_fwp * self.gr_press)  # min ecc gear rpm in a cycle
			spm_cyc_max = n_mot_sof_all / (self.gr_fwp * self.gr_press)  # max ecc gear rpm in a cycle

			self.spm_lst.append(spm)
			self.spm_cyc_min_lst.append(spm_cyc_min)
			self.spm_cyc_max_lst.append(spm_cyc_max)
			self.energy_lst.append(e_tot)
			self.dw_pc_lst.append(self.dw_pc * 100)
			self.t_mot_lst.append(t_mot)


			# calculation of sspm mode

			# calculating sspm1
			t_cycle_sspm1 = (60/self.sspm1) # cycle time for sspm1 value in s
			t_acc_sspm1 = t_cycle_sspm1 - t_form  # acc time in sec (from eof to next cycle sof)
			# resetting dw_pc 
			# dw_pc = str_to_float(dw_pc_ent.get())  # allowable % slowdown in motor speed
			self.dw_pc = self.DW_PC_CONST

			# to find out the percentage reduction in speed permitted at the current spm
			wf1 = (2 * w_mot + alp_mot * t_acc_sspm1) / 2  # final speed of motor
			wi1 = wf1 - alp_mot * t_acc_sspm1  # initial speed of motor
			r1 = 1 - wi1/wf1  # percentage reduction in speed

			# if conditions permit lower '% speed reduction' than given in input, we will consider that lower value
			if r1 < self.dw_pc:
				self.dw_pc = r1

			n_mot_sof_all1 = spm * self.gr_press * self.gr_fwp * (2 / (2 - self.dw_pc))
			w_mot_sof_all1 = 2 * math.pi * n_mot_sof_all1 / 60  # motor w at End Of Forming (allowable)

			n_mot_eof_all1 = (1 - self.dw_pc) * n_mot_sof_all1  # motor rpm at End Of Forming (allowable)
			w_mot_eof_all1 = 2 * math.pi * n_mot_eof_all1 / 60  # motor w at End Of Forming (allowable)

			e_fw1 = 0.5 * self.j_m_tot * (w_mot_sof_all1**2 - w_mot_eof_all1**2) / 1000  # work energy supplied by flywheel in kJ
			e_mot1 = t_mot * (self.th_form_rad * self.gr_fwp * self.gr_fwp) / 1000  # torque x angle = energy delievered by motor directly in forming zone
			e_tot1 = min(e_fw1 + e_mot1, self.energy_max_cap, self.energy_limit)  # total work energy in kJ in intermittent mode. It s the minimum of available energy or delieverable energy)

			if spm < self.sspm1:	
				self.energy_sspm1_lst.append(None)
			else:
				self.energy_sspm1_lst.append(e_tot1)


			# calculating sspm2
			t_cycle_sspm2 = (60/self.sspm2) # cycle time for sspm2 value in s
			t_acc_sspm2 = t_cycle_sspm2 - t_form  # acc time in sec (from eof to next cycle sof)
			# resetting dw_pc 
			# dw_pc = str_to_float(dw_pc_ent.get())  # allowable % slowdown in motor speed
			self.dw_pc = self.DW_PC_CONST

			# to find out the percentage reduction in speed permitted at the current spm
			wf2 = (2 * w_mot + alp_mot * t_acc_sspm2) / 2  # final speed of motor
			wi2 = wf2 - alp_mot * t_acc_sspm2  # initial speed of motor
			r2 = 1 - wi2/wf2  # percentage reduction in speed

			# if conditions permit lower '% speed reduction' than given in input, we will consider that lower value
			if r2 < self.dw_pc:
				self.dw_pc = r2

			n_mot_sof_all2 = spm * self.gr_press * self.gr_fwp * (2 / (2 - self.dw_pc))
			w_mot_sof_all2 = 2 * math.pi * n_mot_sof_all2 / 60  # motor w at End Of Forming (allowable)

			n_mot_eof_all2 = (1 - self.dw_pc) * n_mot_sof_all2  # motor rpm at End Of Forming (allowable)
			w_mot_eof_all2 = 2 * math.pi * n_mot_eof_all2 / 60  # motor w at End Of Forming (allowable)

			e_fw2 = 0.5 * self.j_m_tot * (w_mot_sof_all2**2 - w_mot_eof_all2**2) / 1000  # work energy supplied by flywheel in kJ
			e_mot2 = t_mot * (self.th_form_rad * self.gr_fwp * self.gr_fwp) / 1000  # torque x angle = energy delievered by motor directly in forming zone
			e_tot2 = min(e_fw2 + e_mot2, self.energy_max_cap, self.energy_limit)  # total work energy in kJ in intermittent mode. It s the minimum of available energy or delieverable energy)

			if spm < self.sspm2:	
				self.energy_sspm2_lst.append(None)
			else:
				self.energy_sspm2_lst.append(e_tot2)
			

		# more calculations

		self.n_mot_min = self.spm_min * self.gr_press * self.gr_fwp

		self.n_mot_max = self.spm_max * self.gr_press * self.gr_fwp

		self.npc_mot_min = (self.n_mot_min / self.n_mot_rtd) * 100

		self.npc_mot_max = (self.n_mot_max / self.n_mot_rtd) * 100

		self.v_belt = 2 * math.pi * (self.n_mot_max / self.gr_fwp) / 60

		self.n_fw_max = self.n_mot_max / self.gr_fwp

		self.spm_press_bas = self.n_mot_rtd / (self.gr_press * self.gr_fwp)
	

	# return lists
	def get_spm_lst(self):
		"""
		Returns
		-------
		list
		list of spm from min to max separated by 1
		"""
		return self.spm_lst

	def get_spm_cyc_min_lst(self):
		"""
		Returns
		-------
		list
		list of min spm in a cycle from min to max spm separated by 1
		"""
		return self.spm_cyc_min_lst
	
	def get_spm_cyc_max_lst(self):
		"""
		Returns
		-------
		list
		list of max spm in a cycle from min to max spm separated by 1
		"""
		return self.spm_cyc_max_lst

	def get_energy_lst(self):
		"""
		Returns
		-------
		list
		energy at each spm
		"""
		return self.energy_lst

	def get_dw_pc_lst(self):
		"""
		Returns
		-------
		list
		list of % speed reduction in a cycle for min to max spm
		"""
		return self.dw_pc_lst

	def get_t_mot_lst(self):
		"""
		Returns
		-------
		list
		list of available motor torque from min to max spm
		"""
		return self.t_mot_lst

	def get_energy_sspm1_lst(self):
		"""
		Returns
		-------
		list
		list of energy values from min to max spm in sspm mode for sspm1
		"""
		return self.energy_sspm1_lst

	def get_energy_sspm2_lst(self):
		"""
		Returns
		-------
		list
		list of energy values from min to max spm in sspm mode for sspm1
		"""
		return self.energy_sspm2_lst


	# return individual values

	def get_n_mot_min(self):
		"""
		Returns
		-------
		float
		rpm of motor at min press spm
		"""
		return self.n_mot_min

	def get_n_mot_max(self):
		"""
		Returns
		-------
		float
		rpm of motor at max press spm
		"""
		return self.n_mot_max

	def get_npc_mot_min(self):
		"""
		Returns
		-------
		float
		% of motor rated speed when press is set at min spm
		"""
		return self.npc_mot_min

	def get_npc_mot_max(self):
		"""
		Returns
		-------
		float
		% of motor rated speed when press is set at max spm
		"""
		return self.npc_mot_max

	def get_v_belt(self):
		"""
		Returns
		-------
		float
		linear speed of belt
		"""
		return self.v_belt

	def get_n_fw_max(self):
		"""
		Returns
		-------
		float
		flywheel rpm when press is running at max spm
		"""
		return self.n_fw_max

	def get_spm_press_bas(self):
		"""
		Returns
		-------
		float
		press spm when motor is running at rated rpm
		"""
		return self.spm_press_bas

	def get_energy_max_cap(self):
		"""
		Returns
		-------
		float
		max energy limit in kJ. Graph will not exceed beyond this 
	    limit even if mathematically possible
		"""
		return self.energy_max_cap

# program test
# pcd_fw, pcd_pu, gr_press, pow_mot, n_mot_rtd, j_mot, j_fw, 
# th_form, spm_min, spm_max, dw_pc, eff, sspm1, sspm2, trq_ds, energy_limit

# fw = FlywheelEnergy(1800, 360, 18, 315, 1500, 5, 5000, 45, 10, 25, 0.2, 0.85,
# 	8, 12, 150000, 3000)
# print(fw.get_energy_max_cap())
