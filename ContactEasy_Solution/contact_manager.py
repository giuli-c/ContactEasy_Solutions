import pandas as pd, io, json
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
       return f"Contatto '{name}' aggiunto.", "green"
    else:
       if name in dictres and dictres[name]==phone:
          return f"Il contatto '{name}' associato al numero di telefono '{phone}' esiste già.", "red"
       elif name in dictres:
          return f"Il contatto '{name}' esiste già.", "red"
       elif phone in dictres.values():      
          key = next((k for k, v in dictres.items() if v == phone), None)
          return f"Il numero di telefono {phone} è già associato al nome '{key}' esiste già.", "red"
    
  def delete_contact(self, name, phone):
    """
    Eliminazione di un contatto.
    Il contatto se trovato viene eliminato dal file json.
    """
    name = name.strip()
    phone = phone.strip()
    strkey = ""
    
    if name == "" and phone == "":
        return False, "Specificare il contatto che si desidera eliminare.", "yellow"

    dictres = self.search(name, phone)

    if not dictres:
       return False, f"Contatto '{name or phone}' non trovato.", "red"

    if len(dictres) > 1:
        return False, "Più contatti trovati. Specificare nome o numero di telefono.", "yellow"

    # C'è un solo contatto e quindi lo recupero
    key, val = next(iter(dictres.items()))
    
    # Verifico che il contatto sia quello desiderato
    if (not name or name.lower() == key.lower()) and (not phone or phone == val):
        strkey = key
    else:
        return False, "Impossibile determinare quale contatto eliminare.", "red"

    del self.contacts[strkey]
    return True, f"Contatto '{strkey}' eliminato.", "green"
  
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
        return f"Contatto aggiornato.", "green"
    else:
        return strres

  def to_dataframe(self):
    """
    Converte la rubrica in un oggetto pandas DataFrame.
    Utile per la visualizzazione in Google Colab o per operazioni tabellari.
    """
    return pd.DataFrame(list(self.contacts.items()), columns=["Nome", "Telefono"])

  def save_file(self, format='json', path=None):
    """
    Salva i contatti nel formato specificato.
    """
    df = self.to_dataframe()
    try:
        if format == 'json':
            path = path or "contacts.json"
            with open(path, 'w') as f:
                json.dump(self.contacts, f, indent=4)

        elif format == 'csv':
            path = path or "contacts.csv"
            df.to_csv(path, index=False)

        elif format == 'xlsx':
            path = path or "contacts.xlsx"
            df.to_excel(path, index=False)

        return True, f"Contatti salvati in {format.upper()}."

    except Exception as e:
        return False, f"Errore durante il salvataggio: {e}"

  def load_file(self, uploaded_file):
    """
    Carica i contatti da un file caricato.
    Supporta: .json, .csv, .xlsx
    """
    for filename in uploaded_file:
        content = uploaded_file[filename]

        try:
            if filename.endswith('.json'):
                data = json.loads(content.decode('utf-8'))
                self.contacts = data
            elif filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
                df['nome'] = df['nome'].astype(str).str.strip()
                df['telefono'] = df['telefono'].astype(str).str.strip()
                self.contacts = dict(zip(df['nome'], df['telefono']))
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(content))
                df['nome'] = df['nome'].astype(str).str.strip()
                df['telefono'] = df['telefono'].astype(str).str.strip()
                self.contacts = dict(zip(df['nome'], df['telefono']))
            else:
                return False, f"Formato non supportato: {filename}"
        except Exception as e:
            return False, f"Errore nel caricamento: {e}"
    return True, f"Contatti caricati da {filename}"