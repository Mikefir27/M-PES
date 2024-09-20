import tkinter as tk
from tkinter import ttk, filedialog
import csv
import plotly.graph_objects as go
from plotly.graph_objs.layout import YAxis, XAxis, Margin

class Mech:
    def __init__(self, color, linetype='solid', bartype='solid'):
        if color in colors_html:
            self.color_name = color
            self.color_code = colors_html[color]
            self.linetype = linetype
            self.bartype = bartype
        else:
            raise ValueError(f"Color '{color}' is not in the list of available colors.")
        
        
# Global parameters
energylist = [0, 0]
#energydict2 = {}
refs = [0, 0]
#refs2 = []
S = [0, 0]
RCoord = [0, 0]
#RCoord2 = []
#colordict = {}
colorlist = []
mechs = [0, 0]
#mechs2 = {}
mechstypes = {}
Units = ['eV', 'eV']
#Units2 = 'eV'
Titles = [0, 0]
#Title2 = ''
linedict = {}
bardict = {}


# COLORS
colors_html = {
    'Red': '#FF0000',
    'Green': '#008000',
    'Blue': '#0000FF',
    'Yellow': '#FFFF00',
    'Orange': '#FFA500',
    'Purple': '#800080',
    'Pink': '#FFC0CB',
    'Brown': '#A52A2A',
    'Black': '#000000',
    'White': '#FFFFFF',
    'Gray': '#808080',
    'Cyan': '#00FFFF',
    'Magenta': '#FF00FF',
    'Lime': '#00FF00',
    'Olive': '#808000',
    'Navy': '#000080',
    'Teal': '#008080',
    'Maroon': '#800000',
    'Silver': '#C0C0C0',
    'Gold': '#FFD700'
}

# LINETYPES
linetypes = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']

# Create the main window
root = tk.Tk()
root.title("Potential Energy Diagram Input")
root.geometry('400x400')  # Set window size
root.config(bg='#f0f0f0')  # Light gray background for a modern look
 
 
# Create style for ttk widgets
style = ttk.Style(root)
style.configure('TButton', font=('Helvetica', 20), padding=10)
style.configure('TLabel', font=('Helvetica', 20), background='#f0f0f0')

 # Frame to hold dynamically created buttons
button_frame = tk.Frame(root, bg='#f0f0f0')
button_frame.pack(pady=20)

# Helper function to create a title label with spacing
def create_title_label(text):
    label = ttk.Label(root, text=text, font=('Helvetica', 20, 'bold'))
    label.pack(pady=10)
 
def readinput(ngraph): # Read info from CSV
    global energylist, refs, RCoord, Titles
    energydict = {}
    ref = []

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                T = next(reader)[0]
                print('TITLE = ', T)
                headers = next(reader)  # Skip headers
                RC = next(reader)  # Read gas phase energies
                headers = next(reader)  # Skip headers
                nPES = next(reader)  # Number of PES diagrams
                nPES = int(nPES[0])
                print(nPES)
                for i in range(nPES):
                    energy = next(reader)
                    fenergy = [float(num) for num in energy[1:]]
                    energydict[energy[0]] = fenergy
                    ref.append(energy[0])
                    print(i)
                refs[ngraph] = ref
                Titles[ngraph] = T
                RCoord[ngraph] = RC
                energylist[ngraph] = energydict
                create_ref_buttons(ngraph)


        except Exception as e:
            print(f"Error loading file: {e}")
    print('Titles', Titles)
    print('Energylist', energylist)
    print('Refs', refs)
    print('RCoord', RCoord)
    
    
def create_ref_buttons(ngraph):
    # Clear all existing buttons in button_frame (both ref and settings buttons)
    for widget in button_frame.winfo_children():
        print("WIDGET", widget.cget('text') )
        widget.destroy()

    # Create a button for each reference
    for item in refs[ngraph]:
        button = ttk.Button(button_frame, text=item, command=lambda item=item: set_ref(item, ngraph))
        button.pack(pady=5)
        
    # Recreate the settings button after reference buttons are created
    create_settings_button(ngraph)        
            
def set_ref(ref, ngraph):
    global S
    S[ngraph] = ref
    for widget in button_frame.winfo_children():
        if widget.cget('text') in refs[ngraph]:
            widget.destroy()
    button = ttk.Button(button_frame, text=f"Change Ref from mech {ngraph+1}", command=lambda: create_ref_buttons(ngraph))
    button.pack(pady=5)

def create_settings_button(ngraph):
    # Create the settings and conversion buttons after clearing the old ones
    button = ttk.Button(button_frame, text="Settings", command=lambda: settings_window(ngraph,mechs))
    button2 = ttk.Button(button_frame, text="Convert to kcal/mol", command=lambda: eVtokcal(ngraph))
    button3 = ttk.Button(button_frame, text="Load Second Mechanism", command=lambda: readinput(1))
    norm_button = ttk.Button(button_frame, text="Normalize", command=lambda: normalize(ngraph))
    
    button.pack(pady=5)
    button2.pack(pady=5)
    button3.pack(pady=5)
    norm_button.pack(pady=5)
            
def eVtokcal(ngraph):
    global Units
    conv = 23.060541945329334
    if Units[ngraph] == 'eV':
        for key in energylist[ngraph]:
            energylist[ngraph][key] = [energy * conv for energy in energylist[ngraph][key]]
        Units[ngraph] = 'kcal/mol'
    else:
        print('Units already in kcal/mol')
        
def normalize(ngraph):
    if S[ngraph] != 0:
        print(energylist[ngraph][S[ngraph]])
        Svalue = energylist[ngraph][S[ngraph]][0]
        for key in energylist[ngraph]:
            energylist[ngraph][key] = [energy - Svalue for energy in energylist[ngraph][key]]
    else:
        print("Please Select Reference")
        
def settings_window(ngraph, m):
    print(m[ngraph])
    if m[ngraph] == 0:
        colordict = {}
        setwin = tk.Toplevel(root)
        setwin.title(f'Settings for mech {ngraph+1}')
        setwin.config(bg='#f0f0f0')
        for i in range(len(refs[ngraph])):
            colordict[refs[ngraph][i]] = 0
        titles = [f'Mechanism {ngraph+1}', 'Color' ,'Linestyle', 'Barstyle']
        for i in range(len(titles)): # Print titles in window
            title = ttk.Label(setwin, text=titles[i])
            title.grid(row=0, column=i, padx=10, pady=5)
        for index, (key, en) in enumerate(energylist[ngraph].items()):
            label = ttk.Label(setwin, text=key)
            label.grid(row=index+1, column=0, padx=10, pady=5)
            # COLORS
            color_var = tk.StringVar(setwin)
            color_var.set('Red')
            colordict[key] = color_var
            color_menu = ttk.OptionMenu(setwin, color_var, list(colors_html.keys())[0], *colors_html.keys())
            color_menu.grid(row=index+1, column=1, padx=10, pady=5)
            # LINESTYLE
            line_var = tk.StringVar(setwin)
            line_var.set('solid')
            linedict[key] = line_var
            line_menu = ttk.OptionMenu(setwin, line_var, linetypes[0], *linetypes)
            line_menu.grid(row=index+1, column=2, padx=10, pady=5 )
            # BARSTYLE
            bar_var = tk.StringVar(setwin)
            bar_var.set('solid')
            bardict[key] = bar_var
            bar_menu = ttk.OptionMenu(setwin, bar_var, linetypes[0], *linetypes)
            bar_menu.grid(row=index+1, column=3, padx=10, pady=5)
    else:
        print('SECONDSETTINGS')
        colordict = {}
        setwin = tk.Toplevel(root)
        setwin.title(f'Settings for mech {ngraph+1}')
        setwin.config(bg='#f0f0f0')
        for i in range(len(refs[ngraph])):
            colordict[refs[ngraph][i]] = 0
        titles = [f'Mechanism {ngraph+1}', 'Color' ,'Linestyle', 'Barstyle']
        for i in range(len(titles)): # Print titles in window
            title = ttk.Label(setwin, text=titles[i])
            title.grid(row=0, column=i, padx=10, pady=5)
        for index, (key, en) in enumerate(energylist[ngraph].items()):
            label = ttk.Label(setwin, text=key)
            label.grid(row=index+1, column=0, padx=10, pady=5)
            # COLORS
            color_var = tk.StringVar(setwin)
            #print('m[ngraph]', m[ngraph])
            color_var.set(m[ngraph][key].color_name)
            colordict[key] = color_var
            color_menu = ttk.OptionMenu(setwin, color_var, m[ngraph][key].color_name, *colors_html.keys())
            color_menu.grid(row=index+1, column=1, padx=10, pady=5)
            # LINESTYLE
            line_var = tk.StringVar(setwin)
            line_var.set(m[ngraph][key].linetype)
            linedict[key] = line_var
            line_menu = ttk.OptionMenu(setwin, line_var, m[ngraph][key].linetype, *linetypes)
            line_menu.grid(row=index+1, column=2, padx=10, pady=5 )
            # BARSTYLE
            bar_var = tk.StringVar(setwin)
            bar_var.set(m[ngraph][key].bartype)
            bardict[key] = bar_var
            bar_menu = ttk.OptionMenu(setwin, bar_var, m[ngraph][key].bartype, *linetypes)
            bar_menu.grid(row=index+1, column=3, padx=10, pady=5)
    
    save_button = ttk.Button(setwin, text="Save", command=lambda: [save_settings(ngraph, colordict, linedict, bardict), setwin.destroy()])
    save_button.grid(row=len(energylist[ngraph])+1, column=1, columnspan=2, pady=10)
    
def save_settings(ngraph, color_vars, line_vars, bar_vars):
    m = {}
    for key, color_var in color_vars.items():
        selected_color = color_var.get()
        selected_line = line_vars[key].get()
        selected_bar = bar_vars[key].get()
        print(f"Selected color for {key}: {selected_color}")
        print(f"Selected linetype for {key}: {selected_line}")

        try:
            mech = Mech(selected_color, selected_line, selected_bar)
            m[key] = mech
            print(f"Created Mech for {key} with color {mech.color_name} and linetype {mech.linetype} (Code: {mech.color_code})")
        except ValueError as e:
            print(e)
    
    mechs[ngraph] = m
            
    
def goPES():
    reaction_coordinates = [(i+1)*2 for i in range(len(RCoord[0]))]
    fig = go.Figure(layout={
    'font': {
        'family': 'Helvetica',
        'size': 30
    }
})
    if refs[1] == 0:
        print("ONE GRAPH ONLY")
        try:
            fig.update_layout(
                title=Titles[0],
                yaxis_title=f'Relative Free Energy ({Units[0]})',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[-70, 50],
                xaxis=dict(
                    title='Mechanism 1',
                    tickmode='array',
                    tickvals=reaction_coordinates,
                    ticktext=RCoord[0],
                    side='bottom'
                )
            )
        except ValueError as e:
            print(e)

        for key in energylist[0]:
            for j in range(len(RCoord[0])):
                linex = [reaction_coordinates[j] - 0.5, reaction_coordinates[j], reaction_coordinates[j] + 0.5]
                liney = [energylist[0][key][j], energylist[0][key][j], energylist[0][key][j]]
                try:
                    fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[0][key].color_code, width=15, dash=mechs[0][key].bartype), name=f"{key}", legendgroup=f"{key}", showlegend=(j == 0), xaxis='x'))
                except:
                    print('Please select colors in Settings')
                    return
            for j in range(len(RCoord[0])-1):
                linex = [reaction_coordinates[j] + 0.5, reaction_coordinates[j+1] - 0.5]
                liney = [energylist[0][key][j], energylist[0][key][j+1]]
                fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[0][key].color_code, width=5, dash=mechs[0][key].linetype), name=f"{key}", legendgroup=f"{key}", showlegend=False, xaxis='x'))
            
            
    else:
        reaction_coordinates2 = [(i+1)*2 for i in range(len(RCoord[1]))]
        try:
            fig.update_layout(
                title=Titles[0],
                yaxis_title=f'Relative Free Energy ({Units})',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis_range=[-70, 50],
                xaxis=XAxis(
                    title=Titles[0],
                    tickmode='array',
                    tickvals=reaction_coordinates,
                    ticktext=RCoord[0],
                    side='bottom'
                ),
                xaxis2 = XAxis(title=Titles[1],
                    tickmode = 'array',
                    tickvals = reaction_coordinates2,
                    ticktext = RCoord[1],
                    side = 'top',
                    overlaying='x'
                 )
            )
        except ValueError as e:
            print(e)

        for key in energylist[0]:
            for j in range(len(RCoord[0])):
                linex = [reaction_coordinates[j] - 0.5, reaction_coordinates[j], reaction_coordinates[j] + 0.5]
                liney = [energylist[0][key][j], energylist[0][key][j], energylist[0][key][j]]
                try:
                    fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[0][key].color_code, width=15, dash=mechs[0][key].bartype), name=f"{key}", legendgroup=f"{key}", showlegend=(j == 0), xaxis='x'))
                except:
                    print('Please select colors in Settings')
                    return
            for j in range(len(RCoord[0])-1):
                linex = [reaction_coordinates[j] + 0.5, reaction_coordinates[j+1] - 0.5]
                liney = [energylist[0][key][j], energylist[0][key][j+1]]
                fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[0][key].color_code, width=5, dash=mechs[0][key].linetype), name=f"{key}", legendgroup=f"{key}", showlegend=False, xaxis='x'))
# second csv
        for key in energylist[1]:
            for j in range(len(RCoord[1])):
                linex = [reaction_coordinates2[j] - 0.5, reaction_coordinates2[j], reaction_coordinates2[j] + 0.5]
                liney = [energylist[1][key][j], energylist[1][key][j], energylist[1][key][j]]
                try:
                    fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[1][key].color_code, width=15, dash=mechs[1][key].bartype), name=f"{key}", legendgroup=f"{key}", showlegend=(j == 0), xaxis='x2'))
                except:
                    print('Please select colors in Settings')
                    return
            for j in range(len(RCoord[1])-1):
                linex = [reaction_coordinates2[j] + 0.5, reaction_coordinates2[j+1] - 0.5]
                liney = [energylist[1][key][j], energylist[1][key][j+1]]
                fig.add_trace(go.Scatter(mode='lines', x=linex, y=liney, line=dict(color=mechs[1][key].color_code, width=5, dash=mechs[1][key].linetype), name=f"{key}", legendgroup=f"{key}", showlegend=False, xaxis='x2'))
    fig.show()
        

# Create Load and Normalize buttons with improved layout
create_title_label("Potential Energy Diagram Input")
load_button = ttk.Button(root, text="Load from CSV", command=lambda: readinput(0))
plot_button = ttk.Button(root, text="Plot PES", command=goPES)

load_button.pack(pady=10)
plot_button.pack(pady=10)

# Run the main event loop
root.mainloop()