# Rankine Cycle
modelling of Reheat Rankine single satge regeneration cycle

Usage:

```python
from Cycle import ideal, Cycle
from Graphs import generate_graphs

"""Run the line below in Ipython console. And access attributes of the object. All values are in SI"""
actual_cycle = Cycle(T_max, P_max, T_cond, quality, eff_turbine=0.95, eff_pump=0.9, boiler_p_loss=0.7e6,
                     subcooling=5, cond_p_loss=1e3, pipe_p_loss=0.5e6, pipe_q_loss=100e3, reheater_p_loss=0.3e6)
   
print("Actual cycle Efficiency ", actual_cycle.eff)
print("Actual cycle Heat Input", actual_cycle.q_inp_KJ, " kJ/kg ")
    
""" generating graph may take long time. The graphs will be saved to Graphs folder on script directory"""
generate_graphs(T_max, P_max, T_cond, quality)
```
