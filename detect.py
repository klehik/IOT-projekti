
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
from scanner import Scanner



# Application
def main():

    # Scanner object
    scanner = Scanner()


    # UI
    layout = [
            [sg.Text('SecuritySystem 7000', size=(30, 1), font=("Helvetica", 25))], 
            [sg.Button("Käynnistä valvonta", size=(30,3), font=('Helvetica', 15))],
            [sg.Button("Rekisteröidy", size=(30,3), font=('Helvetica', 15))]
            
            ]
            

    window = sg.Window("SecSystem 7000", layout, margins=(300,150))

    while True:
        # Button events
        event, values = window.read()
        
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break
        # Start surveillance
        if event == 'Käynnistä valvonta':
            
            scanner.scan()
            window.close()  
        # Registration            
        if event == 'Rekisteröidy':
            window.close()
            layout = [[sg.Text("Nimi", font=("Helvetica", 25)), sg.InputText(size=(20,4),font=("Helvetica", 20)), sg.Button("OK", font=('Helvetica', 12), bind_return_key=True)]]
            window = sg.Window("Rekisteröidy", layout, margins=(300,150))
            event, values = window.read()
            user = values[0]
            if event == "OK":
                print(user)
                scanner.scan_for_registration(user)
                window.close()
                main()
    
    



if __name__ == "__main__":
    main()
    