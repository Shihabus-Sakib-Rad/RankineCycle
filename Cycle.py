from CoolProp.CoolProp import PropsSI
from WaterState import State, timing


# @timing
def ideal(T5, P5, T8, x8):
    T5 = T5
    P5 = P5
    s5 = PropsSI('S', 'P', P5, 'T', T5, 'Water')
    h5 = PropsSI('H', 'P', P5, 'T', T5, 'Water')

    x8 = x8
    T8 = T8
    P8 = PropsSI('P', 'T', T8, 'Q', x8, 'Water')
    s8 = PropsSI('S', 'T', T8, 'Q', x8, 'Water')
    h8 = PropsSI('H', 'T', T8, 'Q', x8, 'Water')

    T7 = T5
    s7 = s8
    P7 = PropsSI('P', 'T', T7, 'S', s7, 'Water')
    h7 = PropsSI('H', 'T', T7, 'S', s7, 'Water')

    P6 = P7
    s6 = s5
    h6 = PropsSI('H', 'P', P6, 'S', s6, 'Water')

    P1 = P8
    x1 = 0
    s1 = PropsSI('S', 'P', P1, 'Q', x1, 'Water')
    h1 = PropsSI('H', 'P', P1, 'Q', x1, 'Water')

    P2 = P6
    s2 = s1
    h2 = PropsSI('H', 'P', P2, 'S', s2, 'Water')

    P3 = P2
    x3 = 0
    h3 = PropsSI('H', 'P', P3, 'Q', x3, 'Water')
    s3 = PropsSI('S', 'P', P3, 'Q', x3, 'Water')

    P4 = P5
    s4 = s3
    h4 = PropsSI('H', 'P', P4, 'S', s4, 'Water')

    y = (h3 - h2) / (h6 - h2)

    q = h5 - h4 + (1 - y) * (h7 - h6)
    wt = h5 - h6 + (1 - y) * (h7 - h8)
    wp = (1 - y) * (h2 - h1) + h4 - h3
    w_net = wt - wp

    eff = w_net / q * 100
    return eff, w_net, q, y, P6


class Cycle:
    # @timing
    def __init__(self, T5, P5, T8, x8, eff_turbine: float = 1.0, eff_pump: float = 1.0, subcooling: float = 0.0,
                 boiler_p_loss: float = 0.0, pipe_p_loss: float = 0.0, pipe_q_loss: float = 0.0,
                 cond_p_loss: float = 0.0, reheater_p_loss: float = 0.0):
        st5 = State(T=T5, P=P5)
        st8 = State(T=T8, x=x8)

        st7 = State(T=T5, s=st8.s)
        st7 = State(T=T5, h=eff_turbine * (st7.h - st8.h) + st8.h)

        p_loss_67 = pipe_p_loss + reheater_p_loss
        st6 = State(P=st7.P + p_loss_67, s=st5.s)
        st6 = State(P=st6.P, h=st5.h - eff_turbine * (st5.h - st6.h))

        st1 = State(P=st8.P - cond_p_loss, x=0)
        st3 = State(P=st6.P, x=0)

        # the condition check is required to avoid a bug. the result may be from saturated vapor instead of sat liquid
        if subcooling != 0.0:
            st1 = State(P=st1.P, T=st1.T - subcooling)
            st3 = State(P=st3.P, T=st3.T - subcooling)

        st2 = State(P=st6.P, s=st1.s)
        st2 = State(P=st2.P, h=(st2.h - st1.h) / eff_pump + st1.h)

        p_loss_45 = boiler_p_loss + pipe_p_loss
        st4 = State(P=st5.P + p_loss_45, s=st3.s)
        st4 = State(P=st4.P, h=(st4.h - st3.h) / eff_pump + st3.h)

        y = (st3.h - st2.h) / (st6.h - st2.h)

        q_45 = st5.h - st4.h + pipe_q_loss
        q_67 = (1 - y) * (st7.h - st6.h + pipe_q_loss)

        q_inp = q_45 + q_67

        w_56 = st5.h - st6.h
        w_78 = (1 - y) * (st7.h - st8.h)

        w_t = w_78 + w_56

        w_12 = (1 - y) * (st2.h - st1.h)
        w_34 = st4.h - st3.h

        w_p = w_12 + w_34

        w_net = w_t - w_p

        eff = w_net / q_inp

        q_81 = (1 - y) * (st8.h - st1.h)

        self.eff = eff
        self.w_net = w_net
        self.w_p = w_p
        self.w_34 = w_34
        self.w_12 = w_12
        self.w_t = w_t
        self.w_78 = w_78
        self.w_56 = w_56
        self.q_inp = q_inp
        self.q_67 = q_67
        self.q_45 = q_45

        self.w_net_KJ = round(w_net / 1000, 2)
        self.w_p_KJ = round(w_p / 1000, 2)
        self.w_34_KJ = round(w_34 / 1000, 2)
        self.w_12_KJ = round(w_12 / 1000, 2)
        self.w_t_KJ = round(w_t / 1000, 2)
        self.w_78_KJ = round(w_78 / 1000, 2)
        self.w_56_KJ = round(w_56 / 1000, 2)
        self.q_inp_KJ = round(q_inp / 1000, 2)
        self.q_67_KJ = round(q_67 / 1000, 2)
        self.q_45_KJ = round(q_45 / 1000, 2)
        self.q_81_KJ = round(q_81 / 1000, 2)

        self.y = y
        self.st1 = st1
        self.st2 = st2
        self.st3 = st3
        self.st4 = st4
        self.st5 = st5
        self.st6 = st6
        self.st7 = st7
        self.st8 = st8
