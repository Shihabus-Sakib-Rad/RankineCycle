import time
from CoolProp import CoolProp, AbstractState
from itertools import combinations

CoolProp.set_config_string(CoolProp.ALTERNATIVE_REFPROP_PATH, "C:\\Program Files (x86)\\REFPROP")


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2 - time1) * 1000.0))

        return ret

    return wrap


def is_input_comb(inp1, inp2) -> bool:
    return inp1 is not None and inp2 is not None


def get_st(input_pair, inp1: float, inp2: float, fluid):
    refprop = 'REFPROP'
    heos = 'HEOS'
    # st = AbstractState(refprop, fluid)
    # st.update(input_pair, inp1, inp2)
    # are you sure that both backend uses same reference point?
    try:
        st = AbstractState(heos, fluid)
        st.update(input_pair, inp1, inp2)
    except ValueError as e:
        e_str = str(e)
        i = e_str.find("This pair of inputs")
        if i != -1:
            st = AbstractState(refprop, fluid)
            st.update(input_pair, inp1, inp2)
        else:
            raise Exception(e)
    return st


class State:
    def __init__(self, P: float = None, T: float = None, s: float = None, h: float = None, x: float = None,
                 fluid='Water'):
        props_dict = {'P': P,
                      'T': T,
                      's': s,
                      'h': h,
                      'x': x}

        st = None

        for comb in combinations(props_dict, 2):
            inp1_kw = comb[0]
            inp2_kw = comb[1]
            inp1 = props_dict[inp1_kw]
            inp2 = props_dict[inp2_kw]
            if is_input_comb(inp1, inp2):
                input_pair = get_combination(inp1_kw, inp2_kw)
                if inputs_order(inp1_kw, inp2_kw):
                    st = get_st(input_pair, inp1, inp2, fluid)
                else:
                    st = get_st(input_pair, inp2, inp1, fluid)
                break

        if st is None:
            raise Exception("Couldn't calculate")

        # round function to fix [Saturation pressure [7326.08 Pa] corresponding to T [313 K] is within 1e-4 % of
        # given p [7326.08 Pa]]
        self.P: float = round(st.p(), 1)
        self.T: float = round(st.T(), 3)
        self.s: float = st.smass()
        self.h: float = st.hmass()
        self.x: float = st.Q()


input_order: list[str] = ["ρ", "h", "P", "x", "s", "T", "u"]
cp_input_combinations: list[list] = [[{"T", "P"}, CoolProp.PT_INPUTS],
                                     [{"T", "ρ"}, CoolProp.DmassT_INPUTS],
                                     [{"T", "s"}, CoolProp.SmassT_INPUTS],
                                     [{"T", "h"}, CoolProp.HmassT_INPUTS],
                                     [{"T", "u"}, CoolProp.TUmass_INPUTS],
                                     [{"T", "x"}, CoolProp.QT_INPUTS],
                                     [{"P", "ρ"}, CoolProp.DmassP_INPUTS],
                                     [{"P", "s"}, CoolProp.PSmass_INPUTS],
                                     [{"P", "h"}, CoolProp.HmassP_INPUTS],
                                     [{"P", "u"}, CoolProp.PUmass_INPUTS],
                                     [{"P", "x"}, CoolProp.PQ_INPUTS],
                                     [{"ρ", "s"}, CoolProp.DmassSmass_INPUTS],
                                     [{"ρ", "h"}, CoolProp.DmassHmass_INPUTS],
                                     [{"ρ", "u"}, CoolProp.DmassUmass_INPUTS],
                                     [{"ρ", "x"}, CoolProp.DmassQ_INPUTS],
                                     [{"s", "h"}, CoolProp.HmassSmass_INPUTS],
                                     [{"s", "u"}, CoolProp.SmassUmass_INPUTS],
                                     [{"h", "x"}, CoolProp.HmassQ_INPUTS]]


def inputs_order(input_1: str, input_2: str) -> bool:
    if input_order.index(input_1) < input_order.index(input_2):
        return True
    else:
        return False


def get_combination(symbol_1: str, symbol_2: str):
    given: set = {symbol_1, symbol_2}

    for combination in cp_input_combinations:
        if given == combination[0]:
            return combination[1]

    raise Exception("This line should not get to be executed in get_combination")


if __name__ == '__main__':
    st1 = State(T=300, P=2e6)
    print(st1.T, st1.P, st1.h, st1.s, st1.x)
