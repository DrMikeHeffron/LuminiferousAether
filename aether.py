#===============================================================================
# Refer to https://pint.readthedocs.io/en/stable/ for comprehensive
# documentation for the "pint" unit package.
#
# Install as follows, if not already present in your version of Linux.
# sudo apt-get install python3-pint
#
# This python program was developed by Dr Michael Heffron to compare
# fundamental constants of physics derived from the aether to their
# values published as CODATA 2022.
#===============================================================================

import math
from pint import UnitRegistry

# Create a unit registry
u = UnitRegistry()
Q = u.Quantity

# Define basic aether properties.
c2k = 'convert cgs to kms'
r_λ = 'Compton wavelength'
ρ   = 'aether density'
P   = 'aether pressure'
c   = 'speed of light'
S   = 'shape of ellipsoid'

# Define fundamental luminiferous aether values.
aether = {}
aether[c2k] = Q(1.000000000000000e+07, 'C**2/kg/m')
aether[r_λ] = Q(2.426310235380000e-12, 'm')
aether[ρ]   = Q(1.784488701747213e+16, 'kg/m**3')
aether[P]   = Q(1.603818462092648e+33, 'kg/m/s**2')
aether[c]   = (aether[P] / aether[ρ])**0.5
aether[S]   = 4.0 * math.pi / 3.0

class Dab:
    """Just a little dab of matter, whatever that may be!"""
    def __init__(self, mass: u.Quantity, name:str):
        # Name of this little dab of matter.
        self.name = name
        # Mass contained within the luminiferous radius.
        self.mass = mass
        # Eq 6-3 of "The Luminiferous Aether: primary substance of the universe"
        self.radius = (self.mass / (aether[S] * aether[ρ]))**(1.0/3.0)
        # Resistance of this dab of matter to aether flow.
        self.kinematicViscosity = self.radius * aether[c]
        # Gravitation produced by the kinematic viscosity of this dab of matter.
        self.gravitationalParameter = self.kinematicViscosity * aether[c]
        # Eq 4-3 of "The Luminiferous Aether: primary substance of the universe"
        self.surfaceTension = aether[P] * self.radius

def g2m(gravParm):
    """Determine mass of object from its gravitational parameter."""
    # Eq 4-1 of "The Luminiferous Aether: primary substance of the universe"
    radius = gravParm / aether[c]**2
    # Eq 3-3 of "The Luminiferous Aether: primary substance of the universe"
    return aether[ρ] * aether[S] * radius**3

# ANSII color codes.
LIGHT_BLUE   = '\033[1;34m'
LIGHT_CYAN   = '\033[1;36m'
LIGHT_GREEN  = '\033[1;32m'
LIGHT_PURPLE = '\033[1;35m'
LIGHT_RED    = '\033[1;31m'
LIGHT_WHITE  = '\033[1;37m'
LIGHT_YELLOW = '\033[1;33m'

def indent(name, parm, value):
    if name == '':
        color = LIGHT_CYAN
    else:
        color = LIGHT_WHITE
    legend = '{}{} {}'.format(color, name, parm)
    print('{:>39} = {:.15E~P}'.format(legend, value))
    
def showDab(dab):
    """Show important characteristics of matter."""
    print()
    indent(dab.name, 'gravitational parameter', dab.gravitationalParameter)
    indent(dab.name, 'kinematic viscosity', dab.kinematicViscosity)
    indent(dab.name, 'mass', dab.mass)
    indent(dab.name, 'radius', dab.radius)
    indent(dab.name, 'surface tension', dab.surfaceTension)

# Define fundamental constants of physics.
α =   'fine structure constant'
a_0 = 'Bohr radius'
afu = 'atomic unit of force'
μ_B = 'Bohr magneton'
ε_0 = 'electric constant'
E_h = 'Hartree energy'
G   = 'gravitational constant'
h =   'Planck constant'
K_J = 'Josephson constant'
μ_0 = 'magnetic constant'
Φ_0 = 'magnetic flux quantum'
q =   'elementary charge'
x2q = 'quantum of circulation X 2'
R_8 = 'Rydberg constant'
R_K = 'von Klitzing constant'
Z_0 = 'vacuum impedance'

# CODATA 2022 values, omitting (uncertainty).
nist = {}
nist[afu] = Q(8.2387235038e-8, 'N')       # N = kg*m/s**2
nist[μ_B] = Q(9.2740100657e-24, 'J/T')    # J/T = C*m**2/s
nist[a_0] = Q(5.29177210544e-11, 'm')
nist[ε_0] = Q(8.8541878188e-12, 'F/m')    # F/m = C**2*s**2/kg/m**3
nist[q]   = Q(1.602176634e-19,  'C')
nist[α]   = Q(7.2973525643e-3)
nist[E_h] = Q(4.3597447222060e-18, 'J')   # J = kg*m**2/s**2
nist[G]   = Q(6.67430e-11, 'm**3/s**2*kg')
nist[K_J] = Q(483597.8484e9, 'Hz/V')      # Hz/V = C*s/kg/m**2
nist[μ_0] = Q(1.25663706127e-6, 'N/A**2') # N/A**2 = kg*m/C**2
nist[Φ_0] = Q(2.067833848e-15, 'Wb')      # Wb = kg*m**2/C/s
nist[h]   = Q(6.62607015e-34, 'J/Hz')     # J/Hz = kg*m**2/s
nist[x2q] = Q(7.2738950934e-4, 'm**2/s')
nist[R_8] = Q(10973731.568157, '1/m')
nist[R_K] = Q(25812.80745, 'ohm')         # ohm = kg·m**2/C**2·s
nist[Z_0] = Q(376.730313412, 'ohm')       # ohm = kg·m**2/C**2·s

digits = ['.','0','1','2','3','4','5','6','7','8','9']
def matchTo(str1, str2, rat):
    """Find the first index where two strings differ."""
    for i in range(min(len(str1), len(str2))):
        if (str1[i] != str2[i]) or (str1[i] not in digits) or (str2[i] not in digits):
            # Count first non-match if it rounds up or down.
            if (rat[i] == '0') or (rat[i] == '9'):
                return i
            else: # Deduct for decimal point.
                return i - 1
    # Match to shorter length if no difference.
    return min(len(str1), len(str2)) - 1
    
def compare(name):
    """Compare an aether value to a NIST value."""
    ratio = aether[name] / nist[name]
    if ratio.dimensionless:
        aval = '{:.15E~P}'.format(aether[name])
        nval = '{:.15E~P}'.format(nist[name])
        rat  = '{:.15E~P}'.format(ratio)
        n = matchTo(aval, nval, rat)
        # Deduct for leading digit.
        value = '{:.' + str(n-1) + 'E~P}'
        val = value.format(aether[name])
        # Replace all divison symbols except first with bullet operator.
        val = val.replace('/','!',1)
        val = val.replace('/','·')
        val = val.replace('!','/')
        # Format output for display.
        match = '{}{:>26} : {:<27} ({} digits match)'
        if 0.999999999 <= ratio <= 1.0000000005:
            color = LIGHT_GREEN
        else:
            color = LIGHT_YELLOW
        print(match.format(color, name, val, n))
    # Problem with mismatched units of measure.
    else:
        print('{}{} : {:.9E~P} (UNITS MISMATCH)'.format(LIGHT_RED, name, aether[name]))

def compareDerivation(name, variant, calc):
    compare(name)
    aether[calc] = aether[name]
    nist[calc] = variant
    compare(calc)
    
# Define dabs of matter. Similar in concept to a black hole, but different!
Earth    = Dab(g2m(Q(3.98600441800000e+14, 'm**3/s**2')), 'Earth')
electron = Dab(Q(9.10938371390000e-31, 'kg'), 'electron')
light    = Dab(aether[r_λ]**3 * aether[S] * aether[ρ], 'light')
muon     = Dab(Q(1.88353162700000e-28, 'kg'), 'muon')
proton   = Dab(Q(1.67262192595000e-27, 'kg'), 'proton')
sun      = Dab(g2m(Q(1.32712440018000e20, 'm**3/s**2')), 'sun')
# Approximate Newtonian mass of the sun (not its luminiferous mass!!!)
# intentionally restricted to 6 digits accuracy of NIST value for G.
sunMass  = sun.gravitationalParameter / (0.9999995 * nist[G])

# Calculate fundamental constant values from the aether.
aether[q]   = (aether[c2k] * electron.mass * proton.radius)**0.5
aether[ε_0] = aether[q]**2 * aether[ρ] / (4.0 * math.pi * aether[P] * electron.mass * proton.radius)
aether[μ_0] = 4.0 * math.pi * electron.mass * proton.radius / aether[q]**2
aether[G]   = sun.gravitationalParameter / sunMass
aether[h]   = light.kinematicViscosity * electron.mass
aether[R_K] = aether[h] / aether[q]**2
aether[μ_B] = light.kinematicViscosity * aether[q] / (4.0 * math.pi)
aether[a_0] = (light.radius / (2.0 * math.pi))**2 / proton.radius
aether[α]   = 2.0 * math.pi * proton.radius / light.radius
aether[E_h] = electron.mass * proton.gravitationalParameter / aether[a_0]
aether[afu] = electron.mass * proton.gravitationalParameter / aether[a_0]**2
aether[K_J] = 2.0 * aether[q] / aether[h]
aether[Φ_0] = aether[h] / (2.0 * aether[q])
aether[R_8] = proton.radius / (2.0 * aether[a_0] * light.radius)
aether[Z_0] = 4.0 * math.pi * electron.mass * proton.kinematicViscosity / aether[q]**2
aether[x2q] = light.kinematicViscosity

# Display fundamental aether values
indent('', 'aether density', aether[ρ])
indent('', 'aether pressure', aether[P])
indent('', 'speed of light', aether[c])

# Display important properties of well-known examples of matter.
showDab(Earth)
showDab(electron)
showDab(light)
showDab(muon)
showDab(proton)
showDab(sun)
print('           Newtonian mass of sun = {:.5E~P}'.format(sunMass))

print('{}\nCompare aether values to NIST values'.format(LIGHT_GREEN))
compare(afu)
compare(μ_B)
compare(a_0)
compare(ε_0)
compare(q)
compare(α)
compare(E_h)
print('{}NOTE: the following value is the extremely accurate gravitational parameter'.format(LIGHT_WHITE))
print('of the sun divided by its very inaccurate alleged Newtonian mass.')
compare(G)
compare(K_J)
compare(μ_0)
compareDerivation(Φ_0, nist[h] / (2.0 * nist[q]), 'h/2q')
compare(h)
print('{}NOTE: the following value is equivalent to the kinematic viscosity of light.'.format(LIGHT_WHITE))
compareDerivation(x2q, nist[h] / electron.mass, 'h/mₑ')
compare(R_8)
compare(R_K)
compare(Z_0)