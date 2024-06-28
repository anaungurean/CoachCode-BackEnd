# Proiect CoachCode Backend Flask

Acest proiect este construit folosind Flask și include mai multe module pentru gestionarea diferitelor funcționalități. Mai jos găsiți detalii despre fiecare modul principal și instrucțiuni pentru deploy.

## Modulele Principale

### 1. Auth

Modulul `auth` este responsabil pentru gestionarea autentificării și autorizării utilizatorilor. Include funcționalități pentru înregistrare, autentificare, resetare de parole și management de sesiuni.

### 2. Chatbot

Modulul `chatbot` oferă funcționalități de chat utilizator-utilizator și interacțiuni automate bazate pe inteligență artificială pentru suport sau întrebări frecvente.

### 3. Coding Practice

Modulul `codingpractice` facilitează practica pentru codare, oferind utilizatorilor exerciții, întrebări sau proiecte pentru a-și îmbunătăți abilitățile de programare.

### 4. Community

Modulul `community` permite utilizatorilor să interacționeze și să colaboreze în cadrul unei comunități. Include funcționalități precum forumuri, grupuri de discuții și partajarea resurselor.

### 5. CV Maker

Modulul `cvmaker` permite utilizatorilor să creeze și să gestioneze CV-uri personalizate. Include funcționalități pentru încărcarea de imagini, editare de texte și export în diferite formate.

### 6. Notification

Modulul `notification` gestionează notificările pentru utilizatori. Include funcționalități pentru trimiterea și gestionarea notificărilor legate de activități ale utilizatorilor sau actualizări ale aplicației.

### 7. Problem Submissions

Modulul `problemsubmissions` permite utilizatorilor să trimită și să gestioneze probleme sau întrebări tehnice. Include funcționalități pentru evaluare, feedback și urmărirea progresului.

### 8. Profile User

Modulul `profileuser` facilitează gestionarea profilurilor utilizatorilor. Include funcționalități pentru încărcarea și gestionarea informațiilor de profil, inclusiv fotografii și descrieri personale.

## Deploy

Pentru a face deploy-ul aplicației Flask, urmați acești pași:

1. **Instalare dependințe**: Asigurați-vă că aveți toate dependințele instalate. Puteți instala dependințele listate în `requirements.txt` folosind `pip install -r requirements.txt`.
   
2. **Configurare**: Verificați și actualizați fișierul `config.py` cu setările adecvate pentru mediul de deploy (de exemplu, setările de bază de date, cheile secrete etc.).

3. **Setare și pornire**: Setați variabila de mediu `FLASK_APP` pentru a indica fișierul principal al aplicației (de obicei `run.py` sau `app/__init__.py`) și apoi porniți serverul Flask.

    ```bash
    export FLASK_APP=run.py
    flask run
    ```

    Sau, dacă utilizați `python -m flask`:

    ```bash
    python -m flask run
    ```

4. **Accesare aplicație**: Accesați aplicația în browser la adresa `http://localhost:5000` sau la adresa specificată de serverul Flask.
