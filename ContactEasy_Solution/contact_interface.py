import ipywidgets as widgets
import json
import csv
import pandas as pd
from IPython.display import display, clear_output

class ContactInterface:
  """
  Questa classe si occupa di creare l'inrefaccia grafica e gestirla.
  Definizione dei widget, layout dell'interfaccia...
  """
  def __init__(self):
    self.output = widgets.Output()

    # ----------- widget
    # Button
    self.add_btn = widgets.Button(
        description="Aggiungi",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
    # self.add_button_file = widgets.Button(
    #     description="Carica contatti",
    #     layout=widgets.Layout(margin="10px 10px 10px 10px")
    # )
    self.search_btn = widgets.Button(
        description="Ricerca",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
    self.update_btn = widgets.Button(
        description="Modifica",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
    self.delete_btn = widgets.Button(
        description="Elimina",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
    self.show_btn = widgets.Button(
        description="Mostra tutti",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )

    # Campi input
    self.name_input = widgets.Text(placeholder="Nome del contatto", description="Nome:")
    self.phone_input = widgets.Text(placeholder="Numero di telefono", description="Telefono:")

    # Campi otput
    # self.label_output = widgets.HTML(layout=widgets.Layout(overflow="auto", width="100%", height="100px")) # Mi serve per visualizzare contenuti dinamici e supporta testo multilinea o contenuti più grandi
    # self.label_output.layout.visibility = 'hidden'
    self.output = widgets.Output()
    self.msg = widgets.HTML()

     # Layout
    self.input_layout = widgets.VBox([
      self.name_input, 
      self.phone_input, 
      self.msg, 
      self.output])
    self.button_layout = widgets.HBox([
        self.add_btn, 
        self.delete_btn, 
        self.search_btn, 
        self.update_btn, 
        self.show_btn])
    self.main_layout = widgets.VBox([self.input_layout, 
                                     self.button_layout])

  def display(self):
    """Mostra l'interfaccia grafica."""
    display(self.main_layout)

  def clear_inputs(self):
    self.name_input.value = ""
    self.phone_input.value = ""
    self.msg.value = ""

  def show_message(self, message, color="black"):
    self.msg.value = f"<span style='color:{color}'>{message}</span>"

  def validate_inputs(self):
    """Valida gli input dell'utente."""
    name = self.name_input.value.strip()
    phone = self.phone_input.value.strip()

    msg = ""

    if not phone.isdigit():
       msg = "Errore: Il numero di telefono deve contenere solo cifre."
    if len(phone) < 8 or len(phone) > 15:
       msg = "Errore: Il numero di telefono deve avere tra 8 e 15 cifre."
    self.show_message(msg)
    return msg==""

