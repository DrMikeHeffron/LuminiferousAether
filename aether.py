#===============================================================================
# aether.py revised 20260915
#
# This version replaced old references to coulomb (C) with equivalent
# ampere-seconds (As) for better alignment with NIST/CODATA use of
# MSKA measurement units.
#
# 20260911
# This version relocates NIST/CODATA declared and measured values, and then uses
# that data to implement my original method of finding the luminiferous radius
# of the proton from its gravitational parameter ϰₚ, calculated from the Hartree
# energy Eₕ multiplied by the Bohr radius aₒ, then divided by the mass of the
# electron mₑ. It then uses the luminiferous radius of the proton to calibrate
# the density of the aether and its surface charge density.
#===============================================================================
# Refer to https://pint.readthedocs.io/en/stable/ for comprehensive
# documentation for the "pint" unit package.
#
# Install as follows, if not already present in your version of Linux.
# sudo apt-get install python3-pint
#
# This Python script was developed by Dr Michael Heffron to compare
# "fundamental constants of physics" derived from the aether to their
# values published as CODATA 2022.
#===============================================================================

import math
from pint import UnitRegistry

# Create a pint unit registry
u = UnitRegistry()
Q = u.Quantity

# Define fundamental "constants" of physics.
α =   'fine structure constant'
aₒ  = 'Bohr radius'
afu = 'atomic unit of force'
c   = 'constant speed of light'
ȼ   = 'variable speed of light'
μ_B = 'Bohr magneton'
εₒ  = 'electric constant'
Eₕ  = 'Hartree energy'
G   = 'gravitational constant'
h =   'Planck constant'
K_J = 'Josephson constant'
λ_c = 'Compton wavelength'
mₑ  = 'electron mass'
mₚ  = 'proton mass'
μₒ  = 'magnetic constant'
Φₒ  = 'magnetic flux quantum'
q =   'elementary charge'
x2q = 'quantum of circulation X 2'
R_8 = 'Rydberg constant'
R_K = 'von Klitzing constant'
Zₒ  = 'vacuum impedance'

nist = {}
# CODATA 2022 "exact" values.
nist[c]   = Q(2.9979245800000e8, 'm/s')
nist[q]   = Q(1.6021766340000e-19,  'A*s') 
nist[h]   = Q(6.6260701500000e-34, 'kg*m**2/s')

# CODATA 2022 "measured" values, omitting (uncertainty).
nist[afu] = Q(8.2387235038e-8, 'kg*m/s**2')           # N = kg*m/s**2
nist[μ_B] = Q(9.2740100657e-24, 'A*m**2')             # J/T = A*m**2
nist[aₒ]  = Q(5.29177210544e-11, 'm')
nist[εₒ]  = Q(8.8541878188e-12, 'A**2*s**4/kg/m**3')  # F/m = A**2*s**4/kg/m**3
nist[α]   = Q(7.2973525643e-3)
nist[Eₕ]  = Q(4.3597447222060e-18, 'kg*m**2/s**2')    # J = kg*m**2/s**2
nist[G]   = Q(6.67430e-11, 'm**3/s**2*kg')
nist[K_J] = Q(483597.8484e9, 'A*s**2/kg/m**2')        # Hz/V = A*s**2/kg/m**2
nist[λ_c] = Q(2.42631023538e-12, 'm')
nist[mₑ]  = Q(9.1093837139e-31, 'kg')
nist[mₚ]  = Q(1.67262192595e-27, 'kg')
nist[μₒ]  = Q(1.25663706127e-6, 'kg*m/A**2/s**2')     # N/A*2 = kg*m/A**2/s**2
nist[Φₒ]  = Q(2.067833848e-15, 'kg*m**2/A/s**2')      # Wb = kg*m**2/A/s**2
nist[x2q] = Q(7.2738950934e-4, 'm**2/s')
nist[R_8] = Q(10973731.568157, '1/m')
nist[R_K] = Q(25812.80745, 'kg·m**2/A**2/s**3')       # ohm = kg·m**2/A**2·s**3
nist[Zₒ]  = Q(376.730313412, 'kg*m**2/A**2/s**3')     # ohm = kg·m**2/A**2·s**3

# Scalar used to determine the volume of an ellipsoid particle/body.
volume_scalar = 4.0 * math.pi / 3.0

# Define basic aether properties.
𝕣_λ = 'luminiferous radius of light'
ρ   = 'aether density'
P   = 'aether pressure'
Φ   = 'aether mass flux'
σ2  = 'aether surface charge density squared'

# Define fundamental luminiferous aether values.
aether = {}

# Determine gravitational parameter of proton using NIST values.
ϰₚ           = nist[Eₕ] * nist[aₒ] / nist[mₑ]
# Determine the luminiferous radius of the proton using NIST values.
𝕣ₚ           = ϰₚ  / nist[c]**2

# Determine density of aether using NIST values.
aether[ρ]    = nist[mₚ] / (volume_scalar * 𝕣ₚ**3)
# Determine square surface charge density of aether using NIST values.
# NOTE: This exact definition is necessary due to 2019 SI redefinition
# of ampere, tying it to elementary charge rather than magnetic force.
# That had the effect of changing μₒ from "exact" to measured, thereby
# changing the calibration of aether's surface charge density.
aether[σ2]   = aether[ρ] / nist[μₒ]
# Determine mass flux of aether.
aether[Φ]    = aether[ρ] * nist[c]
# Determine pressure of aether.
aether[P]    = aether[Φ] * nist[c]

# Determine electromagnetic constants from aether properties.
# NOTE: ε₀ is the reciprocal of pressure because Oliver Heaviside defined
# permittivity as the reciprocal of elasticity.
aether[εₒ] = aether[σ2] / aether[P]
aether[μₒ] = aether[ρ] / aether[σ2]
aether[Zₒ] = aether[Φ] / aether[σ2]

# Determine the variable propagation rate of light in aether (cₐ), ȼ = √(P/ρ).
aether[ȼ]   = (aether[P] / aether[ρ])**0.5

class Dab:
    """Just a little dab of mass, encapsulated by oscillating/whirling aether. """
    def __init__(self, mass: u.Quantity, name:str):
        # Name of this little dab of matter.
        self.name = name
        # Mass contained within the luminiferous radius.
        self.mass = mass
        # Eq 6-3 of "The Luminiferous Aether: primary substance of the universe"
        self.radius = (self.mass / (volume_scalar * aether[ρ]))**(1.0/3.0)
        # Volume
        self.volume = volume_scalar * self.radius**3
        # Resistance of this dab of matter to aether flow.
        self.kinematicViscosity = self.radius * aether[ȼ]
        # Gravitation produced by the kinematic viscosity of this dab of matter.
        self.gravitationalParameter = self.kinematicViscosity * aether[ȼ]
        # Eq 4-3 of "The Luminiferous Aether: primary substance of the universe"
        self.surfaceTension = aether[P] * self.radius

def g2m(gravParm):
    """Determine mass of object from its gravitational parameter."""
    # Eq 4-1 of "The Luminiferous Aether: primary substance of the universe"
    radius = gravParm / aether[ȼ]**2
    # Eq 3-3 of "The Luminiferous Aether: primary substance of the universe"
    return aether[ρ] * volume_scalar * radius**3

# ASCII color codes.
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
    print('{:>45} = {:.15E~P}'.format(legend, value))
    
def showDab(dab):
    """Show important characteristics of matter."""
    print()
    indent(dab.name, 'gravitational parameter', dab.gravitationalParameter)
    indent(dab.name, 'kinematic viscosity', dab.kinematicViscosity)
    indent(dab.name, 'mass', dab.mass)
    indent(dab.name, 'radius', dab.radius)
    indent(dab.name, 'volume', dab.volume)
    indent(dab.name, 'surface tension', dab.surfaceTension)

# Kepler's Third Law calculation of the gravitational parameter of light
# via the Hartree energy and the Rydberg constant.
Eₑ = 0.5 * nist[Eₕ]      # Binding energy 13.6 eV.
vₑ = (Eₑ / nist[mₑ])**0.5 # Electron velocity.
rₑ = 1.0 / nist[R_8]      # Inverse of Rydberg wavenumber.
ϰ_λ = vₑ**2 * rₑ          # ϰ=v²r
𝕣_λ = ϰ_λ / nist[c]**2

# Display light properties derived from NIST measurements.
light = Dab(𝕣_λ**3 * volume_scalar * aether[ρ], 'light')
indent('', 'light gravitational parameter, ϰ_λ', ϰ_λ) 
indent('', 'luminiferous radius of light, 𝕣_λ', 𝕣_λ) 

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
        # Replace all division symbols except the first with the bullet operator.
        val = val.replace('/','!',1)
        val = val.replace('/','·')
        val = val.replace('!','/')
        # Format output for display.
        match = '{}{:>26} : {:<27} ({} digits match)'
        if 0.999999999 <= ratio <= 1.0000000005:
            color = LIGHT_GREEN
        else:
            color = LIGHT_YELLOW
        # Assess whether all digits match NIST value.
        if (n > 14) or (nval[n+1] == "0" and nval[n+2] == "0"):
            n = "ALL " + str(n)
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
muon     = Dab(Q(1.88353162700000e-28, 'kg'), 'muon')
proton   = Dab(Q(1.67262192595000e-27, 'kg'), 'proton')
sun      = Dab(g2m(Q(1.32712440018000e20, 'm**3/s**2')), 'sun')

# Approximate Newtonian mass of the sun (not its luminiferous mass!!!)
# intentionally restricted to 6 digits accuracy of NIST value for G.
sunMass  = sun.gravitationalParameter / (0.9999995 * nist[G])

# Calculate fundamental constant values from the aether.
aether[q]   = (4.0 * math.pi * electron.volume * proton.radius * aether[σ2])**0.5
aether[G]   = sun.gravitationalParameter / sunMass
aether[h]   = light.kinematicViscosity * electron.mass
aether[R_K] = aether[h] / aether[q]**2
aether[λ_c] = 𝕣_λ # For comparison to NIST λ_c.
aether[mₑ]  = electron.mass
aether[mₚ]  = proton.mass
aether[μ_B] = light.kinematicViscosity * aether[q] / (4.0 * math.pi)
aether[aₒ] = (light.radius / (2.0 * math.pi))**2 / proton.radius
aether[α]   = 2.0 * math.pi * proton.radius / light.radius
aether[Eₕ]  = electron.mass * proton.gravitationalParameter / aether[aₒ]
aether[afu] = electron.mass * proton.gravitationalParameter / aether[aₒ]**2
aether[K_J] = 2.0 * aether[q] / aether[h]
aether[Φₒ]  = aether[h] / (2.0 * aether[q])
aether[R_8] = proton.radius / (2.0 * aether[aₒ] * light.radius)
aether[x2q] = light.kinematicViscosity

# Display fundamental aether values
indent('', 'aether density', aether[ρ])
indent('', 'aether mass flux', aether[Φ])
indent('', 'aether pressure', aether[P])
indent('', 'aether surface charge density squared', aether[σ2])
indent('', 'variable speed of light', aether[ȼ])

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
#compare(mₑ)  # Vacuous, mass was used to define the Dab!
#compare(mₚ)  # Vacuous, mass was used to define the Dab!
compare(μ_B)
compare(aₒ)
compare(εₒ)
compare(q)
compare(α)
compare(Eₕ)
print('{}NOTE: the following value is the extremely accurate gravitational parameter'.format(LIGHT_WHITE))
print('of the sun divided by its very inaccurate alleged Newtonian mass.')
compare(G)
compare(K_J)
compare(λ_c)
compare(μₒ)
compareDerivation(Φₒ, nist[h] / (2.0 * nist[q]), 'h/2q')
compare(h)
print('{}NOTE: the following two values are approximately the kinematic viscosity of light.'.format(LIGHT_WHITE))
compareDerivation(x2q, nist[h] / electron.mass, 'h/mₑ')
compare(R_8)
compare(R_K)
compare(Zₒ)
