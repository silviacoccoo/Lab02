def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

            num_sezioni = int(lines[0].strip())

            # Creiamo una lista di liste, dove la lista è una biblioteca e ogni sottolista rappresenta una sezione, che contiene dei libri
            biblioteca = [[] for _ in range(num_sezioni)]

            for line in lines[1:]:
                line = line.strip()
                if line:  # Salta righe vuote
                    titolo, autore, anno, pagine, sezione = line.split(',')
                    # Creiamo un dizionario per ogni libro
                    libro = {
                        'titolo': titolo,
                        'autore': autore,
                        'anno': int(anno),
                        'pagine': int(pagine),
                        'sezione': int(sezione)
                    }

                    if 1 <= int(sezione) <= num_sezioni: # Se la sezione è compresa
                        biblioteca[int(sezione) - 1].append(libro) # Aggiungiamo il libro alla lista di liste
                        # Posizioniamo il libro nell'indice corrispondente alla lista di liste, ricordandoci che il primo indice è 0
        return biblioteca # La funzione restituisce una lista di liste, cioè una biblioteca con le sezioni

    # Gestione degli errori
    except FileNotFoundError:
        print("Errore: File non trovato.")
        return None
    except Exception as e:
        print(f"Errore durante il caricamento: {e}")
        return None
    # TODO


def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    try:
        # Controlliamo se il titolo esiste già
        for sez in biblioteca:
            for libro in sez:
                if libro['titolo'].lower() == titolo.lower(): # Convertiamo tutto in minuscolo per evitare fraintendimenti
                    print("Errore: Titolo già presente nella biblioteca.")
                    return None # Se il titolo esiste già non ha senso che la funzione restituisca un valore

        # Controlliamo se la sezione esiste
        if sezione < 1 or sezione > len(biblioteca): # La lunghezza della lista biblioteca indica quante sezioni ha
            print("Errore: Sezione non esistente.")
            return None

        nuovo_libro = {
            'titolo': titolo,
            'autore': autore,
            'anno': anno,
            'pagine': pagine,
            'sezione': sezione
        }

        biblioteca[sezione - 1].append(nuovo_libro) # Aggiungiamo il nuovo libro alla lista di liste

        # Bisogna aggiornare il file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"\n{titolo},{autore},{anno},{pagine},{sezione}")

        return nuovo_libro # Se le condizioni sono rispettate, allora la funzione deve restituire il nuovo libro da aggiungere alla biblioteca

    except FileNotFoundError:
        print("Errore: File non trovato.")
        return None
    except Exception as e:
        print(f"Errore durante l'aggiunta: {e}")
        return None
    # TODO


def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    """Cerca un libro nella biblioteca dato il titolo"""
    for sezione in biblioteca: # Per ogni lista dentro la lista biblioteca
        for libro in sezione: # Per ogni dizionario
            if libro['titolo'].lower() == titolo.lower(): # Ricerca per titolo
                return f"{libro['titolo']}, {libro['autore']}, {libro['anno']}, {libro['pagine']}, {libro['sezione']}"

    return None
    # TODO


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    if sezione < 1 or sezione > len(biblioteca):
        print("Errore: Sezione non esistente.")
        return None

    # Estrae i titoli dalla sezione specificata
    titoli = [libro['titolo'] for libro in biblioteca[sezione - 1]]

    # Ordina alfabeticamente
    titoli.sort()

    return titoli
    # TODO


def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

