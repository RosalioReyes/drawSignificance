
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import numpy as np


def getWhisker(array):
    q3 = np.quantile(array, 0.75)
    q1 = np.quantile(array, 0.25)
    iqr = q3 - q1
    upper_whisker = array[array <= q3 + 1.5*iqr].max()
    lower_whisker = array[array >= q1 - 1.5*iqr].min()
    return upper_whisker, lower_whisker

def decimal_factor(x, xformat = "0.20f"):
    str_x = format(x, xformat)
    pto = str_x.find(".")
    num = "0."
    for i in range(pto + 1, len(str_x)):
        if str_x[i] == "0":
            num = num + "0"
        else:
            num = num + "1"
            break
    return float(num)

def make_statisticalProof(array1, array2, equalVar = False):
    std_array1, pval_array1 = shapiro(array1)
    print("Estadístico array1 = ", std_array1,  "p_value_array1 = ", pval_array1)
    if(pval_array1 < 0.05):
        print("Los valores de array1 no tienen una distribución normal")
        v1 = 1
    else:
        print("Los valores de array1 sí tienen una distribución normal")
        v1 = 0
        
    std_array2, pval_array2 = shapiro(array2)
    print("Estadístico array2 = ", std_array2,  "p_value_array2 = ", pval_array2)
    if(pval_array2 < 0.05):
        print("Los valores de array2 no tienen una distribución normal")
        v2 = 1
    else:
        print("Los valores de array2 sí tienen una distribución normal")
        v2 = 0 
    print("suma de vs : ",v1 + v2)
    # ambos tienen distribución normal (v1 + v2 == 0) --> ttest
    # alguno de ellos no tiene distribución normal --> prueba paramétrica mannwhitneyu
    p = False
    st = False
    if (v1 + v2 == 0):
        print(" se hace una prueba ttest")
        st, p = ttest_ind(a = array1, b = array2, equal_var=equalVar)
    else:
        st, p = mannwhitneyu(array1, array2)
    print("statistic = ",  st, "p = ", p) 
    return p


def draw_significance(array1, array2, position_array1, position_array2, position = "up", factor = 1 , equalVar = False, fliers = False):
    unit = factor * decimal_factor((np.mean(array1) + np.mean(array2))/2)
    if position == "up":
        if fliers == False:
            begin_line1 = unit/3 + getWhisker(array1)[0]
            begin_line2 = unit/3 + getWhisker(array2)[0]
            hline = np.max([begin_line1, begin_line2]) + unit  # horizontal line

            #draw lines
            #horizontal line
            plt.plot([position_array1, position_array2], [hline, hline], c = "k")
            #left vertical line
            plt.plot([position_array1, position_array1], [begin_line1, hline], c = "k")
            # rigth vertical line
            plt.plot([position_array2, position_array2], [begin_line2, hline], c = "k")
            
            # write text
            p = make_statisticalProof(array1, array2, equalVar)
            if p >= 0.0001:
                plt.text(position_array1, hline + unit/5, "p=" + str(round(p,4)))
            else:
                pST = "{:.2e}".format(p)
                plt.text(position_array1, hline + unit/5, "p=" + str(pST))
            
        if fliers == True:
            False
            
    if position == "down":
        False
        
    return


### OJO: algunas estadísticas creo que dan cero por el formato de
### número. Por ejemplo, si la p = 1x10e-100, el formato lo 
### lo leerá como 0.00000000... (con vente ceros, pero no alcanza)
### a detectar el cambio de formmato