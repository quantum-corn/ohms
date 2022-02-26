# %% md
# # Ohm's Law
# ## Let's draw the circuit first
# For that I will use schemdraw
# ### v1.0

# %% Draw
import schemdraw
schemdraw.use('svg')
elm=schemdraw.elements
d=schemdraw.Drawing(file='ohms_ckt.svg')
d+=elm.Battery().reverse().up().label(('-','V','+'))
d+=elm.MeterI().right()
d+=(R:=elm.Resistor()).down().label(('+','R','-'))
d+=elm.Line().left()
d+=elm.Ground().drop(R.start)
d+=elm.Line(unit=1).right()
d+=elm.Dot()
d+=elm.MeterV().down()
d+=elm.Dot()
d+=elm.Line(unit=1).left()
d.draw()

# %% md
# ## Now the simulation
# For this I will use PySpice

# %% import
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# %% setup
logger = Logging.setup_logging()

# %% circuit
def ckt(r):
    circuit = Circuit("Ohm's Law")
    circuit.V('', 1, circuit.gnd, 10@u_V)
    circuit.R('', 1, circuit.gnd, r@u_Ohm)
    return circuit

# %% simulate
def simulate(circuit):
    simulator = circuit.simulator()
    analysis = simulator.dc(V=slice(0, 50, 1))
    return analysis

# %% md
# ### Now let's plot the data
# For this I will use matplotlib

# %% import
import matplotlib.pyplot as plt

# %% plot data
fig, ax=plt.subplots()
ax.set(title="Ohm's Law", xlabel='Voltage in V', ylabel='Current in A', xlim=(0,50), ylim=(0,5))
ax.grid()
for r in (l:=[10, 20, 40]):
    out=simulate(ckt(r))
    ax.plot(out['v-sweep'], -out.branches['v'])
ax.legend(['R = {} Ohm'.format(r) for r in l])
plt.show()
plt.savefig('ohms_plt.svg')
