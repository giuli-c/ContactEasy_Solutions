import pandas as pd
from IPython.display import display, clear_output
from contact_interface import ContactInterface
from contact_manager import ContactManager
import io, json

class ContactController:
    """
    Questa classe si occupa di associare gli eventi e interagire con il controller e l'interfaccia.
    """
    def __init__(self, interface: ContactInterface, manager: ContactManager):
        self.ui = interface
        self.model = manager
        self._connect_events()
        self.modifycontact = None

    def _connect_events(self):
        self.ui.add_btn.on_click(self.add)
        self.ui.delete_btn.on_click(self.delete)
        self.ui.search_btn.on_click(self.search)
        self.ui.update_btn.on_click(self.update)
        self.ui.show_btn.on_click(self.show_all)
        self.ui.save_file_btn.on_click(self.save_to_file)
        self.ui.load_file_btn.on_click(self.load_from_file)

    def add(self, b):
      try:
        with self.ui.output:
            clear_output()
        self.ui.clear_msg()

        name = self.ui.name_input.value.strip()
        phone = self.ui.phone_input.value.strip()
        if name and phone:
            if self.ui.validate_inputs():
                msg, color = self.model.add_contact(name, phone)
                self.ui.show_message(msg, color=color)
        else:
            self.ui.show_message("Inserisci nome e telefono", color="red")
      finally:
        self.ui.clear_inputs()
        self.ui.hide_modify_input() # nascondo la box di modifica se visibile

    def delete(self, b):
        try:
            self.ui.clear_msg()

            if self.modifycontact:            
                if len(self.modifycontact) == 1:
                    # Estraggo singolo nome e telefono
                    name, phone = next(iter(self.modifycontact.items()))
                else:
                    self.ui.show_message("Più contatti trovati. Specifica meglio la ricerca.", color="red")
                    return
            else:
                name = self.ui.name_input.value.strip()
                phone = self.ui.phone_input.value.strip()

            _,msg,color = self.model.delete_contact(name, phone)        
            self.ui.show_message(msg, color=color)
        finally:
            with self.ui.output:
                clear_output()

            self.modifycontact = None
            self.ui.hide_modify_input() # nascondo la box di modifica se visibile

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
                if len(self.modifycontact) == 1:
                    self.ui.show_modify_input()  # mostro i campi per la modifica
                else:
                    self.ui.hide_modify_input()
            else:
                self.ui.show_message("Nessun contatto trovato.", color="red")

    def update(self, b):
      try:
        self.ui.clear_msg()

        if self.modifycontact and len(self.modifycontact) == 1:
            # Estrai nome e telefono dal primo (unico) contatto
            old_name, old_phone = next(iter(self.modifycontact.items()))
        else:
            self.ui.show_message("Specifica un nome o numero di telefono valido e univoco per poter modificare il contatto.", color="red")
            return

        new_name = self.ui.new_name_input.value.strip() or old_name
        new_phone = self.ui.new_phone_input.value.strip() or old_phone

        msg,color = self.model.update_contact(old_name, new_name, old_phone, new_phone)
        self.ui.show_message(msg, color=color)
      finally:
        with self.ui.output:
            clear_output()

        self.modifycontact = None
        self.ui.clear_inputs()
        self.ui.hide_modify_input() # nascondo la box di modifica se visibile

    def show_all(self, b):
      try:
        self.ui.clear_msg()
        
        df = self.model.to_dataframe()
      finally:
        with self.ui.output:
            clear_output()
            display(df)
        self.ui.clear_inputs()
        self.ui.hide_modify_input() # nascondo la box di modifica se visibile

    def save_to_file(self, b):
      format_selected = self.ui.save_format.value
      success, msg = self.model.save_file(format_selected)
      self.ui.show_message(msg, color="green" if success else "red")    
    
    def load_from_file(self, b):
      # L'import per come è stato gestito può essere usato solo su Google Colab
      from google.colab import files
      uploaded = files.upload()

      success, msg = self.model.load_file(uploaded)
      self.ui.show_message(msg, color="green" if success else "red")