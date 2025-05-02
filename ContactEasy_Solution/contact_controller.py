import pandas as pd
from IPython.display import display, clear_output
from contact_interface import ContactInterface
from contact_manager import ContactManager

class ContactController:
    """
    Questa classe si occupa di associare gli eventi e interagire con il controller e l'interfaccia.
    """
    def __init__(self, interface: ContactInterface, manager: ContactManager):
        self.ui = interface
        self.model = manager
        self._connect_events()
        self.modifycontact = {}

    def _connect_events(self):
        self.ui.add_btn.on_click(self.add)
        self.ui.delete_btn.on_click(self.delete)
        self.ui.search_btn.on_click(self.search)
        self.ui.update_btn.on_click(self.update)
        self.ui.show_btn.on_click(self.show_all)

    def add(self, b):
        with self.ui.output:
            clear_output()
        self.ui.clear_msg()

        name = self.ui.name_input.value.strip()
        phone = self.ui.phone_input.value.strip()
        if name and phone:
            if self.ui.validate_inputs():
                msg = self.model.add_contact(name, phone)
                self.ui.show_message(msg)
        else:
            self.ui.show_message("Inserisci nome e telefono", color="red")

        self.ui.clear_inputs()

    def delete(self, b):
        self.ui.clear_msg()

        if self.modifycontact:            
            name = self.modifycontact.keys()
            phone = self.modifycontact.values()
        else:
            name = self.ui.name_input.value.strip()
            phone = self.ui.phone_input.value.strip()

        _,msg = self.model.delete_contact(name, phone)        
        self.ui.show_message(msg)

        with self.ui.output:
            clear_output()

        self.modifycontact = {}
        #self.ui.clear_inputs()

    def search(self, b):      

        self.ui.clear_msg()

        name = self.ui.name_input.value.strip()
        phone = self.ui.phone_input.value.strip()
        results = self.model.search(name, phone)

        self.modifycontact = results

        with self.ui.output:
            clear_output()
            if self.modifycontact:
                display(pd.DataFrame(self.modifycontact.items(), columns=["Nome", "Telefono"]))
            else:
                self.ui.show_message("Nessun contatto trovato.")

    def update(self, b):
        self.ui.clear_msg()

        if self.modifycontact:            
            name = self.modifycontact.keys()
            phone = self.modifycontact.values()
        else:
            msg = "Ricercare un conttato valido."

        old_name = name
        old_phone = phone
        if not self.ui.name_input.value.strip():
            new_name = name
        else:
            new_name = self.ui.name_input.value.strip()

        if not self.ui.phone_input.value.strip():
            new_phone = phone
        else:
            new_phone = self.ui.phone_input.value.strip()

        msg = self.model.update_contact(old_name, new_name, old_phone, new_phone)
        
        self.ui.show_message(msg)
        with self.ui.output:
            clear_output()

        self.modifycontact = {}
        #self.ui.clear_inputs()

    def show_all(self, b):
        self.ui.clear_msg()
        
        df = self.model.to_dataframe()
        self.ui.clear_inputs()

        with self.ui.output:
            clear_output()
            display(df)