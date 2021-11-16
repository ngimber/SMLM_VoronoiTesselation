from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import IntVar
from matplotlib.path import Path
from os import path

from pycobra.cobra import Cobra
from pycobra.visualisation import Visualisation
from pycobra.diagnostics import Diagnostics
from sklearn import cluster
from pycobra.visualisation import voronoi_finite_polygons_2d
from scipy.spatial import Voronoi, voronoi_plot_2d

from joblib import Parallel, delayed


global relativeThreshold





###############get Files
root = Tk()
root.attributes("-topmost", True)
PathList = askopenfilenames(filetypes=(("CSV", "*.csv"),("grouped_out.txt", "*grouped_out.txt"),("pairs_out.txt", "*pairs_out.txt"),
                                           ("All files", "*.*") ))
root.destroy()


files=[]
for thisfile in PathList:
    folder, file = path.split(thisfile)
    files=files+[file]
    
path=folder




###############get Parameters
def getParameters():

    
    def saveParameters():
        
        
    
        global relativeThreshold
        relativeThreshold=e1.get()
        global njobs
        njobs=e2.get()

        master.destroy()

        
    
    master = Tk()
    master.title("tesseler for ThunderSTORM")
    Label(master, text="Relative Threshold           ").grid(row=0, column=0,sticky=W)
    Label(master, text="Number of Parallel Jobs           ").grid(row=1, column=0,sticky=W)

    Label(master, text="niclas.gimber@charite.de ").grid(row=0, column=5,columnspan=1000)
    
    v = IntVar()
    v.set(1)
    e1 = Entry(master, text=v)
    e1.grid(row=0, column=2)
    
    v = IntVar()
    v.set(4)
    e2 = Entry(master, text=v)
    e2.grid(row=1, column=2)
    
    

    
    Label(master, text=" ").grid(row=5, column=0,sticky=W)
    Button(master, text='Go',fg="green",bg="gray83", command=saveParameters).grid(row=1, column=4)
    #master.attributes("-fullscreen", True)
    master.attributes("-topmost", True)

    
    mainloop()
 
getParameters()
relativeThreshold=float(relativeThreshold)
njobs=int(njobs)

print(str(njobs)+" files are being processed")

# ##############################################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import math
import csv

from sklearn import metrics
#from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
#from scipy.misc import imsave




folder=path+"\\"



# ##############################################################

#for u in range (0,len(files)):
def doTheJob(u):
    try:

        # ##############################################################
        print(str(len(files))+" files to process")
        print(files[u])
        print("no " + str(u))
        if (file.endswith(".txt")):
            sample=pd.read_table(folder+files[u],header=None, skiprows=1,sep=" ")
            headers=["x short [nm]","y short [nm]", "I short", "frame","x long [nm]","y long [nm]", "I long"]
            sample.columns=headers
            
            with open(folder+file, newline='') as f:
                reader = csv.reader(f)
                row1 = next(reader)  # gets the first line
            row1
            
            
        else:
            sample=pd.read_csv(folder+files[u], sep=",")
    
    
        # #############################################################################
        
        
        global points
        
        if (file.endswith(".txt")):
            points = sample[['x short [nm]',"y short [nm]"]].values.astype(np.float)
        
        else:
            points = sample[['x [nm]',"y [nm]"]].values.astype(np.float)
        labels_true=points.T[0].astype(int)
        
        def PolygonArea(corners):
            n = len(corners) # of corners
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += corners[i][0] * corners[j][1]
                area -= corners[j][0] * corners[i][1]
            area = abs(area) / 2.0
            return area
        
        
        #calculate voronoi
   
        vor = Voronoi(points)
        regions, vertices = voronoi_finite_polygons_2d(vor)
        
        #calculate areas
        global polygonAreas
        polygonAreas=[]
    
        for region in regions:
            polygon = vertices[region]
            area=PolygonArea(vertices[region])
            polygonAreas=polygonAreas+[area] 
    
        # ##############################################################
            
        #generate analogous array 
        newPath=folder+"tesseler\\"
        if (os.path.exists(newPath)==False):
            os.makedirs(newPath)
    
    
        print("export csv")
        #export to ThunderSTORM        
        Thundertesseler=sample
        sample["tesselation_area"]=polygonAreas
        
        
        
        
    
        
        newPath=folder+"tesseler_clustersOnly\\"
        if (os.path.exists(newPath)==False):
            os.makedirs(newPath)
        
        if (file.endswith(".txt")):
            
            np.savetxt(folder+"tesseler\\Thunder_tesseler_relativeThreshold"+str(relativeThreshold)+"_"+files[u],Thundertesseler.values,comments="" ,header=row1[0],fmt='%f') 
            
            Thundertesseler.to_csv(folder+"tesseler\\Thunder_tesseler_relativeThreshold"+str(relativeThreshold)+"_"+files[u],sep=',',index=False)
            
            table=Thundertesseler[Thundertesseler["tesselation_area"]<(np.median(polygonAreas)/relativeThreshold)]
            np.savetxt(folder+"tesseler_clustersOnly\\Thunder_tesseler_relativeThreshold"+str(relativeThreshold)+"_"+files[u],table.values,comments="" ,header=row1[0],fmt='%f')    
                
        else:
            
            Thundertesseler.to_csv(folder+"tesseler\\Thunder_tesseler_relativeThreshold"+str(relativeThreshold)+"_"+files[u],sep=',',index=False)
            
            Thundertesseler[Thundertesseler["tesselation_area"]<(np.median(polygonAreas)/relativeThreshold)].to_csv(folder+"tesseler_clustersOnly\\Thunder_tesseler_relativeThreshold"+str(relativeThreshold)+"_"+files[u],sep=',',index=False)
        
    except:
        print("error in file "+files[u]) 


#Parallel(n_jobs=-1, backend="loky")(map(delayed(doTheJob), range(0,len(files))))
Parallel(n_jobs=njobs, backend="loky")(delayed(doTheJob)(u) for u in range(0,len(files)))


        