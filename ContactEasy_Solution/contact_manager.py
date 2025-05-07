import json, csv
import pandas as pd
from IPython.display import display, clear_output

class ContactManager:
  """
  Questa classe si occupa di gestire i dati dei contatti, salvataggio/caricamento e la logica di ricerca, rimozione e modifica.
  """
  def __init__(self):
    self.contacts = {}  # inizializzo il dizionario vuoto: chiave nome, valore numero di telefono

  def add_contact(self, name, phone):
    """
    Aggiunge un nuovo contatto alla rubrica.
    Verifica che il nome e il numero non siano già presenti per evitare duplicati.
    Restituisce un messaggio descrittivo dell'esito.
    """
    dictres = self.search(name, phone)
    
    if not dictres:
       self.contacts[name] = phone
       return f"Contatto '{name}' aggiunto."
    else:
       if name in dictres and dictres[name]==phone:
          return f"Il contatto '{name}' associato al numero di telefono '{phone}' esiste già."
       elif name in dictres:
          return f"Il contatto '{name}' esiste già."
       elif phone in dictres.values():      
          key = next((k for k, v in dictres.items() if v == phone), None)
          return f"Il numero di telefono {phone} è già associato al nome '{key}' esiste già."
    
  def delete_contact(self, name, phone):
    """
    Eliminazione di un contatto.
    Il contatto se trovato viene eliminato dal file json.
    """
    strkey = ""
    dictres = self.search(name, phone)
    
    if not dictres:
       return False, f"Contatto '{name}' non trovato."

    if len(dictres) > 1:
        return False, "Più contatti trovati. Specificare meglio nome e numero."

    if name and phone and name in dictres and dictres[name]==phone:
         strkey = name
    elif name and name in dictres and len(dictres) == 1:
         strkey = name
    elif phone in dictres.values():
         key = next((k for k, v in dictres.items() if v == phone), None)
         strkey = key

    if strkey:
        del self.contacts[strkey]
        return True, f"Contatto '{strkey}' eliminato."

    return False, "Impossibile determinare quale contatto eliminare."    
  
  def search(self, name="", phone=""):
    """
    Cerca contatti per nome o numero di telefono.
    La ricerca può essere anche parziale: ad esempio, se cerchi "mar", trova "Marco" e "Mario".
    Restituisce un dizionario con tutti i risultati parziali o esatti.
    """
    results = {}

    name = name.lower().strip()
    phone = phone.strip()

    for n, p in self.contacts.items():
        if (name and name in n.lower().strip()) or (phone and phone in p):
            results[n] = p

    return results

  def update_contact(self, old_name, new_name, old_phone, new_phone):
    """
    Aggiorna un contatto esistente.
    Prima elimina il contatto con nome e numero vecchi,
    poi aggiunge il nuovo nome e numero se la cancellazione è andata a buon fine.
    """
    bresult,strres = self.delete_contact(old_name, old_phone)
    
    if bresult:
        self.contacts[new_name] = new_phone
        return f"Contatto aggiornato."
    else:
        return strres

  def to_dataframe(self):
    """
    Converte la rubrica in un oggetto pandas DataFrame.
    Utile per la visualizzazione in Google Colab o per operazioni tabellari.
    """
    return pd.DataFrame(list(self.contacts.items()), columns=["Nome", "Telefono"])

  def save_json(self, path="contacts.json"):
    """
    Salva i contatti nel file JSON specificato.
    Il formato è { "Nome": "Telefono", ... }
    """
    with open(path, 'w') as f:
        json.dump(self.contacts, f, indent=4)

  def load_json(self, path="contacts.json"):
    """
    Carica i contatti da un file JSON.
    Se il file non esiste, inizializza un dizionario vuoto.
    """
    try:
        with open(path, 'r') as f:
            self.contacts = json.load(f)
    except FileNotFoundError:
        self.contacts = {}