import pandas as pd
import numpy as np
from textwrap import wrap
def syn_proc(lines):
    
                    try:
                        lines.remove('\x1a')
                    except:
                        c=1   
                    index_lines=range(0,len(lines))
                    ############# Preprocessing
                   
                    quot=[]
                    hor=[]
                    
                    file_vald=True
                    
                    for i in index_lines:
                        
                        check=lines[i][:2]
                        lines[i]=lines[i].strip()
                        lines[i]=wrap(lines[i],5,drop_whitespace=False)
                        
                        
                        if len(lines[i]) not in [33,28]:
                            
                            file_vald=False
                            break
                        lines[i][0]=lines[i][0][:2]+";"+lines[i][0][2:]
                        
                        
                        if check=="25":
                            
                            lines[i][2]=lines[i][2][:2]+";"+lines[i][2][2:]
                            lines[i][2]=lines[i][2][:5]+";"+lines[i][2][5:]
                            hindex=range(3,7)
                            for k in hindex:
                                
                                l=True
                                h=0
                                while(l==True):
                                    try:
                                        if lines[i][k][h] in ["0","1","9"]:
                                            lines[i][k]=lines[i][k][:h+1]+";"+lines[i][k][h+1:]
                                        h+=1
                                    except:
                                        
                                        if lines[i][k][h-1]==';':
                                            lines[i][k]=lines[i][k][:h-1]
                                        l=False
                                        
                            result_3 = [item.split(';') for item in lines[i]]
                            lines[i] = [item for l in result_3 for item in l]
                            a=str(lines[i]).replace('[','').replace(']','').replace(" ","").replace("'","").split(",")
                            a=[int(c) for c in a]
                            quot.append(a)
                            
                        elif check=="20":
                           
                            lines[i][2]=lines[i][2][:3]+";"+lines[i][2][3:]
                            result_3 = [item.split(';') for item in lines[i]]
                            lines[i] = [item for l in result_3 for item in l]
                            b=str(lines[i]).replace('[','').replace(']','').replace(" ","").replace("'","").split(",")
                            b=[int(c) for c in b]
                            hor.append(b)
                        else:
                            break
                        
                        
                    if file_vald:   
                    ############ Conversion from List to DataFrame    
                    
                        hor_df=pd.DataFrame(hor)
                        hor_df.columns=["Type Obs","indicatif","annee","mois","jour","heure","visibilite dam","Haut Couche 1 dam","Neb N1 octa","Dir Vent (10 deg)","FF Vent(m/s)","W1 W2","ww","pmer(Hpa)/Geop 850(mgp)","temperature °C","hulidite %","Tension Vapeur (Hpa)","cl","cm","ch","nebulosite","Haut Couche C0 dam","Neb N0 octa","H Autre Cou  C2","Neb N2","Genre C1","Genre C0","Genre C2","Car tendance","Val tendance (Hpa)","pstation (Hpa)","Temp mouillee °C","Temp rosee °C","FF vent en Kt","RR 03H (mm)"]
                        hor_df["mois"]=[s.zfill(2) for s in hor_df["mois"].astype(str)]
                        hor_df["jour"]=[s.zfill(2) for s in hor_df["jour"].astype(str)]
                        hor_df["hor_id"]=hor_df["indicatif"].astype(str)+'_'+hor_df["annee"].astype(str)+hor_df["mois"]+hor_df["jour"]+hor_df["heure"].astype(str)
                        hor_df["Date"]=hor_df["jour"].astype(str)+"/"+hor_df["mois"].astype(str)+"/"+hor_df["annee"].astype(str)+" "+hor_df["heure"].astype(str)
                        hor_df["Date"]=pd.to_datetime(hor_df["Date"], format='%d/%m/%Y %H')
                        
                        
                        quot_df=pd.DataFrame(quot)
                        quot_df.columns=["Type Obs","indicatif","annee","mois","jour","Service station","Brouillard","Orage","Neige","Grele","Gresil","Ins continue","Brume","Rosee","Gelee","Sirocco","Ciel sable","Chasse sable","Tempete sable","Eclair","nuage bas","DDX (10 deg)","FFx (m/s/)","Umin %","Umax %","Tmin °C","Tmax °C","RR0618 (mm)","RR1806 (mm)","RRtotale (mm)","Duree RR0618 (Heur)","Duree RR0024 (Heur)","Evaporation (mm)","Insol matin (Heur)","Insol soir (Heur)","Insol totale (Heur)","Visi min dam","Haut min dam","Etat sol 06H","Epais neige cm","Tmin sol °C","Tmax sol °C"]
                        quot_df["mois"]=[s.zfill(2) for s in quot_df["mois"].astype(str)]
                        quot_df["jour"]=[s.zfill(2) for s in quot_df["jour"].astype(str)]
                        quot_df["quot_id"]=quot_df["indicatif"].astype(str)+'_'+quot_df["annee"].astype(str)+quot_df["mois"]+quot_df["jour"]
                        quot_df["Date"]=quot_df["annee"].astype(str)+"/"+quot_df["mois"].astype(str)+"/"+quot_df["jour"].astype(str)
                        quot_df["Date"]=pd.to_datetime(quot_df["Date"], format='%Y/%m/%d')
                        
                        
                        ########## Data conversion
                        cases=["(Hpa)","°C","(mm)","(Heur)"]
                        
                        quot_df[["RR0618 (mm)","RR1806 (mm)","RRtotale (mm)"]]=quot_df[["RR0618 (mm)","RR1806 (mm)","RRtotale (mm)"]].replace(5555,0)
                        hor_df["RR 03H (mm)"]=hor_df["RR 03H (mm)"].replace(5555,0)
                        
                        
                        quot_df=quot_df.replace(-9999,np.nan)
                        hor_df=hor_df.replace(-9999,np.nan)
                        for index in hor_df.columns:
                            for comp in cases:
                                if index.find(comp)!=-1:       
                                    hor_df[index]*=0.1
                                    hor_df[index]=round( hor_df[index],1)

                        
                        for index2 in quot_df.columns:
                            for comp in cases:
                                if index2.find(comp)!=-1:       
                                    quot_df[index2]*=0.1
                                    quot_df[index2]= round(quot_df[index2],1)
    
                        return quot_df,hor_df