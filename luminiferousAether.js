// code starts here
function setup() { 
  //===========================================================
  // AetherAnalysis JavaScript by Dr Michael Heffron
  // "quick & dirty" development using https://editor.p5js.org/
  //
  // https://pml.nist.gov/cuu/Constants/Table/allascii.txt
  // is the source for all NIST values.
  //
  // NOTE: This software currently only supports the following
  // measures, all of which must be separated by * and must
  // have ^ followed by a positive or negative number to
  // indicate the exponent:
  //
  // C = coulomb
  // k = kilogram
  // m = meter
  // s = second
  //
  // Functions divide, multiply, and power use only those
  // units of measure.
  //===========================================================
  
  let aether = new aetherClass()
  let data = new dataClass()
  let nist = new nistClass()
  
  console.log("Calibration of the momentum of the luminiferous aether")
  showValue(aether.massFlux)
  showValue(aether.density)
  showValue(aether.pressure)

  showParticle("electron", data.electron)
  showParticle("proton", data.proton)
  showParticle("light", data.light)
    
  compare(data.bohrRadius,nist.bohrRadius)
  compare(data.electronMass,nist.electronMass)
  compare(data.fineStructureConstant,nist.fineStructureConstant)
  compare(data.planckConstant,nist.planckConstant)
  compare(data.protonMass,nist.protonMass)
  compare(data.speedOfLight,nist.speedOfLight)
  compare(data.protonImpedanceElectrical,nist.characteristicImpedanceOfVacuum)
  compare(data.vacuumPermeability,nist.vacuumPermeability)
  compare(data.vacuumPermittivity,nist.vacuumPermittivity)
  compare(data.vonKlitzingConstant,nist.vonKlitzingConstant)
  
  console.log("")
  showValue(data.light.dynamicViscosity)
  showValue(data.light.kinematicViscosity)
  console.log("")
  compare(data.hartreeEnergy,nist.hartreeEnergy)
  compare(data.electrostaticForce,nist.atomicUnitOfForce)
  compare(data.magneticFluxQuantum,nist.magneticFluxQuantum)
  compare(data.josephsonConstant,nist.josephsonConstant)
  compare(data.bohrMagneton,nist.bohrMagneton)
  compare(data.rydbergConstant,nist.rydbergConstant)
  compare(data.light.radius,nist.comptonWavelength)
  console.log("")
  showValue(data.vacuumPermeabilityPhysical)
  compare(data.vacuumPermeabilityElectrical,nist.vacuumPermeability)
  console.log("")
  showValue(data.vacuumPermittivityPhysical)
  compare(data.vacuumPermittivityElectrical, nist.vacuumPermittivity)
  console.log("")
  showValue(divide(data.light.surfaceTension, aether.pressure))
  compare(data.elementaryCharge, nist.elementaryCharge)
}
class aetherClass {
  constructor() {
    /*
      These precise NIST constants determine the calibration of the aether.
      To analyze how the aether impacts the fundamental constants of physics,
      these values are all that needs to be changed.
      This code was
      refactored to emphasize that this is a Momentum Model by basing
      everything on the momentum of the proton and then converting that
      to the mass flux within the proton by dividing by the proton's
      volume.
    */
    this.shapeFactor = [(4.0 * PI / 3.0) + " ","calibration.shapeFactor"]
    this.classicElectronRadius = ["2.8179403205(13)e-15 m^1", "calibration.classicElectronRadius"]
    this.protonMass = ["1.67262192595(52)e-27 k^1", "calibration.protonMass"]
    let protonRadius3 = power(this.classicElectronRadius, 3.0)
    // NOTE: The following calculation is NOT A MISTAKE !!!
    let protonVolume = multiply(this.shapeFactor, protonRadius3)
    this.protonVolume = [protonVolume[0],"calibration.protonVolume"]
    this.speedOfLight = ["2.99792458e8 m^1*s^-1", "calibration.speedOfLight"]

    /*
      Determine the precise mass flux from the calibaration constants.
      This code was refactored to emphasize that this is a Momentum Model
      by basing everything on the momentum of the proton and then converting
      that to the mass flux within the proton by dividing by the proton's
      volume.
    */
    let massFlux = divide(multiply(this.protonMass, this.speedOfLight), this.protonVolume)
    this.massFlux = [massFlux[0],"aether.massFlux",massFlux[1]]
    // From that, derive the density and pressure of the aether.
    let density = divide(this.massFlux, this.speedOfLight)
    this.density = [density[0],"aether.density",density[1]]
    let pressure = multiply(this.massFlux, this.speedOfLight)
    this.pressure = [pressure[0],"aether.pressure",pressure[1]]
  }
}
class dataClass {
  constructor () {
    this.aether = new aetherClass()
    this.nist = new nistClass()
    this.one = ["1.0 ", "aether.one"]
    this.two = ["2.0 ", "aether.two"]
    this.twoPi = power(this.nist.twoPi, 2.0)
    this.fourPi = [(4 * PI)+" ", "data.fourPi"]
    
    this.electron = new particleClass(this.nist.electronMass,"electron")
    this.light = new particleClass(multiply(this.aether.density, this.nist.comptonVolume),"light")
    this.proton = new particleClass(this.nist.protonMass,"proton")
    
    let cgs2mks = ["1.000000000000000e7 C^2*k^-1*m^-1", "aether.cgs2mks"]
    let elementaryCharge = power(multiply(cgs2mks, multiply(this.electron.mass, this.proton.radius)), 0.5)
    this.elementaryCharge = [elementaryCharge[0], "aether.elementaryCharge", elementaryCharge[1]]
    let q2over4pi = divide(multiply(cgs2mks, multiply(this.electron.mass, this.proton.radius)), this.fourPi)
    // NOTE: fineStructureConstant must be defined before bohrRadius.
    let fineStructureConstant = divide(multiply(this.nist.twoPi, this.proton.surfaceTension), this.light.surfaceTension)
    this.fineStructureConstant = [fineStructureConstant[0],"aether.fineStructureConstant",fineStructureConstant[1]]
    let bohrMagneton = divide(multiply(this.elementaryCharge, this.light.kinematicViscosity), this.fourPi)
    this.bohrMagneton = [bohrMagneton[0], "aether.bohrMagneton", bohrMagneton[1]]
    let bohrRadius = divide(power(divide(this.light.radius, this.nist.twoPi), 2.0), this.proton.radius)
    this.bohrRadius = [bohrRadius[0],"aether.bohrRadius",bohrRadius[1]]
    let electronMass = multiply(this.aether.density, this.electron.volume)
    this.electronMass = [electronMass[0],"aether.electronMass",electronMass[1]]
    let hartreeEnergy = multiply(this.electronMass, divide(this.proton.gravParm, this.bohrRadius))
    this.hartreeEnergy = [hartreeEnergy[0], "aether.hartreeEnergy", hartreeEnergy[1]]
    let electrostaticForce = divide(this.hartreeEnergy, this.bohrRadius)
    this.electrostaticForce = [electrostaticForce[0], "aether.electrostaticForce", electrostaticForce[1]]
    let two = ["2.0 ","2"]
    let magneticFluxQuantum = divide(multiply(this.electronMass,this.light.kinematicViscosity), multiply(two, this.elementaryCharge))
    this.magneticFluxQuantum = [magneticFluxQuantum[0], "aether.magneticFluxQuantum", magneticFluxQuantum[1]]
    let josephsonConstant = divide(multiply(two, this.elementaryCharge), multiply(this.electronMass,this.light.kinematicViscosity))
    this.josephsonConstant = [josephsonConstant[0], "aether.josephsonConstant", josephsonConstant[1]]
    let physicalOhm = divide(this.light.kinematicViscosity, this.electronMass)
    this.physicalOhm = [physicalOhm[0], "aether.physicalOhm", physicalOhm[1]]
    let protonImpedanceElectrical = divide(multiply(this.electronMass, this.proton.kinematicViscosity), q2over4pi)
    this.protonImpedanceElectrical = [protonImpedanceElectrical[0],"aether.protonImpedanceElectrical",protonImpedanceElectrical[1]]
    let protonImpedancePhysical = multiply(this.electronMass, this.proton.kinematicViscosity)
    this.protonImpedancePhysical = [protonImpedancePhysical[0],"aether.protonImpedancePhysical",protonImpedancePhysical[1]]
    let protonMass = multiply(this.aether.density, this.proton.volume)
    this.protonMass = [protonMass[0],"aether.protonMass",protonMass[1]]
    let rydbergConstant = divide(this.proton.radius,multiply(two,multiply(this.bohrRadius,this.light.radius)))
    this.rydbergConstant = [rydbergConstant[0],"aether.rydbergConstant",rydbergConstant[1]]
    let speedOfLight = power(divide(this.aether.pressure, this.aether.density), 0.5)
    this.speedOfLight = [speedOfLight[0],"aether.speedOfLight",speedOfLight[1]]
    let planckConstant = multiply(this.electronMass, multiply(this.light.radius, this.speedOfLight))
    this.planckConstant = [planckConstant[0], "aether.planckConstant", planckConstant[1]]
    let vacuumPermeabilityPhysical = multiply(this.aether.density, multiply(this.electron.volume, this.proton.radius))
    this.vacuumPermeabilityPhysical = [vacuumPermeabilityPhysical[0], "aether.vacuumPermeabilityPhysical", vacuumPermeabilityPhysical[1]] 
    let vacuumPermeabilityElectrical = divide(vacuumPermeabilityPhysical, q2over4pi)
    this.vacuumPermeabilityElectrical = [vacuumPermeabilityElectrical[0], "aether.vacuumPermeabilityElectrical", vacuumPermeabilityElectrical[1]]
    let vacuumPermittivityPhysical = divide(this.one, multiply(this.aether.pressure, multiply(this.electron.volume, this.proton.radius)))
    this.vacuumPermittivityPhysical = [vacuumPermittivityPhysical[0], "aether.vacuumPermittivityPhysical", vacuumPermittivityPhysical[1]]
    let vacuumPermittivityElectrical = multiply(q2over4pi, this.vacuumPermittivityPhysical)
    this.vacuumPermittivityElectrical = [vacuumPermittivityElectrical[0], "aether.vacuumPermittivityElectrical", vacuumPermittivityElectrical[1]]
    let vacuumPermeability = divide(this.proton.radius, this.electron.chiQ(2))
    this.vacuumPermeability = [vacuumPermeability[0],"aether.vacuumPermeability",vacuumPermeability[1]]
    let vacuumPermittivity = divide(this.electron.chiQ(2), this.proton.gravParm)
    this.vacuumPermittivity = [vacuumPermittivity[0], "aether.vacuumPermittivity",vacuumPermittivity[1]]
    let vonKlitzingConstant = divide(multiply(this.electronMass,this.light.kinematicViscosity), power(this.elementaryCharge, 2.0))
    this.vonKlitzingConstant = [vonKlitzingConstant[0],"aether.vonKlitzingConstant",vonKlitzingConstant[1]]
  }
}
class nistClass {
  constructor () {
    this.fourPi = [(4.0 * PI) + " ","nist.fourPi"]
    this.shapeFactor = [(4.0 * PI / 3.0) + " ","nist.shapeFactor"]
    this.twoPi = [(2.0 * PI) + " ","nist.twoPi"]
    
    // NIST "constants" (actually very stable variables)
    this.atomicUnitOfForce = ["8.2387235038(13)e-8 k^1*m^1*s^-2","nist.atomicUnitOfForce"]
    this.bohrMagneton = ["9.2740100657(29)e-24 C^1*m^2*s^-1","nist.bohrMagneton"]
    this.bohrRadius = ["5.29177210544(82)e-11 m^1","nist.bohrRadius"]
    this.characteristicImpedanceOfVacuum = ["3.76730313412(59)e2 C^-2*k^1*m^2*s^-1","nist.characteristicImpedanceOfVacuum"]
    this.classicElectronRadius = ["2.8179403205(13)e-15 m^1","nist.classicElectronRadius"]
    this.comptonWavelength = ["2.42631023538(76)e-12 m^1","nist.comptonWavelength"]
    let comptonVolume = multiply(this.shapeFactor, power(this.comptonWavelength, 3.0))
    this.comptonVolume = [comptonVolume[0],"nist.comptonVolume"]
    this.electronMass = ["9.1093837139(28)e-31 k^1","nist.electronMass"]
    this.elementaryCharge = ["1.602176634(exact)e-19 C^1","nist.elementaryCharge"]
    // The following value gives far more correct aether values.
    this.fineStructureConstant = ["7.2973525693(11)e-3 ","nist.fineStructureConstant"]
    this.hartreeEnergy = ["4.3597447222060(48)e-18 k^1*m^2*s^-2","nist.hartreeEnergy"]
    this.josephsonConstant = ["4.835978484(exact)e14 C^1*k^-1*m^-2*s^1", "nist.josephsonConstant"]
    this.magneticFluxQuantum = ["2.067833848(exact)e-15 C^-1*k^1*m^2*s^-1","nist.magneticFluxQuantum"]
    this.planckConstant = ["6.62607015(exact)e-34 J*Hz^-1","nist.planckConstant"]
    this.protonMass = ["1.67262192595(52)e-27 k^1","nist.protonMass"]
    let q2over4pi = divide(power(this.elementaryCharge,2.0),this.fourPi)
    this.q2over4pi = [q2over4pi[0],"nist.q2over4pi"]
    this.quantumOfCirculationX2 = ["7.2738950934(23)e-4 m^2*s^-1","nist.quantumOfCirculationX2"]
    this.rydbergConstant = ["1.0973731568157(12)e7 m^-1","nist.rydbergConstant"]
    this.speedOfLight = ["2.99792458(exact)e+8 m^1*s^-1","nist.speedOfLight"]
    this.vacuumPermeability = ["1.25663706212(19)e-6 C^-2*k^1*m^1","nist.vacuumPermeability"]
    this.vacuumPermittivity = ["8.8541878128(13)e-12 C^2*k^-1*m^-3*s^2","nist.vacuumPermittivity"]
    this.vonKlitzingConstant = ["2.581280745(exact)e4 C^-2*k^1*m^2*s^-1","nist.vonKlitzingConstant"]
  }
}
class particleClass {
  constructor(mass, name) {
    this.aether = new aetherClass()
    this.nist = new nistClass()
    
    this.mass = mass
    this.name = name
    
    let energy = multiply(this.mass, power(this.nist.speedOfLight, 2.0))
    this.energy = [energy[0],this.name + ".energy",energy[1]]
    // Luminiferous radius, which could easily be mistaken for Schwarzschild radius.
    let radius = power(divide(mass, multiply(this.nist.shapeFactor, this.aether.density)), (1/3))
    this.radius = [radius[0], this.name + ".radius",radius[1]]
    //this.period = divide(this.radius, this.nist.speedOfLight)
    let circumference = multiply(this.nist.twoPi, this.radius)
    this.circumference = [circumference[0], this.name+".circumference", circumference[1]]
    let gravParm = multiply(power(this.aether.speedOfLight, 2.0), this.radius)
    this.gravParm = [gravParm[0], this.name+".gravParm", gravParm[1]]
    let surfaceTension = multiply(this.aether.pressure, this.radius)
    this.surfaceTension = [surfaceTension[0], this.name+".surfaceTension", surfaceTension[1]]
    let volume = multiply(this.nist.shapeFactor, power(this.radius, 3.0))
    this.volume = [volume[0], this.name+".volume", volume[1]]
    let momentum = multiply(this.mass, this.nist.speedOfLight)
    this.momentum = [momentum[0], this.name+".momentum", momentum[1]]

  let kinematicViscosity = multiply(this.radius, this.nist.speedOfLight)
  this.kinematicViscosity = [kinematicViscosity[0], this.name+".kinematicViscosity", kinematicViscosity[1]]
  let dynamicViscosity = multiply(this.kinematicViscosity, this.aether.density)
  this.dynamicViscosity = [dynamicViscosity[0], this.name+".dynamicViscosity", dynamicViscosity[1]]
  }
  // Functions.
  chiQ(exp) {
    let chiQ = divide(power(this.nist.elementaryCharge, exp), multiply(this.nist.fourPi, this.mass))
    return [chiQ[0],this.name+".chiQ("+exp+")"]
  }
  mcMomentumTimes(value) {
    return multiply(this.momentum, value)
  }
}
function showParticle(label, blackHole) {
  console.log("\nParameters of " + label + " (black hole) produced by the luminiferous aether")
  console.log(label + ".radius: " + blackHole.radius[0])
  console.log(label + ".circumference: " + blackHole.circumference[0])
  console.log(label + ".surfaceTension: " + blackHole.surfaceTension[0])
  console.log(label + ".mass: " + blackHole.mass[0])
  console.log(label + ".momentum: " + blackHole.momentum[0])
  console.log(label + ".energy: " + blackHole.energy[0])
  console.log(label + ".volume: " + blackHole.volume[0])
  console.log(label + ".gravParm: " + blackHole.gravParm[0])
  console.log(label + ".dynamicViscosity: " + blackHole.dynamicViscosity[0])
  console.log(label + ".kinematicViscosity: " + blackHole.kinematicViscosity[0])
}
function matchingDigits(aetherValue, nistValue) {
  var marker = "                    "
  var siz = Math.min(aetherValue.length,nistValue.length)
  var num = 0
  for (let i = 0; i<siz;  i++) {
    if (aetherValue[i] == nistValue[i]) {num++}
    else {
      marker = marker.substr(0, i) + "↕ (match until " + num + "th digit)"
      i = siz
    }
  }
  return marker
}
function compare(aetherValue, nistValue) {
  if (aetherValue[2] != undefined) {
    console.log("\n" + aetherValue[1] +" = " + aetherValue[2])
  }
  else {console.log()}
  console.log("Compare " + aetherValue[1] + " & " + nistValue[1]);
  console.log("aether:" + " = " + aetherValue[0])
  console.log("       " + "   " + matchingDigits(aetherValue[0], nistValue[0]))
  console.log("NIST:  " + " = " + nistValue[0])
}
function stripUncertainty(value) {
  var op = value.indexOf('(')
  if (op >= 0) {
    var cl = value.indexOf(')')
    return value.substr(0, op) + value.substr(cl+1)
  }
  else {return value}
}
function showValue(value) {
  if (value[2] != undefined) {console.log(value[1] + " = " + value[0] + " " + value[2])}
  else {console.log(value[1] + " = " + value[0])}
}
function divide(numerator, divisor) {
  var num = stripUncertainty(numerator[0]).split(" ")
  var den = stripUncertainty(divisor[0]).split(" ")
  var val = parseFloat(num[0]) / parseFloat(den[0])
  var un1 = num[1].split("*")
  var un2 = den[1].split("*")
  var u1 = ["C","k","m","s"]
  var u2 = [0, 0, 0, 0]
  for (var i = 0; i < un1.length; i++) {
    for (var m = 0; m < u1.length; m++) {
      if (un1[i].charAt(0) == u1[m]) {
        u2[m] += parseInt(un1[i].substring(2))
      }
    }
  }
  for (var j = 0; j < un2.length; j++) {
    for (var n = 0; n < u1.length; n++) {
      if (un2[j].charAt(0) == u1[n]) {
        u2[n] -= parseInt(un2[j].substring(2))
      }
    }
  }
  var units = ""
  for (var u = 0; u < u1.length; u++) {
    if (u2[u] != 0) {
      if (units.length > 0) {
        units += "*"
      }
      units += u1[u] + "^" + u2[u]
    }
  }
  var res = val.toExponential(15) + " " + units
  var op = "(" + numerator[1] +"/" + divisor[1] + ")"
  return [res, op]
}
function multiply(n1, n2) {
  var v1 = stripUncertainty(n1[0]).split(" ")
  var v2 = stripUncertainty(n2[0]).split(" ")
  var val = parseFloat(v1[0]) * parseFloat(v2[0])
  var un1 = v1[1].split("*")
  var un2 = v2[1].split("*")
  var u1 = ["C","k","m","s"]
  var u2 = [0, 0, 0, 0]
  for (var i = 0; i < un1.length; i++) {
    for (var m = 0; m < u1.length; m++) {
      if (un1[i].charAt(0) == u1[m]) {
        u2[m] += parseInt(un1[i].substring(2))
      }
    }
  }
  for (var j = 0; j < un2.length; j++) {
    for (var n = 0; n < u1.length; n++) {
      if (un2[j].charAt(0) == u1[n]) {
        u2[n] += parseInt(un2[j].substring(2))
      }
    }
  }
  var units = ""
  for (var u = 0; u < u1.length; u++) {
    if (u2[u] != 0) {
      if (units.length > 0) {
        units += "*"
      }
      units += u1[u] + "^" + u2[u]
    }
  }
  var res = val.toExponential(15) + " " + units
  var op = "(" + n1[1] + "*" + n2[1] + ")"
  return [res, op]
}
function power(value, exp) {
  var v = stripUncertainty(value[0]).split(" ")
  var val = parseFloat(v[0])**exp
  var un = v[1].split("*")
  var u1 = ["C","k","m","s"]
  var u2 = [0, 0, 0, 0]
  for (var i = 0; i < un.length; i++) {
    for (var m = 0; m < u1.length; m++) {
      if (un[i].charAt(0) == u1[m]) {
        u2[m] += parseInt(un[i].substring(2))
      }
    }
  }
  var units = ""
  for (var u = 0; u < u1.length; u++) {
    if (u2[u] != 0) {
      if (units.length > 0) {
        units += "*"
      }
      units += u1[u] + "^" + u2[u] * exp
    }
  }
  var res = val.toExponential(15) + " " + units
  var op = "(" + value[1] + "^" + exp + ")"  //console.log("power: " + v + "**" + exp + " = " + res)
  return [res, op]
}