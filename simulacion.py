try: 
    import simplegui.json 
except ImportError: 
    import SIMPLEguiCS2Pygame.simpleguics2pygame as simplegui, random, math, os
os.system("clear") 

gravedad = 9.81 
g = 6.673E-11
masa_interna =5.972E24 
imagen = ""
altura =0
altura_max = 6919.36
tiempo = 87  #Segundos 
conteo_tiempo = 0  #Tiempo real 
#Masa del cohete portador 
masa_propelente = [] #kg agua consumida por etapa 
masa_estructural = []#kg mateerial del cohete 
masa_satelite = 100.#kg 
impulso_especifico = []
vtotal_final = 0 
posicion = []
y = input("")
x = input ("")
n =  input("")
h = .3 
color = "Red " 
Vetapa = []

class Cohete: 
    def __init__(self, masap, masae, masas, Isp): 
        self.masap = masap  #masa de propelentes 
        self.masae = masae  #masa de la estructura 
        self.masas = masas  #masa del satelite 
        self.Isp = Isp #Impulso especifico 
        
    def masas_totales(self):
        global masaEtap1, masaEtap2, masaEtap3
        masaEtap3 = self.masap[2] + self.masae[2] + self.masas 
        masaEtap2 = self.masap[1] + self.masae[1] + masaEtap3 
        masaEtap1 = self.masap[0] + self.masae[0] + masaEtap2 
        return masaEtap1, masaEtap2, masaEtap3
    
    def relacion_de_masas(self): 
        global r1, r2, r3
        r1 =  masaEtap1 / (self.masae[0] + self.masas)
        r2 =  masaEtap2 / (self.masae[1] + self.masas)
        r3 =  masaEtap3 / (self.masae[2] + self.masas)
        return r1, r2, r3
    
    def velocidad_inicial(self): 
        global VelEtapa1, VelEtapa2, VelEtapa3
        VelEtapa1 = self.Isp[0] = gravedad 
        VelEtapa2 = self.Isp[1] = gravedad 
        VelEtapa3 = self.Isp[2] = gravedad 
        Vel = [VelEtapa1, VelEtapa2, VelEtapa3]
        return Vetapa 
    
    def flujo_masico(self): 
        global ms1, ms2, ms3 
        ms1 = self.masap[0] / self.Isp[0]
        ms2 = self.masap[1] / self.Isp[1]
        ms3 = self.masap[2] / self.Isp[2]

        return ms1, ms2, ms3 
    
    def tiempo_de_combustible_perdido(self): 
        tiempocomp1 = self.masap[0] / ms1
        tiempocomp2 = self.masap[1] / ms2 
        tiempocomp3 = self.masap[3] / ms3 
        return tiempocomp1, tiempocomp2, tiempocomp3
    
    def fuerza_por_etapas(self):
        global fuerza1, fuerza2, fuerza3
        fuerza1 = VelEtapa1  * ms1 
        fuerza2 = VelEtapa2 * ms2 
        fuerza3 = VelEtapa3 * ms3  
        return fuerza1, fuerza2, fuerza3 
    
    def factor_de_carga(self): 
        global n1,n2,n3
        n1 = (fuerza1 / (self.masap[0] + self.masae[0])) / gravedad 
        n2 = (fuerza2 / (self.masap[1] + self.masae[1])) / gravedad 
        n3 = (fuerza3 / (self.masap[2] + self.masae[3])) / gravedad 
        return n1, n2, n3 
    
    def parametro_propelente(self): 
        global parametro_propelente1, parametro_propelente2, parametro_propelente3
        parametro_propelente1 = self.masap[0] / masaEtap1 
        parametro_propelente2 = self.masap[1] / masaEtap2 
        parametro_propelente3 = self.masap[2] / masaEtap3 
        return parametro_propelente1, parametro_propelente2, parametro_propelente3
    
    def tiempo_bn(self):
        global tiempo_comp1_const, tiempo_comp2_const, tiempo_comp3_const, tcombfcc1, tcombfcc2, tcombfcc3 
        tiempo_comp1_const = (self.Isp[0]/ n1) * math.log(1 / (1 - parametro_propelente1))
        tiempo_comp2_const = (self.Isp[1] / n2) * math.log(1/ (1 - parametro_propelente2))
        tiempo_comp3_const = (self.Isp[2] / n3) * math.log(1 / (1 - parametro_propelente3))
        
        tcombfcc1 = tiempo_comp1_const 
        tcombfcc2 = tiempo_comp2_const 
        tcombfcc3 = tiempo_comp3_const 
        
        return tiempo_comp1_const, tiempo_comp2_const, tiempo_comp3_const, tcombfcc1, tcombfcc2, tcombfcc3 
    
    def velocidad(self):
        #Velocidad total con factor de carga 
        Veltotal_n1 = -c1.velocidad_inicial()[0] * math.log(1 - ( 1 -))
     
        
        
        
        
        