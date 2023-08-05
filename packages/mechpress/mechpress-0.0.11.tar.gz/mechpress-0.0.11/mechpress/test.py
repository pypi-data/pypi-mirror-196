# this is only a test file from where, implementation of all modules can be refered
# this will work only after installing mechpress package

# Module 1
# from mechpress import ed
# import math

# stroke = 0.150  # m
# conrod = 0.9  # m
# rd = 0.013  # m
# fr = 6300000  # N

# th2_deg = 110  # deg
# th2_rad = math.pi * th2_deg / 180  # rad
# n2 = 20  # rpm of crank
# w2 = 2 * math.pi * n2 / 60  # ang vel of crank

# press1 = ed.ED(stroke, conrod, rd, fr)  # object press1

# alp_rad = press1.get_alp_rad()
# print("alp_rad: ", alp_rad)

# beta_rad = press1.get_beta_rad()
# print("beta_rad: ", beta_rad)

# t_eg = press1.get_torque()
# print("EG torque is: ", t_eg)

# fbos = press1.get_fbos(th2_rad)
# print("FBOS: ", fbos)

# vel = press1.get_slide_vel(th2_rad, w2)
# print("Slide vel: ", vel)

# acc = press1.get_slide_acc(th2_rad, w2, 0)
# print("Slide acc: ", acc)

# force = press1.get_f(th2_rad)
# print("Press force: ", force)



# Module 2
# import matplotlib.pyplot as plt
# import math
# from mechpress import ld

# press2 = ld.LD(0.260, 0.8, 0.9, 1.175, 0.375, 2.33923, 1.175, 0, 1.175, 10000000, 0.013)

# print("Stroke: ", press2.get_stroke())
# print("EG torque: ", press2.get_eg_torque())

# th2_lst = press2.get_th2_decideg_lst()
# fbos_lst = press2.get_fbos_lst()
# vel_lst = press2.get_vel_lst(2)

# print("TDC: ", press2.get_th2_tdc())
# print("BDC: ", press2.get_th2_bdc())

# plt.plot(th2_lst, fbos_lst)
# plt.plot(th2_lst, vel_lst)
# plt.show()



# Module 3
# from mechpress import section_mi

# my_sec = section_mi.Section_mi(100, 10, 10, 100, 100, 10, 5, 25, 5, 25)
# print(my_sec.get_centroid())
# print(my_sec.get_case())
# print(my_sec.get_inertia())
# print(my_sec.get_section_area())




# Module 4
# from mechpress import crown
# import math

# c1 = crown.Crown(12500000, 5, 3, 1.2, 0.4245, 0.2, 2)
# print("Bending stress (MPa): ", c1.get_sb() / 1000000)
# print("Shear stress (MPa): ", c1.get_ss() / 1000000)
# print("Def in bending (mm): ", c1.get_def_b() * 1000)
# print("Def in shear (mm): ", c1.get_def_s() * 1000)



# Module 5
# from mechpress import bed

# b1 = bed.Bed(12500000, 5, 4, 0.66, 1.2, 0.4245, 0.2, 2)
# print("Bending stress (MPa): ", b1.get_sb() / 1000000)
# print("Shear stress (MPa): ", b1.get_ss() / 1000000)
# print("Def in bending (mm): ", b1.get_def_b() * 1000)
# print("Def in shear (mm): ", b1.get_def_s() * 1000)




# Module 6
# from mechpress import slide

# s1 = slide.Slide(12500000, 3, 4, 0.66, 1.2, 0.4245, 0.2, 2)
# print("Bending stress (MPa): ", s1.get_sb() / 1000000)
# print("Shear stress (MPa): ", s1.get_ss() / 1000000)
# print("Def in bending (mm): ", s1.get_def_b() * 1000)
# print("Def in shear (mm): ", s1.get_def_s() * 1000)




# Module 7
# from mechpress import polynomial_345
# import math
# import matplotlib.pyplot as plt

# curveGen = polynomial_345.Polynomial_345(800, 1, 0.2)
# T_ms = curveGen.t_fcn()
# t_lst = curveGen.t_lst_fcn()
# s_lst = curveGen.s_lst_fcn()
# v_lst = curveGen.v_lst_fcn()
# a_lst = curveGen.a_lst_fcn()
# v_avg = curveGen.v_avg_fcn()
# v_pk = curveGen.v_max_fcn()
# a_pk = curveGen.a_max_fcn()
# a1_rms = curveGen.a1_rms_fcn()
# a_rms = curveGen.a_rms_fcn()

# plt.plot(t_lst, s_lst)
# plt.plot(t_lst, v_lst)
# plt.plot(t_lst, a_lst)
# plt.show()



# Module 8
# from mechpress import automation_345
# import math
# import matplotlib.pyplot as plt

# axis1 = automation_345.Automation_345(1200, 2, 90, 50, 0.02, 500, 0.02, 0.005, 0.003, 10, 0.5)
# t_lst = axis1.get_t_lst()
# s_lst = axis1.get_s_lst()
# v_lst = axis1.get_v_lst()
# trq_lst = axis1.get_trq_mot_lst()
# n_lst = axis1.get_n_mot_lst()

# t_mot_rms = axis1.get_t_mot_rms()
# t_mot_pk = axis1.get_t_mot_pk()
# n_mot_avg = axis1.get_n_mot_avg()
# n_mot_pk = axis1.get_n_mot_pk()
# a_pk = axis1.get_a_pk()
# v_pk = axis1.get_v_pk()

# print("RMS torque of motor (Nm): ", t_mot_rms)
# print("Peak torque of motor (Nm): ", t_mot_pk)
# print("Average rpm of motor: ", n_mot_avg)
# print("Peak rpm of motor: ", n_mot_pk)
# print("Peak acceleration (m/s2): ", a_pk)
# print("Peak velocity (mm/s): ", v_pk)



# Module 9
# from mechpress import polynomial_345_cv
# import matplotlib.pyplot as plt
# ob1 = polynomial_345_cv.Polynomial_345_cv(200, 2.4, 0, 0.5)
# xAxis_lst = ob1.t_lst_fcn()
# yAxis_lst = ob1.s_lst_fcn()
# plt.plot(xAxis_lst, yAxis_lst)
# plt.show()



# Module 10
# from mechpress import automation_345_cv
# axis1 = automation_345_cv.Automation_345_cv(1200, 2, 0.5, 90, 50, 0.02, 500, 0.02, 0.005, 0.003, 10, 0.5)
# t_lst = axis1.get_t_lst()
# s_lst = axis1.get_s_lst()
# v_lst = axis1.get_v_lst()
# trq_lst = axis1.get_trq_mot_lst()
# n_lst = axis1.get_n_mot_lst()

# t_mot_rms = axis1.get_t_mot_rms()
# t_mot_pk = axis1.get_t_mot_pk()
# n_mot_avg = axis1.get_n_mot_avg()
# n_mot_pk = axis1.get_n_mot_pk()
# a_pk = axis1.get_a_pk()
# v_pk = axis1.get_v_pk()

# print("RMS torque of motor (Nm): ", t_mot_rms)
# print("Peak torque of motor (Nm): ", t_mot_pk)
# print("Average rpm of motor: ", n_mot_avg)
# print("Peak rpm of motor: ", n_mot_pk)
# print("Peak acceleration (m/s2): ", a_pk)
# print("Peak velocity (mm/s): ", v_pk)



# Module 11
# from mechpress import shaft
# s1 = shaft.Shaft(10000, 25000, 5000, 35000, 2, 2, 180_000_000, 240_000_000, 1.5)
# print("Shaft diameter (mm): ", s1.get_shaft_dia() * 1000)



# Module 12
# from mechpress import gear_geometry
# a = gear_geometry.GearGeometry(10, 17, 93)
# print("Transverse module")
# print(a.getMt())
# print("\n")
# print("pcd1")
# print(a.getPcd1())
# print("\n")
# print("pcd2")
# print(a.getPcd2())
# print("\n")
# print("tip circle1")
# print(a.getTipCirDia1_S0())
# print("\n")
# print("tip circle2")
# print(a.getTipCirDia2_S0())
# print("\n")
# print("Normal tooth thickness on pcd")
# print(a.norToothThkOnPcd())
# print("\n")
# print("Transverse tooth thickness on pcd")
# print(a.transToothThkOnPcd())
# print("\n")
# print("Root circle dia1")
# print(a.getRootCirDia1())
# print("\n")
# print("Root circle dia2")
# print(a.getRootCirDia2())
# print("\n")
# print("Transverse pressure angle")
# print(a.getAlpt())
# print("\n")
# print("Working pressure angle")
# print(a.getAlptW())
# print("\n")
# print("Tip circle dia1 without topping")
# print(a.getTipCirWotDia1_S())
# print("\n")
# print("Tip circle dia2 without topping")
# print(a.getTipCirWotDia2_S())
# print("\n")
# print("Actual center distance")
# print(a.getA_S())
# print("\n")
# print("Tip circle dia1 after topping")
# print(a.getTipCirWtDia1_S())
# print("\n")
# print("Tip circle dia2 after topping")
# print(a.getTipCirWtDia2_S())
# print("\n")
# print("Topping")
# print(a.getYm())
# print("\n")
# print("Top clearance")
# print(a.getTopClearance())
# print("\n")
# print("Working circle dia1")
# print(a.workCirDia1())
# print("\n")
# print("Working circle dia2")
# print(a.workCirDia2())


# Module 13
# from mechpress import gear_strength
# gso = gear_strength.GearStrength(6, 0, 17, 51)
# trq_p = gso.get_torque()
# print(round(trq_p,0))


# Module 14
# from mechpress import line_equation
# my_line = line_equation.Line(5, 5, 10, 10)
# print(my_line.get_y(20))


# Module 15
# from mechpress import power_screw
# ps = power_screw.PowerScrew(0.1, 10000, 0.05, 0.025, 30*math.pi/180, 0.15, 0.05)
# tr = ps.get_tr()
# tl = ps.get_tl()
# eff = ps.get_eff()
# print(tr)
# print(tl)
# print(eff)


# Module 16
# from mechpress import hydrodynamic_bush
# bush = hydrodynamic_bush.HydrodynamicBush(1000000, 1, 0.5, 0.001, 50, 0.1275)
# ans_dic = bush.hyd_dyn_bush()
# print(ans_dic)

# Module 17
# from mechpress import key_size
# ks = key_size.KeySize(100)
# answer_dic = ks.get_key_data()
# key_width = answer_dic['b']
# key_height = answer_dic['h']
# keyway_depth_shaft = answer_dic['ds']
# keyway_depth_hub = answer_dic['dh']
# print("key width:", key_width)
# print("key height", key_height)
# print("keyway depth in shaft", keyway_depth_shaft)
# print("keyway depth in hub", keyway_depth_hub)

# Module 18
# from mechpress import metric_thread
# my_screw = metric_thread.MetricThread(24, 3)
# print(my_screw.get_ext_dmin())
# print(my_screw.get_int_dmin())

# Module 19
# from mechpress import flywheel_energy
# fw = flywheel_energy.FlywheelEnergy(1800, 360, 18, 315, 1500, 5, 5000, 45, 10, 25, 0.2, 0.85,
# 	8, 12, 150000, 3000)
# print(fw.get_spm_lst())
# print(fw.get_spm_cyc_min_lst())
# print(fw.get_spm_cyc_max_lst())
