import numpy as np
import tkinter as tk
from tkinter import ttk
import math
from tkinter import messagebox
from classes import Structure, Element, Coordinate, Support, Load
from tkinter import *
import pathlib, os
from PIL import ImageTk, Image

np.set_printoptions(6, suppress= True)

# -----------------------------------------------------------------------------------------------------------------------

def select_structure(struct):
  root = tk.Toplevel(master)
  root.geometry("1280x720")
  root.resizable(False, False)
  if struct == "truss_s":
    sstructure = Structure("Truss")
    root.title("Truss Structure Analyzer")
  elif struct == "beam_s":
    sstructure = Structure("Beam")
    root.title("Beam Structure Analyzer")
  elif struct == "frame_s":
    sstructure = Structure("Frame")
    root.title("Frame Structure Analyzer")
  elif struct == "grid_s":
    sstructure = Structure("Grid")
    root.title("Grid Structure Analyzer")

  print (sstructure.structureType)
  structure = ttk.Frame(root)
  structure.grid(row=0, column=0, sticky="NSEW")


  def only_integer(char):
    return char.isdigit()

  def only_float(char):
    try:
      float(char)
      return True
    except ValueError:
      if char == ".": return True
      if char == "-": return True
      return False
    
  validation_int = structure.register(only_integer)
  validation_float = structure.register(only_float)

  container1 = tk.Frame(structure, height=715, width=270)
  container1.grid(row=0, column=0, rowspan=3, sticky="wsn")
  canvas1 = tk.Canvas(container1, height=714, width=240)
  canvas1.grid(row=0, column=0)
  input_frame = tk.LabelFrame(canvas1, text="Input Parameter", fg="green", labelanchor="n", height=715, width=240, bg="#C7DAEA")
  input_frame.grid(row=0, column=0)
  input_frame.configure(height=input_frame["height"],width=input_frame["width"])
  input_frame.grid_propagate(0)
  v_scrollbar1 = tk.Scrollbar(container1, orient='vertical', command=canvas1.yview)
  v_scrollbar1.grid (row=0, column=1, sticky='sn')
  canvas1.create_window((0, 0), width=240, height=50000, window=input_frame, anchor="n")
  input_frame.bind('<Configure>', lambda e: canvas1.configure(scrollregion=canvas1.bbox('all')))
  canvas1.configure(yscrollcommand=v_scrollbar1.set)
   

  section_title1 = tk.Frame(input_frame)
  section_title1.grid(row=0, column=0, columnspan=3)

  dof = []
  noe_label = tk.Label(section_title1, text="Number of Element(s)")
  noe_label.grid(row=0, column=0, padx=(5, 5), pady=(2, 2), sticky="W")
  noe_input = tk.Entry(section_title1, validate="key", validatecommand=(validation_int, '%S'), width=12, borderwidth=2 , justify="center")
  noe_input.grid(row=0, column=1, padx=(0, 5), pady=(2, 2), sticky="W")
  noe_input.focus()
  dof.append(noe_input)

  non_label = tk.Label(section_title1, text="Number of Node(s)")
  non_label.grid(row=1, column=0, padx=(5, 5), pady=(2, 2), sticky="W")
  non_input = tk.Entry(section_title1, validate="key", validatecommand=(validation_int, '%S'), width=12, borderwidth=2, justify="center")
  non_input.grid(row=1, column=1, padx=(0, 5), pady=(2, 2), sticky="W")
  dof.append(non_input)

  next_button = tk.Button(section_title1, text="Next", command=lambda:prsbtn("button1"))
  next_button.grid(row=2, column=0, columnspan=3, padx=2, pady=2, sticky="NSEW")

  canvas_frame = tk.LabelFrame(structure, text="Free Body Diagram", height=425, width=1015, labelanchor="n")
  canvas_frame.grid(row=0, column=2, sticky="ne")
  canvas_frame.configure(height= canvas_frame["height"],width= canvas_frame["width"])
  canvas_frame.grid_propagate(0)

  FBD = tk.Canvas(canvas_frame, bg="white", height=400, width=1005)
  FBD.grid(row=0, column=0, sticky="nsew")
  FBD.grid_propagate(0)
  FBD.configure(scrollregion=(-500, -200, 500, 200))
  for i in range(101):
    grid_y = FBD.create_line(-500+(i*10), -200, -500+(i*10), 200, fill="#ECF4D6")
    grid_x = FBD.create_line(-500, -200+(i*10), 500, -200+(i*10), fill="#ECF4D6")
    FBD.tag_lower(grid_y)
    FBD.tag_lower(grid_x)
  if sstructure.structureType == "Grid":
    FBD.create_line(-460, 160, -420, 160, width=1, fill="black", arrow="last")
    FBD.create_line(-460, 160, -484, 184, width=1, fill="black", arrow="last")
    FBD.create_text(-415, 160, text="x")
    FBD.create_text(-488, 188, text="z")
      
  else:
    FBD.create_line(-480, 180, -440, 180, width=1, fill="black", arrow="last")
    FBD.create_line(-480, 180, -480, 140, width=1, fill="black", arrow="last")
    FBD.create_text(-435, 180, text="x")
    FBD.create_text(-480, 130, text="y")

  FBD.create_text(400, 170, text="pre loading", fill="#4F6F52", font="Aereal 6 bold")
  FBD.create_line(430, 170, 488, 170, width=1, fill="#4F6F52")

  FBD.create_text(400, 190, text="post loading", fill="#FF9130", font="Aereal 6 bold")
  FBD.create_line(430, 190, 490, 190, width=1, fill="#FF9130", dash=(2,5))
  



  container2 = tk.Frame(structure, height=260, width=1025)
  container2.grid(row=1, column=2, sticky="ne")
  canvas2 = tk.Canvas(container2, height=260, width=995)
  canvas2.grid(row=0, column=0)
  output_frame = tk.LabelFrame(canvas2, text="Output Parameter", fg="maroon", labelanchor="n", height=260, width=995, bg="#EEE783")
  output_frame.grid(row=0, column=0)
  output_frame.configure(height=output_frame["height"],width=output_frame["width"])
  output_frame.grid_propagate(0)
  v_scrollbar2 = tk.Scrollbar(container2, orient='vertical', command=canvas2.yview)
  v_scrollbar2.grid (row=0, column=1, sticky='sn')
  canvas2.create_window((0, 0), width=995, height=10000, window=output_frame, anchor="n")
  output_frame.bind('<Configure>', lambda e: canvas2.configure(scrollregion=canvas2.bbox('all')))
  canvas2.configure(yscrollcommand=v_scrollbar2.set) 
  
  disp_frame = tk.LabelFrame(output_frame, text="Displacement", labelanchor="n", borderwidth=4, bg="#7743DB", fg="white")
  disp_frame.grid(row=0, column=0, sticky="wen")
  var_head = tk.Label(disp_frame, text="Variable", width=34, bg="#7743DB", fg="white")
  var_head.grid(row=0, column=0, sticky="we")
  val_head = tk.Label(disp_frame, text="Value", width=34, bg="#7743DB", fg="white")
  val_head.grid(row=0, column=1, sticky="we")

  ss_frame = tk.LabelFrame(output_frame, text="Stress & Strain", labelanchor="n", borderwidth=4, bg="#2D9596", fg="white")
  ss_frame.grid(row=0, column=1, sticky="wen")
  output_element_head = tk.Label(ss_frame, text="Element", width=22, bg="#2D9596", fg="white")
  output_element_head.grid(row=0, column=0, sticky="we")
  stress_head = tk.Label(ss_frame, text="Stress (Pa)", width=22, bg="#2D9596", fg="white")
  stress_head.grid(row=0, column=1, sticky="we")
  strain_head = tk.Label(ss_frame, text="Strain", width=22, bg="#2D9596", fg="white")
  strain_head.grid(row=0, column=2, sticky="we")

  def uc_window():
    def reset():  
      # using the delete() method to delete entries in entry field  
      input_field.delete(0, END)  
      output_field.delete(0, END)  
      # setting the value of the option menu to the  
      # first index of the list using the set() method  
      input_value.set(SELECTIONS[0])  
      output_value.set(SELECTIONS[0])  
    
      # setting the focus to input field using the focus_set() method  
      input_field.focus_set() 
    
    def convert():  
      # getting the string from entry field and converting it into float  
      inputVal = float(input_field.get())  
      # getting the values from selection menus  
      input_unit = input_value.get()  
      output_unit = output_value.get()  
    
      # list of the required combination of the conversion factors  
      conversion_factors = [input_unit in length_units and output_unit in length_units,  
      input_unit in weight_units and output_unit in weight_units,  
      input_unit in temperature_units and output_unit in temperature_units,  
      input_unit in area_units and output_unit in area_units,  
      input_unit in volume_units and output_unit in volume_units]  
    
      if any(conversion_factors): # If both the units are of same type, perform the conversion  
        if input_unit == "celsius" and output_unit == "fahrenheit":  
            output_field.delete(0, END)  
            output_field.insert(0, (inputVal * 1.8) + 32)  
        elif input_unit == "fahrenheit" and output_unit == "celsius":  
            output_field.delete(0, END)  
            output_field.insert(0, (inputVal - 32) * (5/9))  
        else:  
            output_field.delete(0, END)  
            output_field.insert(0, round(inputVal * unitDict[input_unit] / unitDict[output_unit], 5))  
    
      else:  
          # displaying error if units are of different types  
          output_field.delete(0, END)  
          output_field.insert(0, "ERROR")  

    if __name__ == "__main__":  
      # dictionary of conversion factors  
      unitDict = {  
        "millimeter" : 0.001,  
        "centimeter" : 0.01,  
        "meter" : 1.0,  
        "kilometer" : 1000.0,  
        "foot" : 0.3048,  
        "mile" : 1609.344,  
        "yard" : 0.9144,  
        "inch" : 0.0254,  
        "square meter" : 1.0,  
        "square kilometer" : 1000000.0,  
        "square centimeter" : 0.0001,  
        "square millimeter" : 0.000001,  
        "are" : 100.0,  
        "hectare" : 10000.0,  
        "acre" : 4046.856,  
        "square mile" : 2590000.0,  
        "square foot" : 0.0929,  
        "cubic meter" : 1000.0,  
        "cubic centimeter" : 0.001,  
        "litre" :  1.0,  
        "millilitre" : 0.001,  
        "gallon" : 3.785,  
        "gram" : 1.0,  
        "kilogram" : 1000.0,  
        "milligram" : 0.001,  
        "quintal" : 100000.0,  
        "ton" : 1000000.0,  
        "pound" : 453.592,  
        "ounce" : 28.3495  
      }  
  
      # charts for units conversion  
      length_units = [  
        "millimeter", "centimeter", "meter", "kilometer", "foot", "mile", "yard", "inch"  
      ]  
      temperature_units = [  
        "celsius", "fahrenheit"  
      ]  
      area_units = [  
        "square meter", "square kilometer", "square centimeter", "square millimeter",  
        "are", "hectare", "acre", "square mile", "square foot"  
      ]  
      volume_units = [  
        "cubic meter", "cubic centimeter", "litre", "millilitre", "gallon"     
      ]  
      weight_units = [  
        "gram", "kilogram", "milligram", "quintal", "ton", "pound", "ounce"  
      ]  
  
      # creating the list of options for selection menu  
      SELECTIONS = [  
        "Select Unit",  
        "millimeter",  
        "centimeter",  
        "meter",  
        "kilometer",  
        "foot",  
        "mile",  
        "yard",  
        "inch",  
        "celsius",  
        "fahrenheit"  
        "square meter",  
        "square kilometer",  
        "square centimeter",  
        "square millimeter",  
        "are",  
        "hectare",  
        "acre",  
        "square mile",  
        "square foot"  
        "cubic meter",  
        "cubic centimeter",  
        "litre",  
        "millilitre",  
        "gallon"     
        "gram",  
        "kilogram",  
        "milligram",  
        "quintal",  
        "ton",  
        "pound",  
        "ounce"  
      ]  

      guiWindow = tk.Toplevel(root)
      # setting the title of the main window  
      guiWindow.title("Unit Converter")  
      # setting the size and position of the main window  
      guiWindow.geometry("450x300")  
      # disabling the resizing option  
      guiWindow.resizable(0, 0)  
      # setting the background color to #16a085  
      guiWindow.configure(bg = "#16a085")  
    
      # adding frames to the main window  
      header_frame = tk.Frame(guiWindow, bg = "#16a085")  
      body_frame = tk.Frame(guiWindow, bg = "#16a085")  
    
      # setting the positions of the frames  
      header_frame.pack(expand = True, fill = "both")  
      body_frame.pack(expand = True, fill = "both")  
    
      # adding the label to the header frame   
      header_label = tk.Label(  
          header_frame,  
          text = "UNIT CONVERTER",  
          font = ("arial black", 16),  
          bg = "#16a085",  
          fg = "#e8f6f3"  
      )  
    
      # setting the position of the label  
      header_label.pack(expand = True, fill = "both")  
    
      # creating the objects of the StringVar() class  
      input_value = StringVar()  
      output_value = StringVar()  
      # using the set() method to set the primary  
      # value of the objects to index value 0  
      # of the SELECTIONS list  
      input_value.set(SELECTIONS[0])  
      output_value.set(SELECTIONS[0])  
    
      # creating the labels for the body of the main window  
      input_label = tk.Label(  
          body_frame,  
          text = "From:",  
          bg = "#16a085",  
          fg = "#d0ece7"  
      )  
      output_label = tk.Label(  
          body_frame,  
          text = "To:",  
          bg = "#16a085",  
          fg = "#d0ece7"  
      )  
    
      # using the grid() method to set the position of the above labels   
      input_label.grid(row = 1, column = 1, padx = 50, pady = 20, sticky = W)  
      output_label.grid(row = 2, column = 1, padx = 50, pady = 20, sticky = W)  
    
      # creating the entry fields for the body of the main window  
      # input field to enter data  
      input_field = tk.Entry(  
          body_frame,  
          bg = "#e8f8f5"  
      )  
      # output field to display result  
      output_field = tk.Entry(  
          body_frame,  
          bg = "#e8f8f5"  
      )  
    
      # using the grid() method to set the position of the above entry fields   
      input_field.grid(row = 1, column = 2)  
      output_field.grid(row = 2, column = 2)  
    
      # adding the option menus to the main window  
      input_menu = tk.OptionMenu(  
          body_frame,  
          input_value,  
          *SELECTIONS  
      )  
      output_menu = tk.OptionMenu(  
          body_frame,  
          output_value,  
          *SELECTIONS  
      )  
    
      # using the grid() method to set the position of the above option menus   
      input_menu.grid(row = 1, column = 3, padx = 30)  
      output_menu.grid(row = 2, column = 3, padx = 30)  
    
      # creating the buttons for the main window  
      # CONVERT button  
      convert_button = tk.Button(  
          body_frame,  
          text = "CONVERT",  
          bg = "#0b5345",  
          fg = "#ffffff",  
          command = convert  
      )  
      # RESET button  
      reset_button = tk.Button(  
          body_frame,  
          text = "RESET",  
          bg = "#f7dc6f",  
          fg = "#000000",  
          command = reset  
      )  
    
      # using the grid() method to set the position of the above buttons  
      convert_button.grid(row = 3, column = 2)  
      reset_button.grid(row = 3, column = 3)  
  
  # def type_of_load_list():
  #   new_win = tk.Toplevel(root)
  #   new_win.geometry("1100x600")
  #   new_win.title("Type of Load")
  #   new_win.resizable(False, False)
  #   nw_frame = tk.Frame(new_win, height=600, width=1100)
  #   nw_frame.pack()
  #   load_img = ImageTk.PhotoImage(Image.open(img_path5))
  #   nw_canvas = tk.Canvas(nw_frame, height=600, width=1100)
  #   nw_canvas.pack()
  #   nw_canvas.create_image(0, 0, image=load_img)
    
    
  other_frame = ttk.Frame(structure)
  other_frame.grid(row=2, column=2, sticky="es")
  # type_of_load_button = ttk.Button(other_frame, text="Type of Load", command=type_of_load_list)
  # type_of_load_button.grid(row=0, column=0)
  uc_button = ttk.Button(other_frame, text="Unit Converter", command=uc_window)
  uc_button.grid(row=0, column=1)


  

  list_node = {}
  list_element = {}
  list_support = {}
  list_load = {}
  cox = []
  coy = []
  coz = []
  plot_x = []
  plot_y = []
  plot_z = []
  e_ex = []
  e_ey = []
  e_ez = []
  e_initial = []
  e_final = []
  E = []
  A = []
  I = []
  G = []
  J = []
  e_E = []
  e_A = []
  e_I = []
  e_G = []
  e_J = []
  sinels = []
  cosels = []
  cons1 = []
  cons2 = []
  cons3 = []
  cons4 = []
  cons5 = []
  node_os = []
  node_ol = []
  mag_ol = []
  el_ol = []
  wv_ol = []
  av_ol = []
  bv_ol = []
  alpv_ol = []
  pv_ol = []
  RTD = []
  fms = []
  gfms = []
  initial = []
  final = []
  length = []
  s_type = []
  s_orient = []
  l_type = []
  lsms = []
  gsms = []
  lms = []
  disms = []
  Tgls = []
  kgls = []
  lnp_e = []
  lep_e = []
  mag_e = []
  wv_e = []
  av_e = []
  bv_e = []
  alp_e = []
  P_e = []
  edms = []
  soes = []
  strains = []
  coxfs = []
  coyfs = []
  plot_xf = []
  plot_yf = []
  length_f= []
  strains = []

  def prsbtn(button):
    dof_e = dof[0].get()
    dof_n = dof[1].get()
    if button == "button1":
      if dof_e != "" and dof_n != "":
        noe_input["state"] = "disabled"
        non_input["state"] = "disabled"
        global frame1, button2, noe, non
        frame1 = tk.LabelFrame(input_frame, text= "Node Coordinates", labelanchor= "n", background="#C7DAEA")
        frame1.grid(row= 1, column= 0, columnspan= 3, sticky="ew")

        frame1.columnconfigure(1, weight=1)
        frame1.columnconfigure(2, weight=1)

        text2 = tk.Label(frame1, text= "Node", background="#C7DAEA")
        text2.grid(row= 0, column= 0, padx=5, pady=1)
        text3 = tk.Label(frame1, text= "x axis", background="#C7DAEA")
        text3.grid(row= 0, column= 1, padx=5, pady=1)
        if sstructure.structureType == "Truss" or sstructure.structureType == "Frame": 
          text4 = tk.Label(frame1, text= "y axis", background="#C7DAEA")
          text4.grid(row= 0, column= 2, padx=5, pady=1)
        elif sstructure.structureType == "Grid":
          text4 = tk.Label(frame1, text= "z axis", background="#C7DAEA")
          text4.grid(row= 0, column= 2, padx=5, pady=1)
        elif sstructure.structureType == "Beam":
          pass
        noe = int (dof_e)
        non = int (dof_n)
        for i in range(non):
          a = str (i+1)
          point = tk.Label(frame1, text= a, background="#C7DAEA")
          point.grid(row= 1+i, column= 0, padx=5, pady=1)
          ex = tk.Entry(frame1, validate="key", validatecommand=(validation_float, '%S'), width= 5, justify= "center")
          if i == 0: ex.focus()
          ex.grid(row= 1+i, column= 1, sticky= "nsew", padx=5, pady=1)
          e_ex.append(ex)
          if sstructure.structureType == "Truss" or sstructure.structureType == "Frame":
            ey = tk.Entry(frame1, validate="key", validatecommand=(validation_float, '%S'), width= 5, justify= "center")
            ey.grid(row= 1+i, column= 2, sticky= "nsew", padx=5, pady=1)
            e_ey.append(ey)
          elif sstructure.structureType == "Grid":
            ez = tk.Entry(frame1, validate="key", validatecommand=(validation_float, '%S'), width= 5, justify= "center")
            ez.grid(row= 1+i, column= 2, sticky= "nsew", padx=5, pady=1)
            e_ez.append(ez)
          else:
            pass
          next_button.destroy()
        button2 = tk.Button(frame1, text = 'Next', command = lambda: prsbtn('button2'), background="#46EF63")
        button2.grid(row=1+non+noe, column= 0, columnspan=3, sticky="we", padx=2, pady=1)
      else:
        messagebox.showinfo("Alert", "Please input number of element(s) and number of nodal(s) before continue to the next step")
      for child in frame1.winfo_children():
        wtype = child.winfo_class()
        if wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")
      

    elif button == "button2":
      if sstructure.structureType == "Truss" or sstructure.structureType == "Frame":
        len_a = len(e_ex[-1].get())
        len_b = len(e_ey[-1].get())
      elif sstructure.structureType == "Grid":
        len_a = len(e_ex[-1].get())
        len_b = len(e_ez[-1].get())
      elif sstructure.structureType == "Beam":
        len_a = len(e_ex[-1].get())
        len_b = len_a
      if len_a != 0 and len_b != 0 :
        for child in frame1.winfo_children():
          child.configure(state="disabled")
          
        for i in range(non):
          if sstructure.structureType == "Truss" or sstructure.structureType == "Frame":
            list_node[i] = Coordinate(i+1, cox=e_ex[i].get(), coy=e_ey[i].get())
            cox.append(float(list_node[i].cox))
            coy.append(float(list_node[i].coy))
          elif sstructure.structureType == "Grid":
            list_node[i] = Coordinate(i+1, cox=e_ex[i].get(), coz=e_ez[i].get())
            cox.append(float(list_node[i].cox))
            coy.append(float(list_node[i].coz))
          elif sstructure.structureType == "Beam":
            list_node[i] = Coordinate(i+1, cox=e_ex[i].get())
            cox.append(float(list_node[i].cox))
            ey0 = float (0)
            coy.append(ey0)
        global scale, n_text, cx, cy
        height = 400
        width = 1000
        cx = (max(cox)+min(cox))/2
        cy = -(max(coy)+min(coy))/2

        s1_x = abs(max(cox))
        s2_x = abs(min(cox))
        if s1_x > s2_x:
          max_x = s1_x
        else:
          max_x= s2_x 
        scale_x = 1
        condition_x = scale_x*(max_x-cx)
        if max_x == 0:
          pass
        else:
          if condition_x < height:
            while condition_x < height:
              scale_x += 1/1000
              condition_x = scale_x*(max_x-cx)
          else:
            while condition_x > height:
              scale_x -= 1/1000
              condition_x = scale_x*(max_x-cx)

        s1_y = abs(max(coy))
        s2_y = abs(min(coy))
        if s1_y > s2_y:
          max_y = s1_y
        else:
          max_y= s2_y
        scale_y = 1
        condition_y = scale_y*(max_y-cy)
        if max_y == 0:
          pass 
        else:
          if condition_y < height:
            while condition_y < height:
              scale_y += 1/1000
              condition_y = scale_y*(max_y-cy)
          else:
            while condition_y > height:
              scale_y -= 1/1000
              condition_y = scale_y*(max_y-cy)
        if condition_y < height and scale_x < scale_y:
          scale = scale_x
        else:
          scale = scale_y
        # if sstructure.structureType == "Beam":
        #   if condition_y < height and scale_x < scale_y:
        #     scale = scale_x
        #   else:
        #     scale = scale_y
        # else:
        #   if condition_y < height and scale_x < scale_y:
        #     scale = scale_y
        #   else:
        #     scale = scale_x
        print(non)
        print(cox)
   
        for i in range(non):
          if sstructure.structureType == "Grid":
            y = ((coy[i]+cy)*3/5)*scale
            x = ((cox[i]-cx)*scale)-y
          elif sstructure.structureType == "Beam":
            if s1_x <= 10:
              x = (cox[i]-cx)*scale*100
              y = -(coy[i]+cy)*scale*100
            elif s1_x <= 20 and s1_x > 10:
              x = (cox[i]-cx)*scale*20
              y = -(coy[i]+cy)*scale*20
            elif s1_x <= 50 and s1_x > 20:
              x = (cox[i]-cx)*scale*10
              y = -(coy[i]+cy)*scale*10
            else:
              x = (cox[i]-cx)*scale
              y = -(coy[i]+cy)*scale
          else:
            x = (cox[i]-cx)*scale
            y = -(coy[i]+cy)*scale
          plot_x.append(x)
          plot_y.append(y)

          FBD.create_oval(x-2, y-2, x+2, y+2, fill="black")
          n_text = FBD.create_text(x+10, y-10, text=str(i+1), font=('Areal 10 bold'), fill='purple')
        print(plot_x)
        print(plot_y)
            
        print (cox, coy, coz)
        global frame2, button3
        frame2 = tk.LabelFrame(input_frame, text= "Element(s)'s Node Position", labelanchor= "n", background="#C7DAEA")
        frame2.grid(row= 2, column= 0, columnspan= 3, sticky="ew")

        frame2.columnconfigure(1, weight=1)
        frame2.columnconfigure(2, weight=1)

        text5 = tk.Label(frame2, text= "Element") 
        text5.grid(row= 0+non, column= 0, padx=5, pady=1)
        text6 = tk.Label(frame2, text= "Initial Node")
        text6.grid(row= 0+non, column= 1, padx=5, pady=1)
        text7 = tk.Label(frame2, text= "Final Node")
        text7.grid(row= 0+non, column= 2, padx=5, pady=1)
        for i in range (noe):
          a = str(i+1)
          point = tk.Label(frame2, text= a)
          point.grid(row= 1+i+non, column= 0, padx=5, pady=1)
          init = tk.Entry(frame2, validate="key", validatecommand=(validation_int, '%S'), width= 5, justify= "center")
          init.grid(row= 1+i+non, column= 1, sticky= "wesn", padx=5, pady=1)
          if i == 0: init.focus()
          e_initial.append(init)
          la = tk.Entry(frame2, validate="key", validatecommand=(validation_int, '%S'), width= 5, justify= "center")
          la.grid(row= 1+i+non, column= 2, sticky= "wesn", padx=5, pady=1)
          e_final.append(la)
        button2.destroy()
        button3 = tk.Button(frame2, text = 'Next', command = lambda: prsbtn('button3'))
        button3.grid(row= 2+non+noe, column= 0, columnspan=3, sticky="we", padx=2, pady=1)
      else:
        messagebox.showinfo("Alert", "Please fill up nodal coordinates before continue to the next step")
      for child in frame2.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")
  
    elif button == "button3":
      if len(e_initial[-1].get()) != 0 and len(e_final[-1].get()) != 0:
        for child in frame2.winfo_children():
          child.configure(state="disabled")
        for i in range(noe):
          initial.append(int(e_initial[i].get()))
          final.append(int(e_final[i].get()))
          p1 = initial[i]-1
          p2 = final[i]-1
          x1 = plot_x[p1]
          y1 = plot_y[p1]
          x2 = plot_x[p2]
          y2 = plot_y[p2]
          L = math.sqrt((x2-x1)**2+(y2-y1)**2)
          theta_rad = math.asin((y2-y1)/L)
          pi = math.pi
          theta = theta_rad*180/pi
          sv = 0
          if theta != 0:
            sv = 15
          print(theta)
          e_line = FBD.create_line(x1, y1 , x2, y2, fill="#4F6F52", width=1)
          e_text = FBD.create_text(((x1+x2)/2)-sv, ((y1+y2)/2)-10, text="[e"+str(i+1)+"]", fill="#005B41", font="TNR 10 bold")
          # FBD.tag_lower(e_line)
          FBD.tag_raise(e_text)

        global frame3, button4
        frame3 = tk.LabelFrame(input_frame, text="Material Properties", labelanchor="n", background="#C7DAEA")
        frame3.grid(row= 3, column= 0, columnspan= 3, sticky="ew")
        button4 = tk.Button(frame3, text = 'Next', command = lambda: prsbtn('button4'))
        quest1 = tk.Label(frame3, text="Do all elements have same properties?")
        quest1.grid(row=0, column=0, columnspan=2)

        question = tk.IntVar(frame3)

        def exe():
          answer = question.get()
          if answer == 1:
            el_mo_label = tk.Label(frame3, text="E")
            el_mo_label.grid(row=2, column=0, padx=5, pady=1)
            el_mo_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
            el_mo_input.grid(row=2, column=1, sticky= "we", padx=5, pady=1)
            el_mo_input.focus()

            if sstructure.structureType == "Truss":
              cs_area_label = tk.Label(frame3, text="A")
              cs_area_label.grid(row=3, column=0, padx=5, pady=1)
              cs_area_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              cs_area_input.grid(row=3, column=1, sticky= "we", padx=5, pady=1)
              for i in range (noe):
                e_E.append(el_mo_input)
                e_A.append(cs_area_input)

            elif sstructure.structureType == "Beam":
              plan_iner_label = tk.Label(frame3, text="I")
              plan_iner_label.grid(row=3, column=0, padx=5, pady=1)
              plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              plan_iner_input.grid(row=3, column=1, sticky= "we", padx=5, pady=1)
              for i in range (noe):
                e_E.append(el_mo_input)
                e_I.append(plan_iner_input)

            elif sstructure.structureType == "Frame":
              cs_area_label = tk.Label(frame3, text="A")
              cs_area_label.grid(row=3, column=0, padx=5, pady=1)
              cs_area_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              cs_area_input.grid(row=3, column=1, sticky= "we", padx=5, pady=1)
              plan_iner_label = tk.Label(frame3, text="I")
              plan_iner_label.grid(row=4, column=0, padx=5, pady=1)
              plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              plan_iner_input.grid(row=4, column=1, sticky= "we", padx=5, pady=1)
              for i in range (noe):
                e_E.append(el_mo_input)
                e_A.append(cs_area_input)
                e_I.append(plan_iner_input)

            elif sstructure.structureType == "Grid":
              shear_mod_label = tk.Label(frame3, text="G")
              shear_mod_label.grid(row=3, column=0, padx=5, pady=1)
              shear_mod_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              shear_mod_input.grid(row=3, column=1, sticky= "we", padx=5, pady=1)
              plan_iner_label = tk.Label(frame3, text="I")
              plan_iner_label.grid(row=4, column=0, padx=5, pady=1)
              plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              plan_iner_input.grid(row=4, column=1, sticky= "we", padx=5, pady=1)
              pol_iner_label = tk.Label(frame3, text="J")
              pol_iner_label.grid(row=5, column=0, padx=5, pady=1)
              pol_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              pol_iner_input.grid(row=5, column=1, sticky= "we", padx=5, pady=1)
              for i in range (noe):
                e_E.append(el_mo_input)
                e_G.append(shear_mod_input)
                e_I.append(plan_iner_input)
                e_J.append(pol_iner_input)

            button4.grid(row=6, column=0, columnspan=3, sticky="we", padx=2, pady=1)
            yes["state"] = "disabled"
            no["state"] = "disabled"
            for child in frame3.winfo_children():
              wtype = child.winfo_class()
              if  wtype not in ("Entry", "Button"):
                child.configure(background="#C7DAEA")
              elif wtype in ("Button"):
                child.configure(background="#46EF63")

          elif answer == 2:
            for i in range (noe):
              sect1 = tk.Label(frame3, text="Element "+str(i+1)+" Properties")
              sect1.grid(row=2+(i*5), column=0, columnspan=2, padx=5, pady=1)
              el_mo_label = tk.Label(frame3, text="E"+str(i+1))
              el_mo_label.grid(row=3+(i*5), column=0, padx=5, pady=1)
              el_mo_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
              el_mo_input.grid(row=3+(i*5), column=1, sticky= "we", padx=5, pady=1)
              el_mo_input.focus()
              if sstructure.structureType == "Truss":
                cs_area_label = tk.Label(frame3, text="A"+str(i+1))
                cs_area_label.grid(row=4+(i*5), column=0, padx=5, pady=1)
                cs_area_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                cs_area_input.grid(row=4+(i*5), column=1, sticky= "we", padx=5, pady=1)
                e_E.append(el_mo_input)
                e_A.append(cs_area_input)
              elif sstructure.structureType == "Beam":
                plan_iner_label = tk.Label(frame3, text="I"+str(i+1))
                plan_iner_label.grid(row=4+(i*5), column=0, padx=5, pady=1)
                plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                plan_iner_input.grid(row=4+(i*5), column=1, sticky= "we", padx=5, pady=1)
                e_E.append(el_mo_input)
                e_I.append(plan_iner_input)
              elif sstructure.structureType == "Frame":
                cs_area_label = tk.Label(frame3, text="A"+str(i+1))
                cs_area_label.grid(row=4+(i*5), column=0, padx=5, pady=1)
                cs_area_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                cs_area_input.grid(row=4+(i*5), column=1, sticky= "we", padx=5, pady=1)
                plan_iner_label = tk.Label(frame3, text="I"+str(i+1))
                plan_iner_label.grid(row=5+(i*5), column=0, padx=5, pady=1)
                plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                plan_iner_input.grid(row=5+(i*5), column=1, sticky= "we", padx=5, pady=1)
                e_E.append(el_mo_input)
                e_A.append(cs_area_input)
                e_I.append(plan_iner_input)
              elif sstructure.structureType == "Grid":
                shear_mod_label = tk.Label(frame3, text="G"+str(i+1))
                shear_mod_label.grid(row=4+(i*5), column=0, padx=5, pady=1)
                shear_mod_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                shear_mod_input.grid(row=4+(i*5), column=1, sticky= "we", padx=5, pady=1)
                plan_iner_label = tk.Label(frame3, text="I"+str(i+1))
                plan_iner_label.grid(row=5+(i*5), column=0, padx=5, pady=1)
                plan_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                plan_iner_input.grid(row=5+(i*5), column=1, sticky= "we", padx=5, pady=1)
                pol_iner_label = tk.Label(frame3, text="J"+str(i+1))
                pol_iner_label.grid(row=6+(i*5), column=0, padx=5, pady=1)
                pol_iner_input = tk.Entry(frame3, validate="key", validatecommand=(validation_float, '%S'), width= 25, justify= "center")
                pol_iner_input.grid(row=6+(i*5), column=1, sticky= "we", padx=5, pady=1)
                e_E.append(el_mo_input)
                e_G.append(shear_mod_input)
                e_I.append(plan_iner_input)
                e_J.append(pol_iner_input)
              if i == (noe-1):
                button4.grid(row=7+(i*5), column=0, columnspan=3, sticky="we", padx=2, pady=1)
            yes["state"] = "disabled"
            no["state"] = "disabled"
            print(question.get())
            for child in frame3.winfo_children():
              wtype = child.winfo_class()
              if  wtype not in ("Entry", "Button"):
                child.configure(background="#C7DAEA")
              elif wtype in ("Button"):
                child.configure(background="#46EF63")
        yes = tk.Radiobutton(frame3, text="Yes", variable=question, value=1, command=exe)
        yes.grid(row=1, column=0)
        no = tk.Radiobutton(frame3, text="No", variable=question, value=2, command=exe)          
        no.grid(row=1, column=1)
        button3.destroy()
      else:
        messagebox.showinfo("Alert", "Please fill up nodal position on element before continue to the next step")
      for child in frame3.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")

    elif button == "button4":
      if sstructure.structureType == "Truss":
        arg1 = len(e_E[-1].get())
        arg2 = len(e_A[-1].get())
        arg3 = len(e_A[-1].get())
        arg4 = len(e_A[-1].get())
      if sstructure.structureType == "Beam":
        arg1 = len(e_E[-1].get())
        arg2 = len(e_I[-1].get())
        arg3 = len(e_I[-1].get())
        arg4 = len(e_I[-1].get())
      if sstructure.structureType == "Frame":
        arg1 = len(e_E[-1].get())
        arg2 = len(e_A[-1].get())
        arg3 = len(e_I[-1].get())
        arg4 = len(e_A[-1].get())
      if sstructure.structureType == "Grid":
        arg1 = len(e_E[-1].get())
        arg2 = len(e_G[-1].get())
        arg3 = len(e_I[-1].get())
        arg4 = len(e_J[-1].get())
      if arg1 != 0 and arg2 != 0 and arg3 != 0 and arg4 != 0:
        for child in frame3.winfo_children():
          child.configure(state="disabled")

        global tgsm, lm, dimf

        for i in range (noe):
          cx1 = cox [initial[i]-1]
          cx2 = cox [final[i]-1]
          cy1 = coy [initial[i]-1]
          cy2 = coy [final[i]-1]
          E.append(e_E[i].get())
          if sstructure.structureType == 'Truss':
            A.append(e_A[i].get())
            L = math.sqrt((cx2-cx1)**2+(cy2-cy1)**2)
            length.append(L)
            sinel = (cy2-cy1)/L
            sinels.append(sinel)
            cosel = (cx2-cx1)/L
            cosels.append(cosel)
            con1 = float(A[i])*float(E[i])/L
            cons1.append(con1)
            ss = sinels[i]**2
            cc = cosels[i]**2
            cs = sinels[i]*cosels[i]
            lsm = cons1[i]*np.array([[cc, cs, -cc, -cs],
                                    [cs, ss, -cs, -ss],
                                    [-cc, -cs, cc, cs],
                                    [-cs, -ss, cs, ss]])
            lsms.append(lsm)
            pos1 = initial[i]*2
            pos2 = final[i]*2
            position = [pos1-1, pos1, pos2-1, pos2]
            gsm = np.zeros(((non*2),(non*2)))
            for j in range(4):
              for k in range(4):
                p1 = position[j]-1
                p2 = position[k]-1
                gsm[p1,p2] = lsm[j,k]
            gsms.append(gsm)
            if i == (noe-1):
              tgsm = sum(gsms)
              dimf = np.ones((non*2, 1))


          elif sstructure.structureType == 'Beam':
            I.append(e_I[i].get())
            L = cox[i+1]-cox[i]
            length.append(L)
            con1 = float(E[i])*float(I[i])/(L**3)
            cons1.append(con1)
            lsm = cons1[i] * np.array([ [12, 6*L, -12, 6*L],
                                        [6*L, 4*L**2, -6*L, 2*L**2],
                                        [-12, -6*L, 12, -6*L],
                                        [6*L, 2*L**2, -6*L, 4*L**2]   ])
            lsms.append(lsm)
            pos1 = initial[i]*2
            pos2 = final[i]*2
            position = [pos1-1, pos1, pos2-1, pos2]
            gsm = np.zeros(((non*2),(non*2)))
            for j in range(4):
              for k in range(4):
                p1 = position[j]-1
                p2 = position[k]-1
                gsm[p1,p2] = lsm[j,k]
            gsms.append(gsm)
            if i == (noe-1):
              tgsm = sum(gsms)
              dimf = np.ones((non*2, 1))
              

          elif sstructure.structureType == 'Frame':
            A.append(e_A[i].get())
            I.append(e_I[i].get())
            L = math.sqrt((cx2-cx1)**2+(cy2-cy1)**2)
            length.append(L)
            sinel = (cy2-cy1)/L
            sinels.append(sinel)
            cosel = (cx2-cx1)/L
            cosels.append(cosel)
            con1 = (12*float(I[i]))/(L**2)
            cons1.append(con1)
            con2 = (6*float(I[i]))/L
            cons2.append(con2)
            con3 = float(E[i])/L
            cons3.append(con3)
            S = sinels[i]
            C = cosels[i]
            SS = S**2
            CC = C**2
            CS = S*C
            f1 = cons1[i]
            f2 = cons2[i]
            f3 = cons3[i]
            As = float(A[i])
            Is = float(I[i])
            lsm = f3 * np.array ([[(As*CC)+(f1*SS), (As-f1)*CS, -f2*S, -((As*CC)+(f1*SS)), -((As-f1)*CS), -f2*S],
                                  [(As-f1)*CS, (As*SS)+(f1*CC), f2*C, -((As-f1)*CS), -((As*SS)+(f1*CC)), f2*C],
                                  [-f2*S, f2*C, 4*Is, f2*S, -(f2*C), 2*Is],
                                  [-((As*CC)+(f1*SS)), -((As-f1)*CS), f2*S, (As*CC)+(f1*SS), (As-f1)*CS, f2*S],
                                  [-((As-f1)*CS), -((As*SS)+(f1*CC)), -(f2*C), (As-f1)*CS, (As*SS)+(f1*CC), -(f2*C)],
                                  [-f2*S, f2*C, 2*Is, f2*S, -(f2*C), 4*Is]])
            lsms.append(lsm)
            pos1 = initial[i]*3
            pos2 = final[i]*3
            position = [pos1-2, pos1-1, pos1, pos2-2, pos2-1, pos2]
            gsm = np.zeros(((non*3),(non*3)))
            for j in range(6):
                for k in range(6):
                    p1 = position[j]-1
                    p2 = position[k]-1
                    gsm[p1,p2] = lsm[j,k]
            gsms.append(gsm)
            if i == (noe-1):
              tgsm = sum(gsms)
              dimf = np.ones((non*3, 1))

          elif sstructure.structureType == 'Grid':
            G.append(e_G[i].get())
            I.append(e_I[i].get())
            J.append(e_J[i].get())
            L = math.sqrt((cx2-cx1)**2+(cy2-cy1)**2)
            length.append(L)
            sinel = (cy2-cy1)/L
            sinels.append(sinel)
            cosel = (cx2-cx1)/L
            cosels.append(cosel)
            con1 = (12*float(E[i])*float(I[i])/(L**3))
            cons1.append(con1)
            con2 = (6*float(E[i])*float(I[i])/(L**2))
            cons2.append(con2)
            con3 = (float(G[i])*float(J[i])/L)
            cons3.append(con3)
            con4 = (4*float(E[i])*float(I[i])/L)
            cons4.append(con4)
            con5 = (2*float(E[i])*float(I[i])/L)
            cons5.append(con5)
            S = sinels[i]
            C = cosels[i]
            f1 = cons1[i]
            f2 = cons2[i]
            f3 = cons3[i]
            f4 = cons4[i]
            f5 = cons5[i] 
            Tgl = np.array ([ [1, 0, 0, 0, 0, 0],
                              [0, C, S, 0, 0, 0],
                              [0, -S, C, 0, 0, 0],
                              [0, 0, 0, 1, 0, 0],
                              [0, 0, 0, 0, C, S],
                              [0, 0, 0, 0, -S, C]  ])
            kgl = np.array ([ [f1,0,f2,-f1,0,f2],
                              [0,f3,0,0,-f3,0],
                              [f2,0,f4,-f2,0,f5],
                              [-f1,0,-f2,f1,0,-f2],
                              [0,-f3,0,0,f3,0],
                              [f2,0,f5,-f2,0,f4]  ])
            Tgls.append(Tgl)
            kgls.append(kgl)
            o1 = Tgl.transpose()
            o2 = np.matmul(o1,kgl)
            lsm = np.matmul(o2,Tgl)
            lsms.append(lsm)
            pos1 = initial[i]*3
            pos2 = final[i]*3
            position = [pos1-2, pos1-1, pos1, pos2-2, pos2-1, pos2]
            gsm = np.zeros(((non*3),(non*3)))
            for j in range(6):
                for k in range(6):
                    p1 = position[j]-1
                    p2 = position[k]-1
                    gsm[p1,p2] = lsm[j,k]
            gsms.append(gsm)
            if i == (noe-1):
              tgsm = sum(gsms)
              dimf = np.ones((non*3, 1))

        print(E)
        print(A)
        print(I)
        print(G)
        print(J)
        print(cons1)
        print(cons2)
        print(cons3)
        print(cons4)
        print(cons5)
        print(lsms)
        print(gsms)
        print(tgsm)

        global frame4, button5, nos_input
        frame4 = tk.LabelFrame(input_frame, text="Support Properties", labelanchor="n", background="#C7DAEA")
        frame4.grid(row= 4, column= 0, columnspan= 3, sticky="ew")

        nos_label = tk.Label(frame4, text="Number of Support(s)")
        nos_label.grid(row=0, column=0, padx=(5, 5), pady=1, sticky="W")
        nos_input = tk.Entry(frame4, validate="key", validatecommand=(validation_int, '%S'), width=10, borderwidth=2 , justify="center")
        nos_input.grid(row=0, column=1, padx=(0, 5), pady=1, sticky="W")
        nos_input.focus()
        button4.destroy()
        button5 = tk.Button(frame4, text = 'Next', command = lambda: prsbtn('button5'))
        button5.grid(row=1, column=0, columnspan=3, sticky="we", padx=2, pady=1)
      else:
        messagebox.showinfo("Alert", "Please fill up all material properties needed before continue to the next step")
      for child in frame4.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")

    elif button == "button5":
      if nos_input.get() != "":
        nos_input["state"] = "disabled"
        global frame5, button6, nos
        button5.destroy()
        frame5 = tk.Frame(frame4, background="#C7DAEA")
        frame5.grid(row=1, column= 0, columnspan= 3, sticky="ew")

        nos = int (nos_input.get())
        button6 = tk.Button(frame5, text = 'Next', command = lambda: prsbtn('button6'))
        s_text1 = tk.Label(frame5, text="No.", width=2)
        s_text1.grid(row=0, column=0, padx=5, pady=1)
        s_text2 = tk.Label(frame5, text="Node", width=3)
        s_text2.grid(row=0, column=1, padx=5, pady=1)
        s_text3 = tk.Label(frame5, text="Type", width=6)
        s_text3.grid(row=0, column=2, padx=5, pady=1)
        s_text4 = tk.Label(frame5, text="Orient", width=11)
        s_text4.grid(row=0, column=3, padx=5, pady=1)

        for i in range(nos):
          s_text5 = tk.Label(frame5, text=str(i+1), width=2)
          s_text5.grid(row=1+i, column=0, padx=5, pady=1)
          s_entry1 = tk.Entry(frame5, validate="key", validatecommand=(validation_int, '%S'), width= 3, justify= "center")
          s_entry1.grid(row=1+i, column=1, sticky="we", padx=5, pady=1)
          if i == 0: s_entry1.focus() 
          node_os.append(s_entry1)
          s_type_box = ttk.Combobox(frame5, values=['Fixed', 'Pinned', 'Roller'], width=6)
          s_type_box.grid(row=1+i, column=2, padx=5, pady=1)
          s_type.append(s_type_box)
          s_orient_box = ttk.Combobox(frame5, values=['Vertical(+)', 'Vertical(-)', 'Horizontal(+)', 'Horizontal(-)'], width=11)
          s_orient_box.grid(row=1+i, column=3, padx=5, pady=1)
          s_orient.append(s_orient_box)
          if i == (nos-1):
              button6.grid(row=2+i, column=0, columnspan=4, sticky="we", padx=2, pady=1)
      elif nos_input.get() == "":
        messagebox.showinfo("Alert", "Please input how many support(s) exist in the structure before continue to the next step")
      for child in frame5.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")

    elif button == "button6":
      if len(node_os[-1].get()) != 0 or len(s_type[-1].get()) != 0 or len(s_orient[-1].get()) != 0:
        for i in range(nos):
          #snp = support nodal point
          #sor = support orient
          sup_type = str(s_type[i].get())
          sor = str(s_orient[i].get())
          snp = int(node_os[i].get())
          x = plot_x [snp-1]
          y = plot_y [snp-1]
          if sor in ['Vertical(+)']:
            if sup_type in ["Fixed"]:
              FBD.create_rectangle(x-25,y+4,x+25,y+2, fill='#D0D4CA', tags='support')
              for i in range(10):
                FBD.create_line(x-(20-i*5), y+14, x-(25-i*5),y+4, fill='black')
            elif sup_type in ["Pinned"]:
              FBD.create_polygon(x,y,x+15,y+25,x-15,y+25, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-20, y+25, x+20, y+27, fill='#D0D4CA', tags='support')
              for i in range(8):
                FBD.create_line(x-(20-i*5), y+37, x-(15-i*5), y+27, fill='black')
            elif sup_type in ["Roller"]:
              FBD.create_polygon(x,y,x+15,y+25,x-15,y+25, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-15, y+25, x-5, y+35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-5, y+25, x+5, y+35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x+5, y+25, x+15, y+35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-20, y+35, x+20, y+37, fill='#D0D4CA', tags='support')
              for i in range(8): 
                FBD.create_line(x-(20-i*5), y+47, x-(15-i*5), y+37, fill='black')

          elif sor in ['Vertical(-)']:
            if sup_type in ["Fixed"]:
              FBD.create_rectangle(x-25,y-4,x+25,y-2, fill='#D0D4CA', tags='support')
              for i in range(10):
                FBD.create_line(x-(20-i*5), y-14, x-(25-i*5),y-4, fill='black')
            elif sup_type in ["Pinned"]:
              FBD.create_polygon(x,y,x+15,y-25,x-15,y-25, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-20, y-25, x+20, y-27, fill='#D0D4CA', tags='support')
              for i in range(8):
                FBD.create_line(x-(20-i*5), y-37, x-(15-i*5), y-27, fill='black')
            elif sup_type in ["Roller"]:
              FBD.create_polygon(x,y,x+15,y-25,x-15,y-25, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-15, y-25, x-5, y-35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-5, y-25, x+5, y-35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x+5, y-25, x+15, y-35, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-20, y-35, x+20, y-37, fill='#D0D4CA', tags='support')
              for i in range(8): 
                FBD.create_line(x-(20-i*5), y-47, x-(15-i*5), y-37, fill='black')

          elif sor in ['Horizontal(+)']:
            if sup_type in ["Fixed"]:
              FBD.create_rectangle(x-4,y-25,x-2,y+25, fill='#D0D4CA', tags='support')
              for i in range(10):
                FBD.create_line(x-14, y-(20-i*5), x-4,y-(25-i*5), fill='black')
            elif sup_type in ["Pinned"]:
              FBD.create_polygon(x,y,x-25,y+15,x-25,y-15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-25, y-20, x-27, y+20, fill='#D0D4CA', tags='support')
              for i in range(8):
                FBD.create_line(x-37, y-(20-i*5), x-27, y-(15-i*5), fill='black')
            elif sup_type in ["Roller"]:
              FBD.create_polygon(x,y,x-25,y+15,x-25,y-15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-25, y-15, x-35, y-5, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-25, y-5, x-35, y+5, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x-25, y+5, x-35, y+15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x-35, y-20, x-37, y+20, fill='#D0D4CA', tags='support')
              for i in range(8): 
                FBD.create_line(x-47, y-(20-i*5), x-37, y-(15-i*5), fill='black')

          elif sor in ['Horizontal(-)']:
            if sup_type in ["Fixed"]:
              FBD.create_rectangle(x+4,y-25,x+2,y+25, fill='#D0D4CA', tags='support')
              for i in range(10):
                FBD.create_line(x+14, y-(20-i*5), x+4,y-(25-i*5), fill='black')
            elif sup_type in ["Pinned"]:
              FBD.create_polygon(x,y,x+25,y+15,x+25,y-15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x+25, y-20, x+27, y+20, fill='#D0D4CA', tags='support')
              for i in range(8):
                FBD.create_line(x+37, y-(20-i*5), x+27, y-(15-i*5), fill='black')
            elif sup_type in ["Roller"]:
              FBD.create_polygon(x,y,x+25,y+15,x+25,y-15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x+25, y-15, x+35, y-5, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x+25, y-5, x+35, y+5, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_oval(x+25, y+5, x+35, y+15, fill='#D0D4CA', outline='black', tags='supports')
              FBD.create_rectangle(x+35, y-20, x+37, y+20, fill='#D0D4CA', tags='support')
              for i in range(8): 
                FBD.create_line(x+47, y-(20-i*5), x+37, y-(15-i*5), fill='black')
        for child in frame5.winfo_children():
          child.configure(state="disabled")
        global frame6, button7, nol_input
        button6.destroy()
        frame6 = tk.LabelFrame(input_frame, text="Load Properties", labelanchor="n", background="#C7DAEA")
        frame6.grid(row=5, column= 0, columnspan= 3, sticky="ew")

        nol_label = tk.Label(frame6, text="Number of Load(s)          ", justify='left')
        nol_label.grid(row=0, column=0, padx=(5, 5), pady=1, sticky="W")
        nol_input = tk.Entry(frame6, validate="key", validatecommand=(validation_int, '%S'), width=10, borderwidth=2 , justify="center")
        nol_input.grid(row=0, column=1, padx=(0, 5), pady=1, sticky="W")
        nol_input.focus()
        button7 = tk.Button(frame6, text = 'Next', command = lambda: prsbtn('button7'))
        button7.grid(row=1, column=0, columnspan=4, sticky="we", padx=2, pady=1)
      else:
        messagebox.showinfo("Alert", "Please fill up all support properties needed before continue to the next step")
      for child in frame6.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")

    elif button == "button7":
      if nos_input.get() != "":
        nos_input["state"] = "disabled"
        global frame7, button8, nol, l_type_box
        button6.destroy()
        frame7 = tk.Frame(frame6, background="#C7DAEA")
        frame7.grid(row=1, column= 0, columnspan= 4, sticky="ew")
        nol = int (nol_input.get())
        button8 = tk.Button(frame7, text = 'Next', command = lambda: prsbtn('button8'))
        if nol_input.get() != "":
          nol_input["state"] = "disabled"
        l_text1 = tk.Label(frame7, text="No.")
        l_text1.grid(row=0, column=0, padx=5, pady=1)
        l_text2 = tk.Label(frame7, text="Load Type")
        l_text2.grid(row=0, column=1, padx=5, pady=1,sticky="ew")
        if sstructure.structureType == "Truss":
          load_var = ["Vertical Load", "Horizontal Load"]
        elif sstructure.structureType == "Beam":
          load_var = ["Vertical Load", "Moment", "Distributed Load [R]", "Distributed Load [RT]", "Distributed Load [IT]", "Distributed Load [P]", "Concentrated Load [1]", "Concentrated Load [2]", "Concentrated Load [3]"]
        elif sstructure.structureType == "Frame":
          load_var = ["Vertical Load", "Horizontal Load", "Moment", "Distributed Load [R]", "Distributed Load [RT]", "Distributed Load [IT]", "Distributed Load [P]", "Concentrated Load [1]", "Concentrated Load [2]", "Concentrated Load [3]"]
        elif sstructure.structureType == "Grid":
          load_var = ["Vertical Load", "Moment (x-axis)", "Moment (z-axis)"]
        for i in range(nol):
          l_text5 = tk.Label(frame7, text=str(i+1))
          l_text5.grid(row=1+i, column=0, padx=5, pady=1)
          l_type_box = ttk.Combobox(frame7, values=load_var, width=25)
          l_type_box.grid(row=1+i, column=1, padx=5, pady=1, sticky="ew")
          l_type.append(l_type_box)
          if i == (nol-1):
              button8.grid(row=2+i, column=0, columnspan=4, sticky="we", padx=2, pady=1)
      elif nos_input.get() == "":
        messagebox.showinfo("Alert", "Please input how many support(s) exist in the structure before continue to the next step")
      for child in frame7.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")

    elif button == "button8":
      button8.destroy()
      global frame8, button9, l_frame
      frame8 = tk.Frame(frame6, background="#C7DAEA")
      frame8.grid(row=2, column= 0, columnspan= 4, sticky="ew")
      button9 = tk.Button(frame8, text = 'Execute', command = lambda: prsbtn('button9'))
      l_type_box.configure(state="disabled")
      for i in range(nol):
        load_type = str(l_type[i].get())
        l_frame = tk.LabelFrame(frame8, text='Load '+str(i+1)+' Properties', labelanchor='n', background="#C7DAEA")
        l_frame.grid(row=0+i*1, column=0, columnspan=2, sticky="ew")

        if load_type in ['Vertical Load']:
          l_text1 = tk.Label(l_frame, text='Load Node', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='Load Magnitude', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          node_ol.append(l_entry1)
          mag_ol.append(l_entry2)
          el_ol.append(0)
          wv_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Horizontal Load']:
          l_text1 = tk.Label(l_frame, text='Load Node', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, width=3, validate="key", validatecommand=(validation_int, '%S'), borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='Load Magnitude', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          node_ol.append(l_entry1)
          mag_ol.append(l_entry2)
          el_ol.append(0)
          wv_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Moment'] or load_type in ['Moment (x-axis)'] or load_type in ['Moment (z-axis)']:
          l_text1 = tk.Label(l_frame, text='Load Node', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='Load Magnitude', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          node_ol.append(l_entry1)
          mag_ol.append(l_entry2)
          el_ol.append(0)
          wv_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Distributed Load [R]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='w Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          el_ol.append(l_entry1)
          wv_ol.append(l_entry2)
          node_ol.append(0)
          mag_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Distributed Load [RT]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='w Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          l_text3 = tk.Label(l_frame, text="Which node side is greater?")
          l_text3.grid(row=2+i*4, column=0, columnspan=1, sticky="w")
          l_opt = ttk.Combobox(l_frame, values=["Initial node", "Final node"], width=20)
          l_opt.grid(row=3+i*4, column=0, columnspan=1, sticky="w")
          RTD.append(l_opt)
          el_ol.append(l_entry1)
          wv_ol.append(l_entry2)
          node_ol.append(0)
          mag_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)

        elif load_type in ['Distributed Load [IT]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='w Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          el_ol.append(l_entry1)
          wv_ol.append(l_entry2)
          node_ol.append(0)
          mag_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Distributed Load [P]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='w Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          el_ol.append(l_entry1)
          wv_ol.append(l_entry2)
          node_ol.append(0)
          mag_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          pv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Concentrated Load [1]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*2, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*2, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='P Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*2, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*2, column=1, sticky='w')
          el_ol.append(l_entry1)
          pv_ol.append(l_entry2)
          node_ol.append(0)
          mag_ol.append(0)
          wv_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          alpv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Concentrated Load [2]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*4, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*4, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='a Value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*4, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*4, column=1, sticky='w')
          l_text3 = tk.Label(l_frame, text='b Value', background="#C7DAEA", width=15, justify='left')
          l_text3.grid(row=2+i*4, column=0, sticky='w')
          l_entry3 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry3.grid(row=2+i*4, column=1, sticky='w')
          l_text4 = tk.Label(l_frame, text='P Value', background="#C7DAEA", width=15, justify='left')
          l_text4.grid(row=3+i*4, column=0, sticky='w')
          l_entry4 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry4.grid(row=3+i*4, column=1, sticky='w')
          el_ol.append(l_entry1)
          av_ol.append(l_entry2)
          bv_ol.append(l_entry3)
          pv_ol.append(l_entry4)
          node_ol.append(0)
          mag_ol.append(0)
          wv_ol.append(0)
          alpv_ol.append(0)
          RTD.append(0)

        elif load_type in ['Concentrated Load [3]']:
          l_text1 = tk.Label(l_frame, text='Load Element', background="#C7DAEA", width=15, justify='left')
          l_text1.grid(row=0+i*3, column=0, sticky='w')
          l_entry1 = tk.Entry(l_frame, validate="key", validatecommand=(validation_int, '%S'), width=3, borderwidth=2)
          l_entry1.grid(row=0+i*3, column=1, sticky='w')
          l_text2 = tk.Label(l_frame, text='Alpha value', background="#C7DAEA", width=15, justify='left')
          l_text2.grid(row=1+i*3, column=0, sticky='w')
          l_entry2 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry2.grid(row=1+i*3, column=1, sticky='w')
          l_text3 = tk.Label(l_frame, text='P value', background="#C7DAEA", width=15, justify='left')
          l_text3.grid(row=2+i*3, column=0, sticky='w')
          l_entry3 = tk.Entry(l_frame, validate="key", validatecommand=(validation_float, '%S'), width=17, borderwidth=2)
          l_entry3.grid(row=2+i*3, column=1, sticky='w')
          el_ol.append(l_entry1)
          alpv_ol.append(l_entry2)
          pv_ol.append(l_entry3)
          node_ol.append(0)
          mag_ol.append(0)
          wv_ol.append(0)
          av_ol.append(0)
          bv_ol.append(0)
          RTD.append(0)
    
        if i == (nol-1):
          button9.grid(row=1+i*1, column=0, columnspan=4, sticky="we", padx=2, pady=1)

      for child in frame8.winfo_children():
        wtype = child.winfo_class()
        if  wtype not in ("Entry", "Button"):
          child.configure(background="#C7DAEA")
        elif wtype in ("Button"):
          child.configure(background="#46EF63")
    
    elif button == "button9":
      button9.destroy()
      for child in l_frame.winfo_children():
        child.configure(state="disabled")
      
      for i in range (nol):
        load_type = str(l_type[i].get())
        if sstructure.structureType == "Truss":
          lm = np.zeros((non*2,1))
          if load_type in ["Vertical Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*2-1] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag < 0:
                FBD.create_line(x, y-40, x, y, fill='#EF4040', width=3, arrow='last')
                FBD.create_text(x+10, y-50, text=str(abs(mag)), font="Aereal 10 bold")
              elif mag > 0:
                FBD.create_line(x, y+40, x, y, fill='#EF4040', width=3, arrow='last')
                FBD.create_text(x+10, y+50, text=str(mag), font="Aereal 10 bold")
              
          elif load_type in ["Horizontal Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*2-2] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag > 0:
                FBD.create_line(x-40, y, x, y, fill='#EF4040', width=3, arrow='last')
                FBD.create_text(x-50, y-10, text=str(mag), font="Aereal 10 bold")
              elif mag < 0:
                FBD.create_line(x+40, y, x, y, fill='#EF4040', width=3, arrow='last')
                FBD.create_text(x+50, y-10, text=str(abs(mag)), font="Aereal 10 bold")

        elif sstructure.structureType == "Beam":
          lm = np.zeros((non*2,1))
          if load_type in ["Vertical Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*2-2] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag < 0:
                FBD.create_line(x, y-40, x, y, fill='#EF4040', width=3, arrow='last')
                FBD.create_text(x+10, y-50, text=str(abs(mag)), font="Aereal 10 bold")
              elif mag > 0:
                FBD.create_line(x, y+40, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x+10, y+50, text=str(mag), font="Aereal 10 bold")


          elif load_type in ["Moment"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*2-1] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag > 0:
                FBD.create_line(x-15, y-5, x-5, y-15, x+5, y-15, x+15, y-5, x+15, y+5, x+5, y+15, x-5, y+15, fill="red", smooth=1, arrow="first")
                FBD.create_text(x+10, y-25, text=str(abs(mag)), fill="red", font="Aereal 10 bold")
              elif mag < 0:
                FBD.create_line(x-15, y-5, x-5, y-15, x+5, y-15, x+15, y-5, x+15, y+5, x+5, y+15, x-5, y+15, fill="red", smooth=1, arrow="last")
                FBD.create_text(x+10, y-25, text=str(abs(mag)), fill="red", font="Aereal 10 bold")

          elif load_type in ["Distributed Load [R]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/2],
                            [(-wv*length[o]**2)/12],
                            [(-wv*length[o])/2],
                            [(wv*length[o]**2)/12]]) 
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              magc = abs(wv)
              while magc >= 100:
                magc = magc/10
              FBD.create_text((x1+x2)/2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
              FBD.create_line(x1,y1-30-magc,x2,y2-30-magc, fill='red', width=1)
              fc = 0
              while x1+fc*20 <= x2:
                if wv < 0:
                  FBD.create_line(x1+fc*20, y1-30-magc, x1+fc*20, y1, fill='red', width=1, arrow='last')
                else:
                  FBD.create_line(x1+fc*20, y1-30-magc, x1+fc*20, y1, fill='red', width=1, arrow='first')
                fc=fc+1


          elif load_type in ["Distributed Load [RT]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              tend = str(RTD[i].get())
              if tend == 0:
                pass
              elif tend in ["Initial node"]:
                o = lep-1
                fm0 = np.array([[(-7*wv*length[o])/20],
                                [(-wv*length[o]**2)/20],
                                [(-3*wv*length[o])/20],
                                [(wv*length[o]**2)/30]])
                fms.append(fm0)
                pos1 = initial[o]*2
                pos2 = final[o]*2
                position = [pos1-1, pos1, pos2-1, pos2]
                gfm0 = np.zeros(((non*2),1))
                for j in range(4):
                    p1 = position[j]-1
                    gfm0[p1,0] = fm0[j,0]
                x1 = plot_x[initial[o]-1]
                y1 = plot_y[initial[o]-1]
                x2 = plot_x[final[o]-1]
                y2 = plot_y[final[o]-1]
                magc = abs(wv)
                while magc >= 100:
                  magc = magc/10
                FBD.create_text(x1, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
                FBD.create_polygon(x1, y1, x1, y1-30-magc, x2, y2, outline="red", fill="")
                fc = 0
                while x1+fc*20 <= x2:
                  x = x1+fc*20
                  y = ((y1-30-magc)/((x2-x1)))*(x-x2)
                  print(x, y)
                  if wv < 0:
                    FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="last")
                  elif wv > 0:
                    FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="first")
                  fc = fc+1
              elif tend in ["Final node"]:
                o = lep-1
                fm0 = np.array([[(-3*wv*length[o])/20],
                                [(-wv*length[o]**2)/30],
                                [(-7*wv*length[o])/20],
                                [(wv*length[o]**2)/20]])
                fms.append(fm0)
                pos1 = initial[o]*2
                pos2 = final[o]*2
                position = [pos1-1, pos1, pos2-1, pos2]
                gfm0 = np.zeros(((non*2),1))
                for j in range(4):
                    p1 = position[j]-1
                    gfm0[p1,0] = fm0[j,0]
                x1 = plot_x[initial[o]-1]
                y1 = plot_y[initial[o]-1]
                x2 = plot_x[final[o]-1]
                y2 = plot_y[final[o]-1]
                magc = abs(wv)
                while magc >= 100:
                  magc = magc/10
                FBD.create_text(x2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
                FBD.create_polygon(x1, y1, x2, y1-30-magc, x2, y2, outline="red", fill="")
                fc = 0
                while x1+fc*20 <= x2:
                  x = x1+fc*20
                  y = ((y1-30-magc)/((x2-x1)))*(x-x1)
                  print(x, y)
                  if wv < 0:
                    FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="last")
                  elif wv > 0:
                    FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="first")
                  fc = fc+1
  
          elif load_type in ["Distributed Load [IT]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/4],
                            [(-5*wv*length[o]**2)/96],
                            [(-wv*length[o])/4],
                            [(5*wv*length[o]**2)/96]])
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              magc = abs(wv)
              while magc >= 100:
                magc = magc/10
              FBD.create_text((x1+x2)/2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
              FBD.create_polygon(x1, y1, (x1+x2)/2, y1-30-magc, x2, y2, outline="red", fill="")
              fc = 0
              while x1+fc*20 <= (x1+x2)/2:
                x = x1+fc*20
                y = ((y1-30-magc)/((x2-x1)/2))*(x-x1)
                print (x, y)
                if wv < 0:
                  FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="last")
                if wv > 0:
                  FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="first")
                fc=fc+1
              while x1+fc*20 <= x2:
                x = x1+fc*20
                y = ((y1-30-magc)/((x2-x1)/2))*(x-x2)
                print(x, y)
                if wv < 0:
                  FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="last")
                if wv > 0:
                  FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="first")
                fc = fc+1
                pass

          elif load_type in ["Distributed Load [P]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/3],
                            [(-wv*length[o]**2)/15],
                            [(-wv*length[o])/3],
                            [(wv*length[o]**2)/15]]) 
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]

          elif load_type in ["Concentrated Load [1]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # P_e.append(pv_ol[i].get())
              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-P)/2],
                            [(-P*length[o])/8],
                            [(-P)/2],
                            [(P*length[o])/8]])
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xl = (x1+x2)/2
              yl = (y1+y2)/2
              if P > 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
                
          elif load_type in ["Concentrated Load [2]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # av_e.append(av_ol[i].get())                     
              # bv_e.append(bv_ol[i].get())                     
              # P_e.append(pv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i].get())               # av = a value of load
              bv = float(bv_ol[i].get())               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[((-P*bv**2)*(length[o]+(2*av)))/(length[o]**3)],
                            [(-P*av*(bv**2))/(length[o]**2)],
                            [((-P*(av**2))*(length[o]+(2*bv)))/(length[o]**3)],
                            [(P*(av**2)*bv)/(length[o]**2)]]) 
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xl = x1+((av/length[o])*(x2-x1))
              yl = y1
              if P > 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")

          elif load_type in ["Concentrated Load [3]"]:
            lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # alp_e.append(alpv_ol[i].get())                     
              # P_e.append(pv_ol[i].get())
              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i].get())             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[-P],
                            [-alp*(1-alp)*P*length[o]],
                            [-P],
                            [alp*(1-alp)*P*length[o]]]) 
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xcoe = (alp/length[o])*(x2-x1)
              xl1 = x1+xcoe
              xl2 = x2-xcoe
              yl = y1
              if P > 0:
                FBD.create_line(xl1, yl, xl1, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_line(xl2, yl, xl2, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl1, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
                FBD.create_text(xl2, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl1, yl, xl1, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_line(xl2, yl, xl2, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl1, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
                FBD.create_text(xl2, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")

        elif sstructure.structureType == "Frame":
          lm = np.zeros((non*3,1))
          if load_type in ["Vertical Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-2] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag < 0:
                FBD.create_line(x, y-40, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x+10, y-50, text=str(mag))
              elif mag > 0:
                FBD.create_line(x, y+40, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x+10, y+50, text=str(abs(mag)))

          elif load_type in ["Horizontal Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-3] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag < 0:
                FBD.create_line(x+40, y, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x+50, y-10, text=str(abs(mag)))
              elif mag > 0:
                FBD.create_line(x-40, y, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x-50, y-10, text=str(mag))

          elif load_type in ["Moment"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-1] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag > 0:
                FBD.create_line(x-15, y-5, x-5, y-15, x+5, y-15, x+15, y-5, x+15, y+5, x+5, y+15, x-5, y+15, fill="red", smooth=1, arrow="first")
                FBD.create_text(x+10, y-25, text=str(abs(mag)), fill="red", font="Aereal 10 bold")
              elif mag < 0:
                FBD.create_line(x-15, y-5, x-5, y-15, x+5, y-15, x+15, y-5, x+15, y+5, x+5, y+15, x-5, y+15, fill="red", smooth=1, arrow="last")
                FBD.create_text(x+10, y-25, text=str(abs(mag)), fill="red", font="Aereal 10 bold")

          elif load_type in ["Distributed Load [R]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/2],
                            [(-wv*length[o]**2)/12],
                            [(-wv*length[o])/2],
                            [(wv*length[o]**2)/12]]) 
              fms.append(fm0)
              pos1 = initial[o]*3
              pos2 = final[o]*3
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*3),1))
              for j in range(4):
                p1 = position[j]-1
                gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              magc = abs(wv)
              while magc >= 100:
                magc = magc/10
              if y1 == y2:
                FBD.create_text((x1+x2)/2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
                FBD.create_line(x1,y1-30-magc,x2,y2-30-magc, fill='red', width=1)
                fc = 0
                while x1+fc*20 <= x2:
                  if wv < 0:
                    FBD.create_line(x1+fc*20, y1-30-magc, x1+fc*20, y1, fill='red', width=1, arrow='last')
                  else:
                    FBD.create_line(x1+fc*20, y1-30-magc, x1+fc*20, y1, fill='red', width=1, arrow='first')
                  fc=fc+1
              else:
                pass

          elif load_type in ["Distributed Load [RT]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              tend = str(RTD[i].get())
              if tend == 0:
                pass
              elif tend in ["Initial node"]:
                o = lep-1
                fm0 = np.array([[(-7*wv*length[o])/20],
                                [(-wv*length[o]**2)/20],
                                [(-3*wv*length[o])/20],
                                [(wv*length[o]**2)/30]])
                fms.append(fm0)
                pos1 = initial[o]*3
                pos2 = final[o]*3
                position = [pos1-1, pos1, pos2-1, pos2]
                gfm0 = np.zeros(((non*3),1))
                for j in range(4):
                    p1 = position[j]-1
                    gfm0[p1,0] = fm0[j,0]
                x1 = plot_x[initial[o]-1]
                y1 = plot_y[initial[o]-1]
                x2 = plot_x[final[o]-1]
                y2 = plot_y[final[o]-1]
                magc = abs(wv)
                while magc >= 100:
                  magc = magc/10
                FBD.create_text(x1, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
                FBD.create_polygon(x1, y1, x1, y1-30-magc, x2, y2, outline="red", fill="")
                fc = 0
                while x1+fc*20 <= x2:
                  x = x1+fc*20
                  y = ((y1-30-magc)/((x2-x1)))*(x-x2)
                  print(x, y)
                  if wv < 0:
                    FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="last")
                  elif wv > 0:
                    FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="first")
                  fc = fc+1
              elif tend in ["Final node"]:
                o = lep-1
                fm0 = np.array([[(-3*wv*length[o])/20],
                                [(-wv*length[o]**2)/30],
                                [(-7*wv*length[o])/20],
                                [(wv*length[o]**2)/20]])
                fms.append(fm0)
                pos1 = initial[o]*3
                pos2 = final[o]*3
                position = [pos1-1, pos1, pos2-1, pos2]
                gfm0 = np.zeros(((non*3),1))
                for j in range(4):
                    p1 = position[j]-1
                    gfm0[p1,0] = fm0[j,0]
                x1 = plot_x[initial[o]-1]
                y1 = plot_y[initial[o]-1]
                x2 = plot_x[final[o]-1]
                y2 = plot_y[final[o]-1]
                magc = abs(wv)
                while magc >= 100:
                  magc = magc/10
                FBD.create_text(x2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
                FBD.create_polygon(x1, y1, x2, y1-30-magc, x2, y2, outline="red", fill="")
                fc = 0
                while x1+fc*20 <= x2:
                  x = x1+fc*20
                  y = ((y1-30-magc)/((x2-x1)))*(x-x1)
                  print(x, y)
                  if wv < 0:
                    FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="last")
                  elif wv > 0:
                    FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="first")
                  fc = fc+1
  
          elif load_type in ["Distributed Load [IT]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/4],
                            [(-5*wv*length[o]**2)/96],
                            [(-wv*length[o])/4],
                            [(5*wv*length[o]**2)/96]])
              fms.append(fm0)
              pos1 = initial[o]*3
              pos2 = final[o]*3
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*3),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              magc = abs(wv)
              while magc >= 100:
                magc = magc/10
              FBD.create_text((x1+x2)/2, y1-40-magc, text=abs(wv), fill="red", font="Aereal 10 bold")
              FBD.create_polygon(x1, y1, (x1+x2)/2, y1-30-magc, x2, y2, outline="red", fill="")
              fc = 0
              while x1+fc*20 <= (x1+x2)/2:
                x = x1+fc*20
                y = ((y1-30-magc)/((x2-x1)/2))*(x-x1)
                print (x, y)
                if wv < 0:
                  FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="last")
                if wv > 0:
                  FBD.create_line(x, y, x, y1, fill='red', width=1, arrow="first")
                fc=fc+1
              while x1+fc*20 <= x2:
                x = x1+fc*20
                y = ((y1-30-magc)/((x2-x1)/2))*(x-x2)
                print(x, y)
                if wv < 0:
                  FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="last")
                if wv > 0:
                  FBD.create_line(x, -y, x, y1, fill='red', width=1, arrow="first")
                fc = fc+1
                pass

          elif load_type in ["Distributed Load [P]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # wv_e.append(wv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i].get())               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-wv*length[o])/3],
                            [(-wv*length[o]**2)/15],
                            [(-wv*length[o])/3],
                            [(wv*length[o]**2)/15]]) 
              fms.append(fm0)
              pos1 = initial[o]*3
              pos2 = final[o]*3
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*3),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]

          elif load_type in ["Concentrated Load [1]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # P_e.append(pv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[(-P)/2],
                            [(-P*length[o])/8],
                            [(-P)/2],
                            [(P*length[o])/8]])
              fms.append(fm0)
              pos1 = initial[o]*3
              pos2 = final[o]*3
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*3),1))
              for j in range(4):
                p1 = position[j]-1
                gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xl = (x1+x2)/2
              yl = (y1+y2)/2
              if P > 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")

          elif load_type in ["Concentrated Load [2]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(el_ol[i].get())               # lep = load element point
            if lep == 0:
              pass
            else:
              # av_e.append(av_ol[i].get())                     
              # bv_e.append(bv_ol[i].get())                     
              # P_e.append(pv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i].get())               # av = a value of load
              bv = float(bv_ol[i].get())               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[((-P*bv**2)*(length[o]+(2*av)))/(length[o]**3)],
                            [(-P*av*(bv**2))/(length[o]**2)],
                            [((-P*(av**2))*(length[o]+(2*bv)))/(length[o]**3)],
                            [(P*(av**2)*bv)/(length[o]**2)]]) 
              fms.append(fm0)
              pos1 = initial[o]*3
              pos2 = final[o]*3
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*3),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xl = x1+((av/length[o])*(x2-x1))
              yl = y1
              if P > 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl, yl, xl, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")

          elif load_type in ["Concentrated Load [3]"]:
            # lep_e.append(el_ol[i].get())                     
            lep = int(lep_e[i])               # lep = load element point
            if lep == 0:
              pass
            else:
              # alp_e.append(alpv_ol[i].get())                     
              # P_e.append(pv_ol[i].get())

              lnp = int(node_ol[i])               # lnp = load node point
              mag = float(mag_ol[i])             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i].get())             # alp = alpha value of load
              P = float(pv_ol[i].get())                 # P = P value of load
              o = lep-1
              fm0 = np.array([[-P],
                            [-alp*(1-alp)*P*length[o]],
                            [-P],
                            [alp*(1-alp)*P*length[o]]]) 
              fms.append(fm0)
              pos1 = initial[o]*2
              pos2 = final[o]*2
              position = [pos1-1, pos1, pos2-1, pos2]
              gfm0 = np.zeros(((non*2),1))
              for j in range(4):
                  p1 = position[j]-1
                  gfm0[p1,0] = fm0[j,0]
              x1 = plot_x[initial[o]-1]
              y1 = plot_y[initial[o]-1]
              x2 = plot_x[final[o]-1]
              y2 = plot_y[final[o]-1]
              xcoe = (alp/length[o])*(x2-x1)
              xl1 = x1+xcoe
              xl2 = x2-xcoe
              yl = y1
              if P > 0:
                FBD.create_line(xl1, yl, xl1, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_line(xl2, yl, xl2, yl-40, fill="#EF4040", width=3, arrow="last")
                FBD.create_text(xl1, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
                FBD.create_text(xl2, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
              elif P < 0:
                FBD.create_line(xl1, yl, xl1, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_line(xl2, yl, xl2, yl-40, fill="#EF4040", width=3, arrow="first")
                FBD.create_text(xl1, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
                FBD.create_text(xl2, yl-50, text=str(abs(P)), fill="#EF4040", font="Aereal 10 bold")
 
        elif sstructure.structureType == "Grid":
          lm = np.zeros((non*3,1))
          if load_type in ["Vertical Load"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-3] = mag
              gfm0 = lm
              x = plot_x[lnp-1]
              y = plot_y[lnp-1]
              if mag < 0:
                FBD.create_line(x, y-40, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x, y-50, text=str(abs(mag)), fill="red", font="Aereal 10 bold")
              elif mag > 0:
                FBD.create_line(x, y+40, x, y, fill='#EF4040', width=3, arrow="last")
                FBD.create_text(x, y+50, text=str(abs(mag)), fill="red", font="Aereal 10 bold")

          if load_type in ["Moment (x-axis)"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-2] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag > 0:
                FBD.create_line(x-20, y+20, x-20, y, x+10, y-30, x+10, y-10, fill="red", smooth=1, arrow="first")
                FBD.create_text(x-35, y-15, text=str(abs(mag)), fill="red", font="Aereal 10 bold")
              elif mag < 0:
                FBD.create_line(x-20, y+20, x-20, y, x+10, y-30, x+10, y-10, fill="red", smooth=1, arrow="last")
                FBD.create_text(x-35, y-15, text=str(abs(mag)), fill="red", font="Aereal 10 bold")


          if load_type in ["Moment (z-axis)"]:
            lnp_e.append(node_ol[i].get())                     
            lnp = int(lnp_e[i])               # lnp = load node point
            if lnp == 0:
              pass
            else:
              # mag_e.append(mag_ol[i].get())      
                  
              lep = int(el_ol[i])               # lep = load element point
              mag = float(mag_ol[i].get())             # mag = load magnitude
              wv = float(wv_ol[i])               # wv = w value of load
              av = float(av_ol[i])               # av = a value of load
              bv = float(bv_ol[i])               # bv = b value of load
              alp = float(alpv_ol[i])             # alp = alpha value of load
              P = float(pv_ol[i])                 # P = P value of load
              lm[lnp*3-1] = mag
              gfm0 = lm
              x = plot_x [lnp-1]
              y = plot_y [lnp-1]
              if mag > 0:
                FBD.create_line(x-20, y, x-15, y-15, x+15, y-15, x+20, y, fill="maroon", smooth=1, arrow="first")
                FBD.create_text(x+20, y-25, text=str(abs(mag)), fill="maroon", font="Aereal 10 bold")
              elif mag < 0:
                FBD.create_line(x-20, y, x-15, y-15, x+15, y-15, x+20, y, fill="maroon", smooth=1, arrow="last")
                FBD.create_text(x+20, y-25, text=str(abs(mag)), fill="maroon", font="Aereal 10 bold")

        gfms.append(gfm0)
        tgfms = sum(gfms)
        print (gfms)
        print (tgfms)

        tsms = tgsm
        lm1 = tgfms
      for i in range(nos-1, -1, -1):
        snp = int(node_os[i].get())
        sup_type = str(s_type[i].get())
        sor = str(s_orient[i].get())
        if sstructure.structureType == "Truss":
          if sup_type in ["Roller"]:
            if sor in ["Vertical(+)"] or sor in ["Vertical(-)"] :
              tsms = np.delete(tsms, snp*2-1, 0)
              tsms = np.delete(tsms, snp*2-1, 1)
              lm1 = np.delete(lm1, snp*2-1, 0)
              dimf[snp*2-1] = 0
            elif sor in ["Horizontal(+)"] or sor in ["Horizontal(-)"]:
              tsms = np.delete(tsms, snp*2-2, 0)
              tsms = np.delete(tsms, snp*2-2, 1)
              lm1 = np.delete(lm1, snp*2-2, 0)
              dimf[snp*2-2] = 0
          else:
            tsms = np.delete(tsms, snp*2-1, 0)
            tsms = np.delete(tsms, snp*2-1, 1)
            lm1 = np.delete(lm1, snp*2-1, 0)
            tsms = np.delete(tsms, snp*2-2, 0)
            tsms = np.delete(tsms, snp*2-2, 1)
            lm1 = np.delete(lm1, snp*2-2, 0)
            dimf[snp*2-1] = 0
            dimf[snp*2-2] = 0

        elif sstructure.structureType == "Beam":
          if sup_type in ["Fixed"]:
            tsms = np.delete(tsms, snp*2-1, 0)
            tsms = np.delete(tsms, snp*2-1, 1)
            lm1 = np.delete(lm1, snp*2-1, 0)
            tsms = np.delete(tsms, snp*2-2, 0)
            tsms = np.delete(tsms, snp*2-2, 1)
            lm1 = np.delete(lm1, snp*2-2, 0)
            dimf[snp*2-1] = 0
            dimf[snp*2-2] = 0
          elif sup_type in ["Roller"]:
            if sor in ["Vertical(+)"] or sor in ["Vertical(-)"] :
              tsms = np.delete(tsms, snp*2-2, 0)
              tsms = np.delete(tsms, snp*2-2, 1)
              lm1 = np.delete(lm1, snp*2-2, 0)
              dimf[snp*2-2] = 0
            elif sor in ["Horizontal(+)"] or sor in ["Horizontal(-)"]:
              pass
          else:
            tsms = np.delete(tsms, snp*2-2, 0)
            tsms = np.delete(tsms, snp*2-2, 1)
            lm1 = np.delete(lm1, snp*2-2, 0)
            dimf[snp*2-2] = 0

        elif sstructure.structureType == "Frame":
          if sup_type in ["Fixed"]:
            tsms = np.delete(tsms, snp*3-1, 0)
            tsms = np.delete(tsms, snp*3-1, 1)
            lm1 = np.delete(lm1, snp*3-1, 0)
            tsms = np.delete(tsms, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-2, 1)
            lm1 = np.delete(lm1, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-3, 0)
            tsms = np.delete(tsms, snp*3-3, 1)
            lm1 = np.delete(lm1, snp*3-3, 0)
            dimf[snp*3-1] = 0
            dimf[snp*3-2] = 0
            dimf[snp*3-3] = 0
          elif sup_type in ["Pinned"]:
            tsms = np.delete(tsms, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-2, 1)
            lm1 = np.delete(lm1, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-3, 0)
            tsms = np.delete(tsms, snp*3-3, 1)
            lm1 = np.delete(lm1, snp*3-3, 0)
            dimf[snp*3-2] = 0
            dimf[snp*3-3] = 0
          elif sup_type in ["Roller"]:
            if sor in ["Vertical(+)"] or sor in ["Vertical(-)"]:
              tsms = np.delete(tsms, snp*3-2, 0)
              tsms = np.delete(tsms, snp*3-2, 1)
              lm1 = np.delete(lm1, snp*3-2, 0)
              dimf[snp*3-2] = 0
            elif sor in ["Horizontal(+)"] or sor in ["Horizontal(-)"]:
              tsms = np.delete(tsms, snp*3-3, 0)
              tsms = np.delete(tsms, snp*3-3, 1)
              lm1 = np.delete(lm1, snp*3-3, 0)
              dimf[snp*3-3] = 0

        elif sstructure.structureType == "Grid":
          if sup_type in ["Fixed"]:
            tsms = np.delete(tsms, snp*3-1, 0)
            tsms = np.delete(tsms, snp*3-1, 1)
            lm1 = np.delete(lm1, snp*3-1, 0)
            tsms = np.delete(tsms, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-2, 1)
            lm1 = np.delete(lm1, snp*3-2, 0)
            tsms = np.delete(tsms, snp*3-3, 0)
            tsms = np.delete(tsms, snp*3-3, 1)
            lm1 = np.delete(lm1, snp*3-3, 0)
            dimf[snp*3-1] = 0
            dimf[snp*3-2] = 0
            dimf[snp*3-3] = 0
          elif sup_type in ["Roller"]:
            if sor in ["Vertical(+)"] or sor in ["Vertical(-)"]:
              tsms = np.delete(tsms, snp*3-3, 0)
              tsms = np.delete(tsms, snp*3-3, 1)
              lm1 = np.delete(lm1, snp*3-3, 0)
              dimf[snp*3-3] = 0
            elif sor in ["Horizontal(+)"] or sor in ["Horizontal(-)"]:
              pass
          else:
            tsms = np.delete(tsms, snp*3-3, 0)
            tsms = np.delete(tsms, snp*3-3, 1)
            lm1 = np.delete(lm1, snp*3-3, 0)
            dimf[snp*3-3] = 0
        print (np.around(lm1,3))

      print (np.around(tsms,3))
      print (np.around(lm1,3))
      print (dimf)

      dism = np.matmul(np.linalg.inv(tsms),lm1)
      print ('Displacement Matrix is : ')
      print (dism)
       
      if sstructure.structureType == "Truss" or sstructure.structureType == "Beam":
        for i in range(len(dism)):
          for j in range(non*2):
            if dimf[j] == 1:
              dimf[j] = dism[i]
              break
            else:
              dimf[j] = dimf[j]

      elif sstructure.structureType == "Frame" or sstructure.structureType == "Grid":
        for i in range(len(dism)):
          for j in range(non*3):
            if dimf[j] == 1:
              dimf[j] = dism[i]
              break
            else:
              dimf[j] = dimf[j]

                  
      print ('Total displacement matrix is :')
      print (dimf)
      fm = np.matmul(tgsm,dimf)
      print (fm)

      
      for i in range(non):
        if sstructure.structureType == "Beam":
          coxf = cox[i]
          coyf = coy[i] + dimf[0+i*2]
        else:
          coxf = cox[i] + dimf[0+i*2]
          coyf = coy[i] + dimf[1+i*2]
        coxfs.append(coxf)
        coyfs.append(coyf)
        if sstructure.structureType == "Grid":
          yf = float(((coyf[0]+cy)*3/5)*scale)
          xf = float(((coxf[0]-cx)*scale)-yf)
        elif sstructure.structureType == "Beam":
          if abs(max(cox)) <= 10:
            xf = float((coxf[0]-cx)*scale*100)
            yf = float((coyf[0]+cy)*scale*100)
          elif abs(max(cox)) <= 20 and abs(max(cox)) > 10:
            xf = float((coxf[0]-cx)*scale*20)
            yf = float((coyf[0]+cy)*scale*20)
          elif abs(max(cox)) <= 50 and abs(max(cox)) > 20:
            xf = float((coxf[0]-cx)*scale*10)
            yf = float((coyf[0]+cy)*scale*10)
          else:
            xf = float((coxf[0]-cx)*scale)
            yf = float((coyf[0]+cy)*scale)
        else:
          # print("dimf adalah ", dimf[0+i*2], type(dimf))
          # print(coxf, type(coxf), "coxf adalah")
          # print(coyf, type(coyf), "coyf adalah")
          # print(cox, type(cox), "cox adalah")
          # print(coy, type(coy), "coy adalah")
          xf = float((coxf[0]-cx)*scale)
          yf = float(-(coyf[0]+cy)*scale)
          print(xf)
          print(yf)
        plot_xf.append(xf)
        plot_yf.append(yf)

        FBD.create_oval(xf-2, yf-2, xf+2, yf+2, fill="#FF9130")
      print(cox)
      print(coxfs)
      print(coy)
      print(coyfs)
      print(plot_x)
      print(plot_y)
      print(plot_xf)
      print(plot_yf)
      for i in range(noe):
        initial.append(int(e_initial[i].get()))
        final.append(int(e_final[i].get()))
        p1 = initial[i]-1
        p2 = final[i]-1
        x1 = plot_xf[p1]
        y1 = plot_yf[p1]
        x2 = plot_xf[p2]
        y2 = plot_yf[p2]
        L = math.sqrt((x2-x1)**2+(y2-y1)**2)
        theta_rad = math.asin((y2-y1)/L)
        pi = math.pi
        theta = theta_rad*180/pi
        sv = 0
        if theta != 0:
          sv = 15
        print(theta)
        ef_line = FBD.create_line(x1, y1 , x2, y2, fill="#FF9130", width=1, dash=(2,5))
        FBD.tag_raise(ef_line)
      if sstructure.structureType == "Truss":
        for i in range(noe):
          c = float(cosels[i])
          s = float(sinels[i])
          con2 = (float(cons1[i])/float(A[i]))* np.array([-c, -s, c, s])
          pos1 = initial[i]*2-1
          pos2 = final[i]*2-1
          position = [pos1-1, pos1, pos2-1, pos2]
          edm = np.zeros((4,1))
          for j in range(4):
            p1 = position[j]
            edm[j,0] = dimf[p1,0]
          soe = np.matmul(con2, edm) 
          edms.append(edm)
          print('Displacement matrix of element '+str(i+1)+' :')
          print(edm)
          print('Stress of element '+str(i+1)+' =', soe)
          soes.append(soe)
          cxf1 = coxfs [initial[i]-1]
          cxf2 = coxfs [final[i]-1]
          cyf1 = coyfs [initial[i]-1]
          cyf2 = coyfs [final[i]-1]
          if sstructure.structureType == 'Beam':
            L = coxfs[i+1]-coxfs[i]
          else:
            L = math.sqrt((cxf2[0]-cxf1[0])**2+(cyf2[0]-cyf1[0])**2)
          length_f.append(L)
          strain = (length_f[i]-length[i])/length[i]
          strains.append(strain)
          print('Strain of element '+str(i+1)+' =', strain)

        print(length)
        print(length_f)

        for i in range (non): 
          disp_var_text1 = tk.Label(disp_frame, text="u"+str(i+1), bg="#E5D4FF")
          disp_var_text1.grid(row=1+i*2, column=0, sticky="wen")
          disp_var_text2 = tk.Label(disp_frame, text="v"+str(i+1), bg="#C3ACD0")
          disp_var_text2.grid(row=2+i*2, column=0, sticky="wen")

          disp_val_text1 = tk.Label(disp_frame, text= str(dimf[0+i*2]), bg="#E5D4FF")
          disp_val_text1.grid(row=1+i*2, column=1, sticky="wen")
          disp_val_text2 = tk.Label(disp_frame, text= str(dimf[1+i*2]), bg="#C3ACD0")
          disp_val_text2.grid(row=2+i*2, column=1, sticky="wen")

        for i in range(noe):
          if i % 2 == 0:  
            bg_color = "#DDF2FD"
          else:
            bg_color = "#9AD0C2"
          ss_var_text1 = tk.Label(ss_frame, text=str(i+1), bg=bg_color)
          ss_var_text1.grid(row=1+i, column=0, sticky="wen")

          ss_val_text1 = tk.Label(ss_frame, text= str(soes[i]), bg=bg_color)
          ss_val_text1.grid(row=1+i, column=1, sticky="wen")
          ss_val_text2 = tk.Label(ss_frame, text= "["+str(strains[i])+"]", bg=bg_color)
          ss_val_text2.grid(row=1+i, column=2, sticky="wen")

      elif sstructure.structureType == "Beam":
        for i in range (non):
          disp_var_text1 = tk.Label(disp_frame, text="v"+str(i+1), bg="#E5D4FF")
          disp_var_text1.grid(row=1+i*2, column=0, sticky="wen")
          disp_var_text2 = tk.Label(disp_frame, text="\u03A6"+str(i+1), bg="#C3ACD0")
          disp_var_text2.grid(row=2+i*2, column=0, sticky="wen")

          disp_val_text1 = tk.Label(disp_frame, text= str(dimf[0+i*2]), bg="#E5D4FF")
          disp_val_text1.grid(row=1+i*2, column=1, sticky="wen")
          disp_val_text2 = tk.Label(disp_frame, text= str(dimf[1+i*2]), bg="#C3ACD0")
          disp_val_text2.grid(row=2+i*2, column=1, sticky="wen")

          stress_var_text1 = tk.Label(ss_frame, text="Fy"+str(i+1), bg="#9AD0C2")
          stress_var_text1.grid(row=1+i*2, column=0, sticky="wen")
          stress_var_text2 = tk.Label(ss_frame, text="M"+str(i+1), bg="#9AD0C2")
          stress_var_text2.grid(row=2+i*2, column=0, sticky="wen")

          stress_val_text1 = tk.Label(ss_frame, text= str(fm[0+i*2]), bg="#9AD0C2")
          stress_val_text1.grid(row=1+i*2, column=1, sticky="wen")
          stress_val_text2 = tk.Label(ss_frame, text= str(fm[1+i*2]), bg="#9AD0C2")
          stress_val_text2.grid(row=2+i*2, column=1, sticky="wen")

      elif sstructure.structureType == "Frame":
        for i in range (non):
          disp_var_text1 = tk.Label(disp_frame, text="u"+str(i+1), bg="#C3ACD0")
          disp_var_text1.grid(row=1+i*3, column=0, sticky="wen")
          disp_var_text2 = tk.Label(disp_frame, text="v"+str(i+1), bg="#C3ACD0")
          disp_var_text2.grid(row=2+i*3, column=0, sticky="wen")
          disp_var_text3 = tk.Label(disp_frame, text="\u03A6"+str(i+1), bg="#C3ACD0")
          disp_var_text3.grid(row=3+i*3, column=0, sticky="wen")

          disp_val_text1 = tk.Label(disp_frame, text= str(dimf[0+i*3]), bg="#C3ACD0")
          disp_val_text1.grid(row=1+i*3, column=1, sticky="wen")
          disp_val_text2 = tk.Label(disp_frame, text= str(dimf[1+i*3]), bg="#C3ACD0")
          disp_val_text2.grid(row=2+i*3, column=1, sticky="wen")
          disp_val_text3 = tk.Label(disp_frame, text= str(dimf[2+i*3]), bg="#C3ACD0")
          disp_val_text3.grid(row=3+i*3, column=1, sticky="wen")

          stress_var_text1 = tk.Label(ss_frame, text="Fx"+str(i+1), bg="#C1C283")
          stress_var_text1.grid(row=1+i*3, column=0, sticky="wen")
          stress_var_text2 = tk.Label(ss_frame, text="Fy"+str(i+1), bg="#9AD0C2")
          stress_var_text2.grid(row=2+i*3, column=0, sticky="wen")
          stress_var_text3 = tk.Label(ss_frame, text="M"+str(i+1), bg="#61C283")
          stress_var_text3.grid(row=3+i*3, column=0, sticky="wen")

          stress_val_text1 = tk.Label(ss_frame, text= str(fm[0+i*3]), bg="#C1C283")
          stress_val_text1.grid(row=1+i*3, column=1, sticky="wen")
          stress_val_text2 = tk.Label(ss_frame, text= str(fm[1+i*3]), bg="#9AD0C2")
          stress_val_text2.grid(row=2+i*3, column=1, sticky="wen")
          stress_val_text3 = tk.Label(ss_frame, text= str(fm[2+i*3]), bg="#61C283")
          stress_val_text3.grid(row=3+i*3, column=1, sticky="wen")
      
      elif sstructure.structureType == "Grid":
        for i in range (non):
          disp_var_text1 = tk.Label(disp_frame, text="v"+str(i+1), bg="#C3ACD0")
          disp_var_text1.grid(row=1+i*3, column=0, sticky="wen")
          disp_var_text2 = tk.Label(disp_frame, text="\u03A6"+str(i+1)+"x", bg="#C3ACD0")
          disp_var_text2.grid(row=2+i*3, column=0, sticky="wen")
          disp_var_text3 = tk.Label(disp_frame, text="\u03A6"+str(i+1)+"z", bg="#C3ACD0")
          disp_var_text3.grid(row=3+i*3, column=0, sticky="wen")

          disp_val_text1 = tk.Label(disp_frame, text= str(dimf[0+i*3]), bg="#C3ACD0")
          disp_val_text1.grid(row=1+i*3, column=1, sticky="wen")
          disp_val_text2 = tk.Label(disp_frame, text= str(dimf[1+i*3]), bg="#C3ACD0")
          disp_val_text2.grid(row=2+i*3, column=1, sticky="wen")
          disp_val_text3 = tk.Label(disp_frame, text= str(dimf[2+i*3]), bg="#C3ACD0")
          disp_val_text3.grid(row=3+i*3, column=1, sticky="wen")

          stress_var_text1 = tk.Label(ss_frame, text="Fy"+str(i+1), bg="#C1C283")
          stress_var_text1.grid(row=1+i*3, column=0, sticky="wen")
          stress_var_text2 = tk.Label(ss_frame, text="Mx"+str(i+1), bg="#9AD0C2")
          stress_var_text2.grid(row=2+i*3, column=0, sticky="wen")
          stress_var_text3 = tk.Label(ss_frame, text="Mz"+str(i+1), bg="#61C283")
          stress_var_text3.grid(row=3+i*3, column=0, sticky="wen")

          stress_val_text1 = tk.Label(ss_frame, text= str(fm[0+i*3]), bg="#C1C283")
          stress_val_text1.grid(row=1+i*3, column=1, sticky="wen")
          stress_val_text2 = tk.Label(ss_frame, text= str(fm[1+i*3]), bg="#9AD0C2")
          stress_val_text2.grid(row=2+i*3, column=1, sticky="wen")
          stress_val_text3 = tk.Label(ss_frame, text= str(fm[2+i*3]), bg="#61C283")
          stress_val_text3.grid(row=3+i*3, column=1, sticky="wen")
# ------------------------------------------------------------------------------------------------------------------------
     
      




  for child in input_frame.winfo_children():
    child.configure(background="#C7DAEA")
    
  for child in section_title1.winfo_children():
    wtype = child.winfo_class()
    if  wtype not in ("Entry", "Button"):
      child.configure(background="#C7DAEA")
    elif wtype in ("Button"):
      child.configure(background="#46EF63")


# -----------------------------------------------------------------------------------------------------------------------

master = tk.Tk()
master.title("Structural Analyzer")
master.geometry('500x565')
master.resizable(False, False)

current_dir = pathlib.Path(__file__).parent.resolve()
img_path1 = os.path.join(current_dir, "truss_icon.png")
img_path2 = os.path.join(current_dir, "beam_icon.png")
img_path3 = os.path.join(current_dir, "frame_icon.png")
img_path4 = os.path.join(current_dir, "grid_icon.png")
img_path5 = os.path.join(current_dir, "type_of_load.png")

truss_icon = ImageTk.PhotoImage(Image.open(img_path1))
beam_icon = ImageTk.PhotoImage(Image.open(img_path2))
frame_icon = ImageTk.PhotoImage(Image.open(img_path3))
grid_icon =  ImageTk.PhotoImage(Image.open(img_path4))


main_label = ttk.Label(master, text="SELECT TYPE OF STRUCTURE", font="TNR 18 bold")
main_label.pack()
space_label = ttk.Label(master)
space_label.pack()
masterframe = ttk.Frame(master)
masterframe.pack()

truss_btn = ttk.Button(masterframe, command= lambda: select_structure("truss_s"), image= truss_icon)
truss_btn.grid(row=0, column=0, sticky= "news")
truss_label = ttk.Label(masterframe, text="TRUSS", anchor=CENTER, font="TNR 14 bold")
truss_label.grid(row=1, column=0)

beam_btn = ttk.Button(masterframe, command= lambda: select_structure("beam_s"), image= beam_icon)
beam_btn.grid(row=0, column=2, sticky= "news")
beam_label = ttk.Label(masterframe, text="BEAM", anchor=CENTER, font="TNR 14 bold")
beam_label.grid(row=1, column=2)

blank_label_h = ttk.Label(masterframe, text=" ")
blank_label_h.grid(row=2, column=1)
blank_label_v = ttk.Label(masterframe, width=4)
blank_label_v.grid(row=2, column=1)

frame_btn = ttk.Button(masterframe, command= lambda: select_structure("frame_s"), image= frame_icon)
frame_btn.grid(row=3, column=0, sticky= "news")
frame_label = ttk.Label(masterframe, text="FRAME", anchor=CENTER, font="TNR 14 bold")
frame_label.grid(row=4, column=0)

grid_btn = ttk.Button(masterframe, command= lambda: select_structure("grid_s"), image= grid_icon)
grid_btn.grid(row=3, column=2, sticky="news")
grid_label = ttk.Label(masterframe, text="GRID", anchor=CENTER, font="TNR 14 bold")
grid_label.grid(row=4, column=2)

master.mainloop()
