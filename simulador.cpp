#include <stdio.h> 
#include <math.h> 

//Variables 
float velinicial = 0.0, velfinal, p, pi, hi, voli, pf, hf, a, mp, ti, tf, dt, area, diametro, pa=101325, mr=1.3, volt, d=0.0023, hmax; 

int main(){

    float accel(float, float, float); 
    float m(float);
    float presion(float); 

    FILE *arc; arc=fopen("Simulacion_Lanzamiento.xls", "w"); 
    printf("Simulaci%cn de lanzamiento de cohete: ", 162); 
    printf("\nPresi%cn inicial (psi)", 162);
    scanf("%f", &pi);
    pi=pi*6894.76; // Conversión a pascales 
    printf("\n Volumen inicial del gas (cnm3)");
    scanf("%f",  &voli);
    voli= voli/1000000;  // Conversión a m3 
    printf(" \n Volumen total (cm3): "); 
    scanf("%f", &volt);
    volt = volt/1000000;
    printf("\n Di%cmetro del orificio de escape en metros: ", 160);
    scanf("%f", &diametro);
    area = pow((diametro/2), 2)*3.1416; 

    printf("\n%cQn%c tama%co de paso (seg)? : ", 168,130,164);
    scanf("%f", &dt);
    fprintf(arc, "t\tP\tM\tA\tVel\th0");
    p=pi; 

    do{
    fprintf(arc, "\n%f\t%f\t%f\t%f\t%f", ti, p,mp,velinicial,hi);
    mp=m(p);
    if (mp<mr){
        mp=mr;
    }

    tf = ti+ dt;
    if (p>pa){
        if (mp>mr){
    pf = p -(presion(p)*dt);    
    }    
    else{
    pf = p-(p*p*area*pow((2*(p-pa)/1.22),.5)/(pi*velinicial))*dt; 
    } a = accel(p,velinicial,mp);
    } 
    else{
        p=pa;
        a = -9.81-(d+velinicial*velinicial)/mr; 
    }

    velfinal = velinicial+ (a*dt); 
    
    hf = hi+velinicial*dt;
    ti=tf;
    p=pf;
    velinicial=velfinal;
    hi=hf;
    if(hmax<hf){
        hmax=hf;
    }
     }

    while(hi>=0);
        fclose(arc);
        getchar();
        printf("%f", hmax);
    }   

float presion(float p){
    return (p*p*area*pow((2*(p-pa)/1000),.5)/(pi*voli));
}

float accel(float p, float v, float m){
    return ((((2*area*(p-pa))-(d*v*v))/m)-9.81);
}

float m(float p){
    return ((1000*(volt-(pi*voli/p)))+mr);
}