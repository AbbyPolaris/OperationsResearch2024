\* Source Pyomo model name=OR1 *\

max 
revenue:
+520 g(A_Tehran_Mashhad)
+540 g(A_Tehran_Kerman)
+490 g(A_Tehran_Ahvaz)
+500 g(A_Tehran_Tabriz)
+520 g(A_Isfahan_Mashhad)
+540 g(A_Isfahan_Kerman)
+490 g(A_Isfahan_Ahvaz)
+500 g(A_Isfahan_Tabriz)
+700 g(B_Tehran_Mashhad)
+690 g(B_Tehran_Kerman)
+730 g(B_Tehran_Ahvaz)
+710 g(B_Tehran_Tabriz)
+700 g(B_Isfahan_Mashhad)
+690 g(B_Isfahan_Kerman)
+730 g(B_Isfahan_Ahvaz)
+710 g(B_Isfahan_Tabriz)
-45 Extracted_ore(1)
-65 Extracted_ore(2)
-70 Extracted_ore(3)
-375 t(A_1_Tehran)
-375 t(A_1_Isfahan)
-390 t(A_2_Tehran)
-390 t(A_2_Isfahan)
-520 t(B_1_Tehran)
-520 t(B_1_Isfahan)
-540 t(B_2_Tehran)
-540 t(B_2_Isfahan)
-120 h(1)
-90 h(2)
-180 B(1_Tehran)
-210 B(1_Isfahan)
-240 B(2_Tehran)
-220 B(2_Isfahan)
-200 B(Main_Tehran)
-230 B(Main_Isfahan)
-110 G(Tehran_Mashhad)
-85 G(Tehran_Kerman)
-120 G(Tehran_Ahvaz)
-100 G(Tehran_Tabriz)
-100 G(Isfahan_Mashhad)
-100 G(Isfahan_Kerman)
-110 G(Isfahan_Ahvaz)
-90 G(Isfahan_Tabriz)

s.t.

c_u_Max_extracted_ore_limit(1)_:
+1 Extracted_ore(1)
<= 560.0

c_u_Max_extracted_ore_limit(2)_:
+1 Extracted_ore(2)
<= 1000.0

c_u_Max_extracted_ore_limit(3)_:
+1 Extracted_ore(3)
<= 1440.0

c_u_Alloy_sum_limit(A)_:
+1 U(A)
-1 Z(1_A)
-1 Z(2_A)
-1 Z(3_A)
-1 C(1_A)
-1 C(2_A)
-1 C(3_A)
-1 A(1_A)
-1 A(2_A)
-1 A(3_A)
-1 F(1_A)
-1 F(2_A)
-1 F(3_A)
<= 0

c_u_Alloy_sum_limit(B)_:
+1 U(B)
-1 Z(1_B)
-1 Z(2_B)
-1 Z(3_B)
-1 C(1_B)
-1 C(2_B)
-1 C(3_B)
-1 A(1_B)
-1 A(2_B)
-1 A(3_B)
-1 F(1_B)
-1 F(2_B)
-1 F(3_B)
<= 0

c_u_Metal_sum_limit_Z(1)_:
-0.25 Extracted_ore(1)
+1 Z(1_A)
+1 Z(1_B)
<= 0

c_u_Metal_sum_limit_Z(2)_:
-0.15 Extracted_ore(2)
+1 Z(2_A)
+1 Z(2_B)
<= 0

c_u_Metal_sum_limit_Z(3)_:
-0.65 Extracted_ore(3)
+1 Z(3_A)
+1 Z(3_B)
<= 0

c_u_Metal_sum_limit_F(1)_:
-0.05 Extracted_ore(1)
+1 F(1_A)
+1 F(1_B)
<= 0

c_u_Metal_sum_limit_F(2)_:
-0.2 Extracted_ore(2)
+1 F(2_A)
+1 F(2_B)
<= 0

c_u_Metal_sum_limit_F(3)_:
-0.05 Extracted_ore(3)
+1 F(3_A)
+1 F(3_B)
<= 0

c_u_Metal_sum_limit_C(1)_:
-0.3 Extracted_ore(1)
+1 C(1_A)
+1 C(1_B)
<= 0

c_u_Metal_sum_limit_C(2)_:
-0.25 Extracted_ore(2)
+1 C(2_A)
+1 C(2_B)
<= 0

c_u_Metal_sum_limit_C(3)_:
-0.05 Extracted_ore(3)
+1 C(3_A)
+1 C(3_B)
<= 0

c_u_Metal_sum_limit_A(1)_:
-0.35 Extracted_ore(1)
+1 A(1_A)
+1 A(1_B)
<= 0

c_u_Metal_sum_limit_A(2)_:
-0.3 Extracted_ore(2)
+1 A(2_A)
+1 A(2_B)
<= 0

c_u_Metal_sum_limit_A(3)_:
-0.25 Extracted_ore(3)
+1 A(3_A)
+1 A(3_B)
<= 0

c_u_Metal_in_alloy_limit_A_Z_f_:
-1 Z(1_A)
-1 Z(2_A)
-1 Z(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_Z_t_:
-0.8 U(A)
+1 Z(1_A)
+1 Z(2_A)
+1 Z(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_C_f_:
-1 C(1_A)
-1 C(2_A)
-1 C(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_C_t_:
-1 U(A)
+1 C(1_A)
+1 C(2_A)
+1 C(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_A_f_:
+0.55 U(A)
-1 A(1_A)
-1 A(2_A)
-1 A(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_A_t_:
-1 U(A)
+1 A(1_A)
+1 A(2_A)
+1 A(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_F_f_:
-1 F(1_A)
-1 F(2_A)
-1 F(3_A)
<= 0

c_u_Metal_in_alloy_limit_A_F_t_:
-0.25 U(A)
+1 F(1_A)
+1 F(2_A)
+1 F(3_A)
<= 0

c_u_Metal_in_alloy_limit_B_Z_f_:
-1 Z(1_B)
-1 Z(2_B)
-1 Z(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_Z_t_:
-1 U(B)
+1 Z(1_B)
+1 Z(2_B)
+1 Z(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_C_f_:
+0.35 U(B)
-1 C(1_B)
-1 C(2_B)
-1 C(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_C_t_:
-1 U(B)
+1 C(1_B)
+1 C(2_B)
+1 C(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_A_f_:
-1 A(1_B)
-1 A(2_B)
-1 A(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_A_t_:
-0.7 U(B)
+1 A(1_B)
+1 A(2_B)
+1 A(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_F_f_:
+0.45 U(B)
-1 F(1_B)
-1 F(2_B)
-1 F(3_B)
<= 0

c_u_Metal_in_alloy_limit_B_F_t_:
-0.7 U(B)
+1 F(1_B)
+1 F(2_B)
+1 F(3_B)
<= 0

c_u_Export_from_main_fac_limit(A)_:
+1 t(A_Main_Tehran)
+1 t(A_Main_Isfahan)
-1 U(A)
<= 0

c_u_Export_from_main_fac_limit(B)_:
+1 t(B_Main_Tehran)
+1 t(B_Main_Isfahan)
-1 U(B)
<= 0

c_u_buy_from_fac_limit_f(1)_:
-1 t(A_1_Tehran)
-1 t(A_1_Isfahan)
-1 t(B_1_Tehran)
-1 t(B_1_Isfahan)
+2000 h(1)
<= 0

c_u_buy_from_fac_limit_f(2)_:
-1 t(A_2_Tehran)
-1 t(A_2_Isfahan)
-1 t(B_2_Tehran)
-1 t(B_2_Isfahan)
+2500 h(2)
<= 0

c_u_buy_from_fac_limit_t(1)_:
+1 t(A_1_Tehran)
+1 t(A_1_Isfahan)
+1 t(B_1_Tehran)
+1 t(B_1_Isfahan)
-5000 h(1)
<= 0

c_u_buy_from_fac_limit_t(2)_:
+1 t(A_2_Tehran)
+1 t(A_2_Isfahan)
+1 t(B_2_Tehran)
+1 t(B_2_Isfahan)
-6000 h(2)
<= 0

c_u_container_limit(1_Tehran)_:
+1 t(A_1_Tehran)
+1 t(B_1_Tehran)
-100 B(1_Tehran)
<= 0

c_u_container_limit(1_Isfahan)_:
+1 t(A_1_Isfahan)
+1 t(B_1_Isfahan)
-100 B(1_Isfahan)
<= 0

c_u_container_limit(2_Tehran)_:
+1 t(A_2_Tehran)
+1 t(B_2_Tehran)
-100 B(2_Tehran)
<= 0

c_u_container_limit(2_Isfahan)_:
+1 t(A_2_Isfahan)
+1 t(B_2_Isfahan)
-100 B(2_Isfahan)
<= 0

c_u_container_limit(Main_Tehran)_:
+1 t(A_Main_Tehran)
+1 t(B_Main_Tehran)
-100 B(Main_Tehran)
<= 0

c_u_container_limit(Main_Isfahan)_:
+1 t(A_Main_Isfahan)
+1 t(B_Main_Isfahan)
-100 B(Main_Isfahan)
<= 0

c_u_transportation_limit_t(1_Tehran)_:
-30 h(1)
+1 B(1_Tehran)
<= 0

c_u_transportation_limit_t(1_Isfahan)_:
-30 h(1)
+1 B(1_Isfahan)
<= 0

c_u_transportation_limit_t(2_Tehran)_:
-25 h(2)
+1 B(2_Tehran)
<= 0

c_u_transportation_limit_t(2_Isfahan)_:
-15 h(2)
+1 B(2_Isfahan)
<= 0

c_u_transportation_limit_t(Main_Tehran)_:
-20 h(Main)
+1 B(Main_Tehran)
<= 0

c_u_transportation_limit_t(Main_Isfahan)_:
-20 h(Main)
+1 B(Main_Isfahan)
<= 0

c_u_transportation_limit_f(1_Tehran)_:
+10 h(1)
-1 B(1_Tehran)
<= 0

c_u_transportation_limit_f(1_Isfahan)_:
+10 h(1)
-1 B(1_Isfahan)
<= 0

c_u_transportation_limit_f(2_Tehran)_:
+5 h(2)
-1 B(2_Tehran)
<= 0

c_u_transportation_limit_f(2_Isfahan)_:
+5 h(2)
-1 B(2_Isfahan)
<= 0

c_u_transportation_limit_f(Main_Tehran)_:
+5 h(Main)
-1 B(Main_Tehran)
<= 0

c_u_transportation_limit_f(Main_Isfahan)_:
+5 h(Main)
-1 B(Main_Isfahan)
<= 0

r_l_transportation_limit2(Tehran)_:
+1 B(1_Tehran)
+1 B(2_Tehran)
+1 B(Main_Tehran)
>= 20.0

r_u_transportation_limit2(Tehran)_:
+1 B(1_Tehran)
+1 B(2_Tehran)
+1 B(Main_Tehran)
<= 65

r_l_transportation_limit2(Isfahan)_:
+1 B(1_Isfahan)
+1 B(2_Isfahan)
+1 B(Main_Isfahan)
>= 30.0

r_u_transportation_limit2(Isfahan)_:
+1 B(1_Isfahan)
+1 B(2_Isfahan)
+1 B(Main_Isfahan)
<= 70

c_u_transp_from_dep_to_market_limit(A_Tehran)_:
+1 g(A_Tehran_Mashhad)
+1 g(A_Tehran_Kerman)
+1 g(A_Tehran_Ahvaz)
+1 g(A_Tehran_Tabriz)
-1 t(A_1_Tehran)
-1 t(A_2_Tehran)
-1 t(A_Main_Tehran)
<= 0

c_u_transp_from_dep_to_market_limit(A_Isfahan)_:
+1 g(A_Isfahan_Mashhad)
+1 g(A_Isfahan_Kerman)
+1 g(A_Isfahan_Ahvaz)
+1 g(A_Isfahan_Tabriz)
-1 t(A_1_Isfahan)
-1 t(A_2_Isfahan)
-1 t(A_Main_Isfahan)
<= 0

c_u_transp_from_dep_to_market_limit(B_Tehran)_:
+1 g(B_Tehran_Mashhad)
+1 g(B_Tehran_Kerman)
+1 g(B_Tehran_Ahvaz)
+1 g(B_Tehran_Tabriz)
-1 t(B_1_Tehran)
-1 t(B_2_Tehran)
-1 t(B_Main_Tehran)
<= 0

c_u_transp_from_dep_to_market_limit(B_Isfahan)_:
+1 g(B_Isfahan_Mashhad)
+1 g(B_Isfahan_Kerman)
+1 g(B_Isfahan_Ahvaz)
+1 g(B_Isfahan_Tabriz)
-1 t(B_1_Isfahan)
-1 t(B_2_Isfahan)
-1 t(B_Main_Isfahan)
<= 0

c_u_container_limit2(Tehran_Mashhad)_:
+1 g(A_Tehran_Mashhad)
+1 g(B_Tehran_Mashhad)
-100 G(Tehran_Mashhad)
<= 0

c_u_container_limit2(Tehran_Kerman)_:
+1 g(A_Tehran_Kerman)
+1 g(B_Tehran_Kerman)
-100 G(Tehran_Kerman)
<= 0

c_u_container_limit2(Tehran_Ahvaz)_:
+1 g(A_Tehran_Ahvaz)
+1 g(B_Tehran_Ahvaz)
-100 G(Tehran_Ahvaz)
<= 0

c_u_container_limit2(Tehran_Tabriz)_:
+1 g(A_Tehran_Tabriz)
+1 g(B_Tehran_Tabriz)
-100 G(Tehran_Tabriz)
<= 0

c_u_container_limit2(Isfahan_Mashhad)_:
+1 g(A_Isfahan_Mashhad)
+1 g(B_Isfahan_Mashhad)
-100 G(Isfahan_Mashhad)
<= 0

c_u_container_limit2(Isfahan_Kerman)_:
+1 g(A_Isfahan_Kerman)
+1 g(B_Isfahan_Kerman)
-100 G(Isfahan_Kerman)
<= 0

c_u_container_limit2(Isfahan_Ahvaz)_:
+1 g(A_Isfahan_Ahvaz)
+1 g(B_Isfahan_Ahvaz)
-100 G(Isfahan_Ahvaz)
<= 0

c_u_container_limit2(Isfahan_Tabriz)_:
+1 g(A_Isfahan_Tabriz)
+1 g(B_Isfahan_Tabriz)
-100 G(Isfahan_Tabriz)
<= 0

c_u_market_sell_limit_f(Tehran_Mashhad)_:
-1 G(Tehran_Mashhad)
+3 l(Tehran_Mashhad)
<= 0

c_u_market_sell_limit_f(Tehran_Kerman)_:
-1 G(Tehran_Kerman)
+6 l(Tehran_Kerman)
<= 0

c_u_market_sell_limit_f(Tehran_Ahvaz)_:
-1 G(Tehran_Ahvaz)
+10 l(Tehran_Ahvaz)
<= 0

c_u_market_sell_limit_f(Tehran_Tabriz)_:
-1 G(Tehran_Tabriz)
+5 l(Tehran_Tabriz)
<= 0

c_u_market_sell_limit_f(Isfahan_Mashhad)_:
-1 G(Isfahan_Mashhad)
+4 l(Isfahan_Mashhad)
<= 0

c_u_market_sell_limit_f(Isfahan_Kerman)_:
-1 G(Isfahan_Kerman)
+5 l(Isfahan_Kerman)
<= 0

c_u_market_sell_limit_f(Isfahan_Ahvaz)_:
-1 G(Isfahan_Ahvaz)
+5 l(Isfahan_Ahvaz)
<= 0

c_u_market_sell_limit_f(Isfahan_Tabriz)_:
-1 G(Isfahan_Tabriz)
+10 l(Isfahan_Tabriz)
<= 0

c_u_market_sell_limit_t(Tehran_Mashhad)_:
+1 G(Tehran_Mashhad)
-3 l(Tehran_Mashhad)
<= 0

c_u_market_sell_limit_t(Tehran_Kerman)_:
+1 G(Tehran_Kerman)
-6 l(Tehran_Kerman)
<= 0

c_u_market_sell_limit_t(Tehran_Ahvaz)_:
+1 G(Tehran_Ahvaz)
-10 l(Tehran_Ahvaz)
<= 0

c_u_market_sell_limit_t(Tehran_Tabriz)_:
+1 G(Tehran_Tabriz)
-5 l(Tehran_Tabriz)
<= 0

c_u_market_sell_limit_t(Isfahan_Mashhad)_:
+1 G(Isfahan_Mashhad)
-4 l(Isfahan_Mashhad)
<= 0

c_u_market_sell_limit_t(Isfahan_Kerman)_:
+1 G(Isfahan_Kerman)
-5 l(Isfahan_Kerman)
<= 0

c_u_market_sell_limit_t(Isfahan_Ahvaz)_:
+1 G(Isfahan_Ahvaz)
-5 l(Isfahan_Ahvaz)
<= 0

c_u_market_sell_limit_t(Isfahan_Tabriz)_:
+1 G(Isfahan_Tabriz)
-10 l(Isfahan_Tabriz)
<= 0

c_u_max_market_demand_limit(Mashhad_A)_:
+1 g(A_Tehran_Mashhad)
+1 g(A_Isfahan_Mashhad)
<= 600

c_u_max_market_demand_limit(Mashhad_B)_:
+1 g(B_Tehran_Mashhad)
+1 g(B_Isfahan_Mashhad)
<= 400

c_u_max_market_demand_limit(Kerman_A)_:
+1 g(A_Tehran_Kerman)
+1 g(A_Isfahan_Kerman)
<= 800

c_u_max_market_demand_limit(Kerman_B)_:
+1 g(B_Tehran_Kerman)
+1 g(B_Isfahan_Kerman)
<= 1200

c_u_max_market_demand_limit(Ahvaz_A)_:
+1 g(A_Tehran_Ahvaz)
+1 g(A_Isfahan_Ahvaz)
<= 1500

c_u_max_market_demand_limit(Ahvaz_B)_:
+1 g(B_Tehran_Ahvaz)
+1 g(B_Isfahan_Ahvaz)
<= 1500

c_u_max_market_demand_limit(Tabriz_A)_:
+1 g(A_Tehran_Tabriz)
+1 g(A_Isfahan_Tabriz)
<= 1400

c_u_max_market_demand_limit(Tabriz_B)_:
+1 g(B_Tehran_Tabriz)
+1 g(B_Isfahan_Tabriz)
<= 1100

bounds
   0 <= g(A_Tehran_Mashhad) <= +inf
   0 <= g(A_Tehran_Kerman) <= +inf
   0 <= g(A_Tehran_Ahvaz) <= +inf
   0 <= g(A_Tehran_Tabriz) <= +inf
   0 <= g(A_Isfahan_Mashhad) <= +inf
   0 <= g(A_Isfahan_Kerman) <= +inf
   0 <= g(A_Isfahan_Ahvaz) <= +inf
   0 <= g(A_Isfahan_Tabriz) <= +inf
   0 <= g(B_Tehran_Mashhad) <= +inf
   0 <= g(B_Tehran_Kerman) <= +inf
   0 <= g(B_Tehran_Ahvaz) <= +inf
   0 <= g(B_Tehran_Tabriz) <= +inf
   0 <= g(B_Isfahan_Mashhad) <= +inf
   0 <= g(B_Isfahan_Kerman) <= +inf
   0 <= g(B_Isfahan_Ahvaz) <= +inf
   0 <= g(B_Isfahan_Tabriz) <= +inf
   0 <= Extracted_ore(1) <= +inf
   0 <= Extracted_ore(2) <= +inf
   0 <= Extracted_ore(3) <= +inf
   0 <= t(A_1_Tehran) <= +inf
   0 <= t(A_1_Isfahan) <= +inf
   0 <= t(A_2_Tehran) <= +inf
   0 <= t(A_2_Isfahan) <= +inf
   0 <= t(A_Main_Tehran) <= +inf
   0 <= t(A_Main_Isfahan) <= +inf
   0 <= t(B_1_Tehran) <= +inf
   0 <= t(B_1_Isfahan) <= +inf
   0 <= t(B_2_Tehran) <= +inf
   0 <= t(B_2_Isfahan) <= +inf
   0 <= t(B_Main_Tehran) <= +inf
   0 <= t(B_Main_Isfahan) <= +inf
   0 <= h(1) <= 1
   0 <= h(2) <= 1
   0 <= h(Main) <= 1
   0 <= B(1_Tehran) <= +inf
   0 <= B(1_Isfahan) <= +inf
   0 <= B(2_Tehran) <= +inf
   0 <= B(2_Isfahan) <= +inf
   0 <= B(Main_Tehran) <= +inf
   0 <= B(Main_Isfahan) <= +inf
   0 <= G(Tehran_Mashhad) <= +inf
   0 <= G(Tehran_Kerman) <= +inf
   0 <= G(Tehran_Ahvaz) <= +inf
   0 <= G(Tehran_Tabriz) <= +inf
   0 <= G(Isfahan_Mashhad) <= +inf
   0 <= G(Isfahan_Kerman) <= +inf
   0 <= G(Isfahan_Ahvaz) <= +inf
   0 <= G(Isfahan_Tabriz) <= +inf
   0 <= U(A) <= +inf
   0 <= U(B) <= +inf
   0 <= Z(1_A) <= +inf
   0 <= Z(1_B) <= +inf
   0 <= Z(2_A) <= +inf
   0 <= Z(2_B) <= +inf
   0 <= Z(3_A) <= +inf
   0 <= Z(3_B) <= +inf
   0 <= C(1_A) <= +inf
   0 <= C(1_B) <= +inf
   0 <= C(2_A) <= +inf
   0 <= C(2_B) <= +inf
   0 <= C(3_A) <= +inf
   0 <= C(3_B) <= +inf
   0 <= A(1_A) <= +inf
   0 <= A(1_B) <= +inf
   0 <= A(2_A) <= +inf
   0 <= A(2_B) <= +inf
   0 <= A(3_A) <= +inf
   0 <= A(3_B) <= +inf
   0 <= F(1_A) <= +inf
   0 <= F(1_B) <= +inf
   0 <= F(2_A) <= +inf
   0 <= F(2_B) <= +inf
   0 <= F(3_A) <= +inf
   0 <= F(3_B) <= +inf
   0 <= l(Tehran_Mashhad) <= 1
   0 <= l(Tehran_Kerman) <= 1
   0 <= l(Tehran_Ahvaz) <= 1
   0 <= l(Tehran_Tabriz) <= 1
   0 <= l(Isfahan_Mashhad) <= 1
   0 <= l(Isfahan_Kerman) <= 1
   0 <= l(Isfahan_Ahvaz) <= 1
   0 <= l(Isfahan_Tabriz) <= 1
general
  B(1_Tehran)
  B(1_Isfahan)
  B(2_Tehran)
  B(2_Isfahan)
  B(Main_Tehran)
  B(Main_Isfahan)
  G(Tehran_Mashhad)
  G(Tehran_Kerman)
  G(Tehran_Ahvaz)
  G(Tehran_Tabriz)
  G(Isfahan_Mashhad)
  G(Isfahan_Kerman)
  G(Isfahan_Ahvaz)
  G(Isfahan_Tabriz)
binary
  h(1)
  h(2)
  h(Main)
  l(Tehran_Mashhad)
  l(Tehran_Kerman)
  l(Tehran_Ahvaz)
  l(Tehran_Tabriz)
  l(Isfahan_Mashhad)
  l(Isfahan_Kerman)
  l(Isfahan_Ahvaz)
  l(Isfahan_Tabriz)
end
