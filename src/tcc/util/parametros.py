# equivalente.py

"""
Classe que deve representar as linahs de transmissão
"""


class Parametros:
    
    def __init__(self, tf, rele, rf = 0.01, delta_m = 0.01):
        self.tf = tf
        self.rele = rele
        
        #validação para que delta_m não seja zero
        if delta_m == 0:
            self.delta = 0.01
        else:
            self.delta = delta_m
        
        #validação para que delta_m não seja zero
        if rf == 0:
            self.rf = 0.01
        else:
            self.rf = delta_m
    
    
    '''Getters '''
            
    def get_tipo_falta(self):
        return self.tf
    
    def get_tipo_rele(self):
        return self.rele
    
    def get_intervalo_tempo(self):
        return self.delta
    
    def get_resistencia_falta(self):
        return self.rf
    
