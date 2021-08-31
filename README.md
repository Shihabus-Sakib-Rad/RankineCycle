# Rankine Cycle
Modelling of Reheat regenerative Rankine cycle.

The code was written to complete a project from Applied Thermodynamics Course. The project report is also included with some modifications. 

![Cycle](ts%20ideal.png)

"You need to have REFPROP Library installed on your computer. Modify the State.py to point to REFPROP library"
>> CoolProp.set_config_string(CoolProp.ALTERNATIVE_REFPROP_PATH, "C:\\Program Files (x86)\\REFPROP")

Usage:

```python
from Cycle import ideal, Cycle

# All input in SI unit
T_max = 855
P_max = 19e6
T_cond = 313
quality = 0.89



"""Run the line below in Ipython console. And access attributes of the object. All values are in SI"""
actual_cycle = Cycle(T_max, P_max, T_cond, quality, eff_turbine=0.95, eff_pump=0.9, boiler_p_loss=0.7e6,
                     subcooling=5, cond_p_loss=1e3, pipe_p_loss=0.5e6, pipe_q_loss=100e3, reheater_p_loss=0.3e6)
ideal_cycle = Cycle(T_max, P_max, T_cond, quality)


print("Actual cycle Efficiency ", actual_cycle.eff)
print("Actual cycle Heat Input", actual_cycle.q_inp_KJ, " kJ/kg ")
print("Ideal cycle Efficiency ", ideal_cycle.eff)
print("Ideal cycle Heat Input", ideal_cycle.q_inp_KJ, " kJ/kg ")
"""This way you can access all other information of the cycle"""
    

"""IF you don't have refprop library installed, comment out above lines. You can only use the ideal 
    function. Modify ideal function to return any values you want """
eff, w_net, q, y, P6 = ideal(T_max, P_max, T_cond, quality)
print(f'Efficiency {eff:.4f}')

"""You Can also use State class to create any cycle."""
from State import State
# Default fluid is Water.
st5 = State(T=T_max, P=P_max)
st8 = State(T=T_cond, x=quality)

# Specify other fluid
st1 = State(T=T_max, P=P_max, fluid="Air")

# Access values of properties inSI unit with dot
print(st5.T, st5.P, st5.s, st5.h, st5.x) 

"""Graphs.py was used to generate some graphs related to my project. Generating graph may take some time.
    The graphs will be saved to Graphs folder on script directory"""
from Graphs import generate_graphs
generate_graphs(T_max, P_max, T_cond, quality)
```
