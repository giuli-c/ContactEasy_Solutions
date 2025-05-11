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
    self.load_file_btn = widgets.Button(
        description="Carica contatti da file",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
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
    self.save_file_btn = widgets.Button(
        description="Salva file",
        layout=widgets.Layout(margin="10px 10px 10px 10px")
    )
    
    # Campi input
    common_input_layout = widgets.Layout(width="300px")
    self.name_input = widgets.Text(description="Nome:", layout=common_input_layout, style={'description_width': '100px'})
    self.phone_input = widgets.Text(description="Telefono:", layout=common_input_layout, style={'description_width': '100px'})
    self.new_name_input = widgets.Text(description="Nuovo nome:", layout=common_input_layout, style={'description_width': '100px'})
    self.new_phone_input = widgets.Text(description="Nuovo telefono:", layout=common_input_layout, style={'description_width': '100px'})

    # Campi otput
    self.output = widgets.Output()
    self.msg = widgets.HTML()

    # Combo box per il salvataggio del file
    self.save_format = widgets.Dropdown(
      options=[('JSON', 'json'), ('CSV', 'csv'), ('Excel', 'xlsx')],
      value='json',
      description='Formato:',
      style={'description_width': 'initial'},
      layout=widgets.Layout(width='200px')
    )

    # Layout
    self.update_box = widgets.VBox([
      self.new_name_input,
      self.new_phone_input
    ])
    self.update_box.layout.display = 'none'

    self.input_layout = widgets.VBox([
      self.name_input, 
      self.phone_input,
      self.update_box, 
      self.msg, 
      self.output])
    self.button_layout1 = widgets.HBox([
        self.add_btn, 
        self.load_file_btn,
        self.delete_btn, 
        self.search_btn, 
        self.update_btn])
    self.button_layout2 = widgets.HBox([
        self.show_btn, 
        self.save_file_btn,
        self.save_format])
    self.main_layout = widgets.VBox([self.input_layout, 
                                     self.button_layout1,
                                     self.button_layout2])

  def display(self):
    """Mostra l'interfaccia grafica."""
    display(self.main_layout)

  def clear_inputs(self):
    self.name_input.value = ""
    self.phone_input.value = ""

  def clear_msg(self):
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

  def show_modify_input(self):
    self.update_box.layout.display = ''  # mostra il box per modifiche

  def hide_modify_input(self):
    self.update_box.layout.display = 'none'  # nasconde il box per modifiche
    self.new_name_input.value = ""
    self.new_phone_input.value = ""