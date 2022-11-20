class Battery:
    g: float = 9.80665 # Gravitational acceleration [ms/s^2]
    rho: float = 1.204 # Air density [kg/m^3], at surface

    Apf: float = 0
    Atf: float = 0
    
    def __init__(self,
                 md: float = 0.5, # Mass [kg], drone
                 mp: float = 0, # Mass [kg], payload
                 Af: float = 0.5, # Cross-section [m^2], horizontal
                 At: float = 0.1, # Cross-section [m^2], vertical
                 Cd: float = 1, # Drag coefficient
                 Ct: float = 0.03, # Thrust coefficient
                 Ap: float = 0.5, # Propeller disc area [m^3]
                 p: float = 0.05 # Propeller radius [m]
                 ):
        self.md = md
        self.mp = mp
        self.Af = Af
        self.At = At
        self.Cd = Cd
        self.Ct = Ct
        self.Ap = Ap
        self.p = p
        
    def set_package(mass, Apf, Atf):
        self.mp = mass
        self.Apf = Apf
        self.Atf = Atf

    def remove_package():
        self.mp = 0
        self.Apf = 0
        self.Atf = 0
        
    def rot_horizontal(vh: float):
        nom = ( 4*(md+mp)^2 * g^2 + \
                rho^2 * Af^2 * Cd^2 * vh^4 )^(1/4)
        dnum = ( r^2 * rho * Ap *  Ct)^(1/2)

        return nom/denum

    def rot_vertical(vv: float):
        nom = ( 2 * (md+mp) * g + \
                rho * At * Cd * vv^2 )^(1/2)

        dnum = ( r^2 * rho * Ap * Ct )^(1/2)

        return nom/denum

    def power(ang_freq: float):
        return 2.258 * 10^(-7) * ang_freq^3 + \
            3.866 * 10^(-5) * ang_freq^2 + \
            5.137 * 10^(-3) * ang_freq + \
            2.616

    
