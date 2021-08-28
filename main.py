from Cycle import ideal, Cycle
from Graphs import generate_graphs


def main():
    T_max = 855
    P_max = 19e6

    T_surr = 303
    dT_cond = 10
    T_cond = T_surr + dT_cond
    quality = 0.89

    """Run these teo line below in Ipython console. And access attributes of the objects. All values are in SI"""
    actual_cycle = Cycle(T_max, P_max, T_cond, quality, eff_turbine=0.95, eff_pump=0.9, boiler_p_loss=0.7e6,
                         subcooling=5, cond_p_loss=1e3, pipe_p_loss=0.5e6, pipe_q_loss=100e3, reheater_p_loss=0.3e6)
    ideal_cycle = Cycle(T_max, P_max, T_cond, quality)
    print("Actual cycle Efficiency ", actual_cycle.eff)
    print("Actual cycle Heat Input", actual_cycle.q_inp_KJ, " kJ/kg ")
    print("Ideal cycle Efficiency ", ideal_cycle.eff)
    print("Ideal cycle Heat Input", ideal_cycle.q_inp_KJ, " kJ/kg ")
    """This way you can access all other information of the cycle"""

    """ generating graph may take long time. The graphs will be saved to Graphs folder on script directory"""
    generate_graphs(T_max, P_max, T_cond, quality)

    """IF you don't have refprop library installed, comment out above three lines. You can only use the ideal 
    function """
    eff, w_net, q, y, P6 = ideal(T_max, P_max, T_cond, quality)
    print(f'Efficiency {eff:.4f}')


if __name__ == '__main__':
    main()
