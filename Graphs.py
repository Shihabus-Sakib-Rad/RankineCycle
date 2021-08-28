from Cycle import Cycle
import matplotlib.pyplot as plt
import numpy as np
import os
from WaterState import timing


@timing
def generate_graphs(T5, P5, T8, x8):
    eff_v_boiler_p_loss(T5, P5, T8, x8)
    eff_v_pipe_p_loss(T5, P5, T8, x8)
    eff_v_cond_p_loss(T5, P5, T8, x8)
    eff_v_subcooling(T5, P5, T8, x8)
    eff_v_q_loss(T5, P5, T8, x8)
    eff_v_pump_eff(T5, P5, T8, x8)
    eff_v_turbine_eff(T5, P5, T8, x8)


def eff_v_boiler_p_loss(T5, P5, T8, x8):
    losses: list[float] = []
    effs: list[float] = []
    dx: float = 0.1e6
    for boiler_p_loss in np.arange(0.0e6, 2e6, dx):
        c: Cycle = Cycle(T5, P5, T8, x8, boiler_p_loss=boiler_p_loss)
        losses.append(boiler_p_loss / 1e6)
        effs.append(c.eff * 100)

    plot_graph(losses, effs, "Boiler Pressure Loss (MPa)", "Efficiency %")


def eff_v_pipe_p_loss(T5, P5, T8, x8):
    losses: list[float] = []
    effs: list[float] = []
    dx: float = 0.1e6
    for pipe_p_loss in np.arange(0.0e6, 2e6, dx):
        c: Cycle = Cycle(T5, P5, T8, x8, pipe_p_loss=pipe_p_loss)
        losses.append(pipe_p_loss / 1e6)
        effs.append(c.eff * 100)

    plot_graph(losses, effs, "Pipe Pressure Loss (MPa)", "Efficiency %")


def eff_v_cond_p_loss(T5, P5, T8, x8):
    losses: list[float] = []
    effs: list[float] = []
    dx: float = 0.5e3
    for cond_p_loss in np.arange(0.0e3, 2e3, dx):
        c: Cycle = Cycle(T5, P5, T8, x8, cond_p_loss=cond_p_loss)
        losses.append(cond_p_loss * 1e-3)
        effs.append(c.eff * 100)

    plot_graph(losses, effs, "Condenser Pressure Loss (kPa)", "Efficiency %")


def eff_v_subcooling(T5, P5, T8, x8):
    temps: list[float] = []
    effs: list[float] = []
    dx: float = 1.0
    for temp in np.arange(0.0, 10, dx):
        c: Cycle = Cycle(T5, P5, T8, x8, subcooling=temp)
        temps.append(temp)
        effs.append(c.eff * 100)

    plot_graph(temps, effs, "Subcooling (K)", "Efficiency %")


def eff_v_q_loss(T5, P5, T8, x8):
    losses: list[float] = []
    effs: list[float] = []
    dx: float = 10e3
    for loss in np.arange(0e3, 150e3, dx):
        c: Cycle = Cycle(T5, P5, T8, x8, pipe_q_loss=loss)
        losses.append(loss * 1e-3)
        effs.append(c.eff * 100)

    plot_graph(losses, effs, "Heat loss (KJ per kg)", "Efficiency %")


def eff_v_turbine_eff(T5, P5, T8, x8):
    tur_effs: list[float] = []
    effs: list[float] = []
    dx: float = 0.01
    for tur_eff in np.arange(1.0, 0.9, -dx):
        c: Cycle = Cycle(T5, P5, T8, x8, eff_turbine=tur_eff)
        tur_effs.append(tur_eff * 100)
        effs.append(c.eff * 100)

    plot_graph(tur_effs, effs, "Turbine Efficiency %", "Cycle Efficiency %")


def eff_v_pump_eff(T5, P5, T8, x8):
    pump_effs: list[float] = []
    effs: list[float] = []
    dx: float = 0.01
    for pump_eff in np.arange(1.0, 0.9, -dx):
        c: Cycle = Cycle(T5, P5, T8, x8, eff_pump=pump_eff)
        pump_effs.append(pump_eff * 100)
        effs.append(c.eff * 100)

    plot_graph(pump_effs, effs, "Pump Efficiency %", "Cycle Efficiency %")


def plot_graph(x: list[float], y: list[float], x_label: str, y_label: str):
    graph_dir_name = "Graphs"
    if not os.path.exists(graph_dir_name):
        os.makedirs(graph_dir_name)
    plt.clf()
    plt.cla()
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    fname: str = x_label + " vs " + y_label
    fpath: str = os.path.join(graph_dir_name, fname)
    plt.savefig(fpath)
    print(fpath)
