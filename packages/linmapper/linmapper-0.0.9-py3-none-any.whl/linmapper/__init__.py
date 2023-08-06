import numpy as np
import math


def linmapper(Z, fZ):
    
    count = 0
    while count <= len(fZ):


        mean_Z = Z.mean()
        mean_fZ = fZ.mean()

        fZ_origin = fZ - mean_fZ
        Z_origin = Z - mean_Z
        
        theta_con =[]
        M_con = []    
        for i in range (0, len(Z)):
            
            dot_product = (Z_origin[i]*np.conj(fZ_origin[i]))
            mag_Z = np.linalg.norm(Z_origin[i])
            mag_fZ = np.linalg.norm(fZ_origin[i])
            rotation = np.degrees(np.real(np.arccos(dot_product/(mag_Z * mag_fZ ))))
            theta_con.append(rotation)
            
            Magnification = fZ_origin[i] * np.exp(-1j*rotation) / Z_origin[i]
            M_con.append(np.abs(Magnification))
            
        if np.allclose(theta_con, theta_con[0]):

            Z_origin_check = np.round(((fZ_origin * np.exp(-1j*theta_con[0]))/Magnification),3)

            if all(Z_origin[i] == Z_origin_check[i] for i in range(0, len(Z_origin))):


                rotated_mean_Z = np.round(((mean_Z * M_con[0])* np.exp(1j*math.radians(theta_con[0]))),3)

                translation_x =  np.real(mean_fZ) - np.real(rotated_mean_Z)
                translation_y =  np.imag(mean_fZ) - np.imag(rotated_mean_Z)

                exp = np.round((np.exp(1j*math.radians(theta_con[0]))),3)


                print ("Rotation(θ)      : ", np.round(theta_con[0]), "deg\nMagnification(M) : ", np.round(M_con[0]), "X\nTranslation      : ", translation_x, "(Real axis), ", translation_y, "(imag axis)")
                print ("\nfunc(Z) = ", exp*np.round(M_con[0]), "Z + (", translation_x, ") + (", translation_y, "j)")

                print ("\n\n-------------- additional information --------------")
                print ("\nind.\tvertices(Z-plane)\tvertices(f(Z)-plane)")
                for p in range (0, len(Z)):
                    print (f"{p}\t{Z[p]}\t          •---•\t{fZ[p]}")
                break            
            else:
                fZ = np.roll(fZ, 1)
        else:
            print ("The Shapes are different in the Z-plane and f(Z)-plane!")
            break

        count +=1
            
    

    




    

        




