class Battery:
    g: float = 9.80665 # Gravitational acceleration [ms/s^2]
    rho: float = 1.204 # Air density [kg/m^3], at surface
    
    #Af: float = 0
    #At: float = 0

    Apf: float = 0 # Payload cross-section, hoz 
    Apt: float = 0 # Payload cross-section, vert

    battery_energy = 0 # Energy spent
    n_obs = 0 # How many observations have we seen?
    CA_n = 0 # Commulative average power for observation n
    
    
    def __init__(self,
                 md: float = 0.5, # Mass [kg], drone
                 mp: float = 0, # Mass [kg], payload
                 Af: float = 0.4, # Cross-section [m^2], horizontal
                 At: float = 0.2, # Cross-section [m^2], vertical
                 Cd: float = 1, # Drag coefficient
                 Ct: float = 0.02, # Thrust coefficient
                 r: float = 0.25 # Propeller radius [m]
                 ):
        self.md = md
        self.mp = mp
        self.Af = Af
        self.At = At 
        self.Cd = Cd
        self.Ct = Ct
        self.Ap = (3.14 * (2*r)**2) / 4 # Propeller disc area [m^2] 
        self.r = r

    # Attach package to drone
    # Update package parameters
    def set_package(self, mass, Apf, Apt):
        self.mp = mass / 1000 # Convert to kg
        self.Apf = Apf
        self.Apf = Apt

    # Detach package from drone
    # Set package parameters to 0
    def remove_package(self):
        self.mp = 0
        self.Apf = 0
        self.Atf = 0

    def update(self, dt, vv = 0, vh = 0):
        ep = self.get_move_EP(dt, vv, vh)
        self.battery_energy += ep[0]
        self.update_com_avg(ep[1])
        
        return ep

    # Get power as function of rotor angular velocity
    # Power approximated using 3rd degree polynomial
    def get_power(self, ang_freq: float):
        return 2.258 * 10**(-7) * ang_freq**3 + \
            3.866 * 10**(-5) * ang_freq**2 + \
            5.137 * 10**(-3) * ang_freq + \
            2.616

    # Get power and energy consumption from movement
    def get_move_EP(self, dt, vv = 0, vh = 0):
        ang_freq_h = self.rot_horizontal(vh)
        ang_freq_v = self.rot_vertical(vv)

        Ph = self.get_power(ang_freq_h)
        Pv = self.get_power(ang_freq_v)
        P = Ph + Pv
        E = P * dt
        
        #print("P: {:.2f}".format(P))
        #print("E: {:.2f}".format(E))
        #print("dt: {:.2f}".format(dt))
        
        return (E, P)

    # Calculate angular velocity for horizontal travel at vh m/s
    def rot_horizontal(self, vh: float):
        nom = ( 4*(self.md+self.mp)**2 * self.g**2 + \
                self.rho**2 * (self.Af+self.Apf)**2 * self.Cd**2 * vh**4 )**(1/4)
        dnum = ( self.r**2 * self.rho * self.Ap *  self.Ct)**(1/2)

        return nom/dnum

    # Calculate angular velocity for vertical travel at vh m/s
    def rot_vertical(self, vv: float):
        nom = ( 2 * (self.md+self.mp) * self.g + \
                self.rho * (self.At+self.Apt) * self.Cd * vv**2 )**(1/2)

        dnum = ( self.r**2 * self.rho * self.Ap * self.Ct )**(1/2)

        return nom/dnum

    def conv_Ah(power, dt):
        return 0

    def get_energy_consumed(self):
        return self.battery_energy

    # Update cumulative average of the instantatious
    # power of the drone
    def update_com_avg(self, inst_power: float):
        #print("Inst power: {:.2f}".format(inst_power))
        self.CA_n = (inst_power + self.n_obs * self.CA_n) /\
            (self.n_obs + 1)
        
        self.n_obs = self.n_obs + 1

    def get_battery_stats(self):
        return (self.CA_n, self.battery_energy, self.n_obs)
    

    

    
