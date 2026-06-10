#App to convert .FIT files to .csv

#Libraries
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import *

import time
import csv
import os
import fitparse
import pytz

#Initial values
original_fields = ['timestamp','position_lat','position_long', 'distance',
'enhanced_altitude', 'altitude','enhanced_speed',
                 'speed', 'heart_rate','temperature','cadence','fractional_cadence','power','vertical_oscillation',
                 'activity_type','step_length','sport']

required_fields = ['timestamp']

allowed_fields = ['timestamp']

UTC = pytz.UTC
CST = pytz.timezone('US/Pacific')

#
root = tk.Tk()
root.title("FIT To CSV file converter")
root.iconbitmap("C:/Users/Alfonso Vecino/Documents/CODING/FIT_To_CSV/icons/icon.ico")

# Center window when opening -----------------------------------------------------
#  Obtaining the lenght and width of the current window
wtotal = root.winfo_screenwidth()
htotal = root.winfo_screenheight()
#  Defining the window app size
wventana = 600
hventana = 370
#  Calculate where to place the window
pwidth = round(wtotal/2-wventana/2)
pheight = round(htotal/2-hventana/2)
#  Applying the properties to the window's geometry
root.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
# ---------------------------------------------------------------------------------


#Creating the Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#File cascade
menu_archivo = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=menu_archivo)

#int for counting the executions of the program
ejecuciones = 0

#Configurate window
def configure():
    
    global ventana_config
    global ejecuciones
    global allowed_fields
    global original_fields

    ventana_config = tk.Toplevel()
    ventana_config.title("Field selector")
    ventana_config.iconbitmap("C:/Users/Alfonso Vecino/Documents/CODING/FIT_To_CSV/icons/icon.ico")
    # Center window when opening -----------------------------------------------------
    #  obtaining the lenght and width of the current window
    wtotal = ventana_config.winfo_screenwidth()
    htotal = ventana_config.winfo_screenheight()
    #  Defining the window app size
    wventana = 425
    hventana = 500
    #  Calculate where to place the window
    pwidth = round(wtotal/2-wventana/2)
    pheight = round(htotal/2-hventana/2)
    #  Applying the properties to the window's geometry
    ventana_config.geometry(str(wventana)+"x"+str(hventana)+"+"+str(pwidth)+"+"+str(pheight))
    # --------------------------------------------------------------------------------

    #Definition of main list
    lista_ppal = tk.Listbox(ventana_config)
    lista_ppal.place(x=20,y=35,width=150, height=370)
    j=0
    for i in original_fields:
        lista_ppal.insert(j,i)
        j=j+1
    listado_ppal=lista_ppal.get(0,tk.END)

    #Main label
    titulo_ppal = tk.Label(ventana_config, text="Variables to choose")
    titulo_ppal.place(x=20, y=10)

    #Definition of secondary list
    lista_sec = tk.Listbox(ventana_config)
    lista_sec.place(x=250,y=35,width=150, height=370)

    if ejecuciones==0:
        allowed_fields = ["timestamp"]
        lista_sec.delete(0,END)
        lista_sec.insert(0,"timestamp")

    if ejecuciones>0:

        j=0
        for i in allowed_fields:  
            lista_sec.insert(j,i)
            j=j+1

    #Secondary label
    titulo_sec = tk.Label(ventana_config, text="Selected Variables")
    titulo_sec.place(x=250, y=10)

    #Adding new variables
    def agregar_variable():
        
        indicador="No"
        seleccion=""
        listado_sec = lista_sec.get(0,tk.END)

        for item in lista_ppal.curselection():
            seleccion = lista_ppal.get(item)

        if seleccion=="":
            ventana_config.grab_set()
            messagebox.showinfo(title="Invalid Selection!", message="No variable selected to add.")
            
        for x in listado_sec:
            if x==seleccion:
                indicador="Yes"

        if indicador=="No":
            lista_sec.insert(tk.END,seleccion)

    def quitar_variable():
        
        seleccion=""

        for item in lista_sec.curselection():
            seleccion = lista_sec.get(item)

        if seleccion=="":
            ventana_config.grab_set()
            messagebox.showinfo(title="Invalid Selection!", message="No variable selected to be deleted.")
            return

        if seleccion=="timestamp":
            ventana_config.grab_set()
            messagebox.showinfo(title="Invalid Selection!", message="This variable cannot be removed!")
            return

        for item in lista_sec.curselection():
            lista_sec.delete(item)

    def aceptar_cambios():
        
        global ejecuciones
        global allowed_fields
        contador=0
        listado_sec = lista_sec.get(0,tk.END)
        contador = len(listado_sec) + 1

        if contador==1:
            ventana_config.grab_set()
            messagebox.showinfo(title="Error!",message="There is no variable selected.")
        
        ventana_config.grab_set()
        answer = messagebox.askyesno(title="Do you want to save?", message="The program has detected " + str(contador-1) + " variables, would you like to continue?")

        if answer==True:
            allowed_fields = lista_sec.get(0,tk.END)
            ejecuciones = ejecuciones + 1
            ventana_config.withdraw()
            root.grab_set()

    def agregar_personalizado():
        
        global original_fields
        global ventana_custom
        global listado_ppal

        ventana_custom = tk.Toplevel()
        ventana_custom.title("Add Field")
        ventana_custom.geometry("300x100")
        ventana_custom.iconbitmap("C:/Users/Alfonso Vecino/Documents/CODING/FIT_To_CSV/icons/icon.ico")

        texto = tk.Text(ventana_custom, height=2, width=30)
        texto.pack(ipady=10)
        
        #Add field button

        def ingresar():
            
            global original_fields
            global listado_ppal

            nuevo = texto.get(1.0,END)
            repetido = "no"
            for item in original_fields:
                if item==nuevo:
                    repetido="yes"
            if repetido=="yes":
                messagebox.showinfo(title="Error!",message="The variable is already selected.")
                pass
            if repetido=="no":
                original_fields.append(nuevo)
                ventana_custom.withdraw()
                ventana_config.withdraw()
                configure()

        boton_ingresar = tk.Button(ventana_custom, text="Accept", command=ingresar)
        boton_ingresar.pack(pady=5)

    def eliminar_personalizado():

        global original_fields

        seleccion=""

        for item in lista_ppal.curselection():
            seleccion = lista_ppal.get(item)

        if seleccion=="":
            ventana_config.grab_set()
            messagebox.showinfo(title="Invalid selection!", message="You haven't selected any variable to delete.")
            return

        if seleccion=="timestamp":
            ventana_config.grab_set()
            messagebox.showinfo(title="Invalid selection!", message="This variable cannot be deleted!")
            return

        answer = messagebox.askyesno(title="Would you like to delete this variable?", message="The field  " + seleccion + " will be deleted, would you like to continue?")

        if answer==True:

            for item in lista_ppal.curselection():
                lista_ppal.delete(item)

            original_fields.remove(seleccion)
            
        if answer==False:
            messagebox.showinfo(title="Elimination aborted", message="This variable will not be deleted.")
            return

    def cerrar_config():
        global ventana_config
        ventana_config.withdraw()

    boton_agregar = tk.Button(ventana_config,text=" > ",command=agregar_variable)
    boton_agregar.place(x=195,y=200)

    boton_quitar = tk.Button(ventana_config,text=" < ",command=quitar_variable)
    boton_quitar.place(x=195,y=240)

    boton_custom = tk.Button(ventana_config,text="New",command=agregar_personalizado)
    boton_custom.place(x=20,y=420)

    boton_eliminar = tk.Button(ventana_config,text="Delete",command=eliminar_personalizado)
    boton_eliminar.place(x=75,y=420)

    boton_guardar = tk.Button(ventana_config,text="Save",command=aceptar_cambios)
    boton_guardar.place(x=250,y=420)

    btn_cerrar = tk.Button(ventana_config, text="Close", command=cerrar_config)
    btn_cerrar.place(x=310,y=420)


menu_archivo.add_command(label="Configure", command=configure)
menu_archivo.add_separator()
menu_archivo.add_command(label="Close", command=root.quit)


#Main window headers:

titulo = tk.Label(root, text="FIT TO CSV CONVERTER", font=('Arial', 10)).pack(pady=3)
titulo2 = tk.Label(root, text="By Alfonso Vecino - 2025", font=('Arial', 10)).pack()

file_name = tk.Label(root, text="Select a file.", font=('Arial', 10))
file_name.place(x=50,y=110)

lista_archivos = tk.Listbox(root)
lista_archivos.place(x=20,y=150,width=560, height=170)


#Browse multiple files button

def browse_file():

    #Read selected file(s)
    pathfile = fd.askopenfilename(initialdir="C:/", filetypes=(("FIT Files", "*.fit"),("All Files", "*.*")), multiple=True)
    
    #Saving the paths into a list
    var = root.tk.splitlist(pathfile)
    rutas_archivos = []
    for f in var:
        rutas_archivos.append(f)

    #Filling up the list with data collected
    j=0
    for f in rutas_archivos:
        lista_archivos.insert(j,f)
        j+=1

    #Validates that at leat 1 file has been selected
    if pathfile=='':
        file_name.config(text ="Select a file.")
    if pathfile!='':
        file_name.config(text ="The following files were detected")

btn_pick_file = tk.Button(root,text="...",command=browse_file)
btn_pick_file.place(x=20,y=110)

#Clear list button

def borrar_lista():
    
    lista_archivos.delete(0,tk.END)

btn_clear_list = tk.Button(root, text="Clear list", command=borrar_lista)
btn_clear_list.place(x=210,y=70)

#Run button

def ejecutar_csv():

    inicio=time.time()

    listado = []
    listado = lista_archivos.get(0,tk.END)

    def main():

        #Writing one single file with all data
        if checkbox_value.get() == True:
            
            new_filename = os.path.dirname(listado[0]) + "/Total_FIT_Converted.csv"
            #If the file already exists, it is deleted and a new one is created
            if os.path.exists(new_filename):
                os.remove(new_filename)

            #Writing the header of the single file and entering each file to extrac the information
            with open(new_filename, 'w', newline='') as f:
                writer = csv.writer(f)
                #write the headers
                source_file = ("source_file",)
                writer.writerow(allowed_fields + source_file)

                for file in listado:
                    fitfile = fitparse.FitFile(file,data_processor=fitparse.StandardUnitsDataProcessor())
                    write_onefile_to_csv(fitfile, new_filename, file, f)

        #Writing individual files
        else:

            for file in listado:
                new_filename = file[:-4] + '.csv'

                #If the file already exists, it is deleted and a new one is created
                if os.path.exists(new_filename):
                    os.remove(new_filename)
                
                fitfile = fitparse.FitFile(file,data_processor=fitparse.StandardUnitsDataProcessor())
                write_fitfile_to_csv(fitfile, new_filename)

    #Function to write individual files
    def write_fitfile_to_csv(fitfile, output_file='test_output.csv'):
        messages = fitfile.messages
        #raw data in messages in one line
        data = []
        for m in messages:
            skip=False
            if not hasattr(m, 'fields'):
                continue
            fields = m.fields

            #check for important data types
            mdata = {}
            for field in fields:
                #print(field) print varaibles
                if field.name in allowed_fields:
                    if field.name=='timestamp':
                        mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                    else:
                        mdata[field.name] = field.value    
            for rf in required_fields:
                if rf not in mdata:
                    skip=True
                
            if not skip:
                data.append(mdata) 

        #writing the csv file
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            #write the headers
            writer.writerow(allowed_fields)
            #If the user selected the variable heart_rate, the app will only write rows with HR values different from 0
            try:
                index_hr = allowed_fields.index("heart_rate")   #Reading the index of HR
            except ValueError:
                index_hr=-1
            #write the data
            for entry in data:

                line_file=[]
                #Collecting data in a list
                for k in allowed_fields:
                    data_var= str(entry.get(k,""))
                    line_file.append(data_var)

                if index_hr >= 0:
                    if line_file[index_hr]!= "":
                        writer.writerow(line_file)
                else:
                    writer.writerow(line_file)

        #Printing the status           
        #print('wrote %s' % output_file)


    #Function to write one single file
    def write_onefile_to_csv(fitfile, output_file='test_output.csv', filepath="file.csv", f=0):
        messages = fitfile.messages
        #raw data in messages in one line
        data = []
        for m in messages:
            skip=False
            if not hasattr(m, 'fields'):
                continue
            fields = m.fields

            #check for important data types
            mdata = {}
            for field in fields:
                #print(field) print varaibles
                if field.name in allowed_fields:
                    if field.name=='timestamp':
                        mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                    else:
                        mdata[field.name] = field.value    
            for rf in required_fields:
                if rf not in mdata:
                    skip=True
                
            if not skip:
                data.append(mdata) 

        #writing the csv file
        writer = csv.writer(f)
        #If the user selected the variable heart_rate, the app will only write rows with HR values different from 0
        try:
            index_hr = allowed_fields.index("heart_rate")   #Reading the index of HR
        except ValueError:
            index_hr=-1
        #write the data
        for entry in data:

            line_file=[]
            #Collecting data in a list
            for k in allowed_fields:
                data_var= str(entry.get(k,""))
                line_file.append(data_var)

            #Adding the column of the file name
            line_file.append(os.path.basename(filepath[:-4]))

            if index_hr >= 0:
                if line_file[index_hr]!= "":
                    writer.writerow(line_file)
            else:
                writer.writerow(line_file)

        #Printing the status           
        #print('wrote %s' % output_file)

 
    if __name__=='__main__':
        main()

    fin=time.time()
    tiempo_total=str(round(fin-inicio,2))
    messagebox.showinfo("Execution completed","Finished!, Execution time: " + tiempo_total + " seconds.")

btn_execute = tk.Button(root, text="Run", command=ejecutar_csv)
btn_execute.place(x=272,y=70)

#Configure button

btn_configure = tk.Button(root, text="Configurate", command=configure)
btn_configure.place(x=310,y=70)

#Checkbox to run a single file
checkbox_value = tk.BooleanVar()
checkbox = tk.Checkbutton(text="Single file",variable=checkbox_value)
checkbox.place(x=390, y=70)

root.mainloop()