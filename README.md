# JWT Authentication Console Application

## 1. Përshkrimi i Projektit
Ky projekt implementon një sistem autentikimi dhe autorizimi duke përdorur **JSON Web Tokens (JWT)** në një model komunikimi Client-Server përmes Sockets. Siguria bazohet në algoritmin asimetrik **RS256 (RSA me SHA-256)**, ku Serveri përdor një çelës privat për të nënshkruar tokenin, ndërsa vërtetësia e tij mund të verifikohet përmes çelësit publik.

## 2. Pjesët e Implementuara
*   **generate_keys.py**: Gjeneron një çift çelësash RSA 2048-bit (`private_key.pem` dhe `public_key.pem`).
*   **server.py**:
    *   Pranon lidhjet nga klientët përmes sockets.
    *   Verifikon kredencialet e përdoruesit (Login).
    *   Lëshon JWT token të nënshkruar me Private Key me kohëzgjatje 30 minuta.
    *   Implementon middleware për verifikimin e tokenit para qasjes në resurse të mbrojtura.
*   **client.py**:
    *   Ofron ndërfaqen në konzollë për inputin e përdoruesit.
    *   Ruan tokenin e pranuar në memorie lokale.
    *   Dërgon kërkesa të autorizuara drejt serverit.

## 3. Udhëzimet e Ekzekutimit

### Parakushtet
Instaloni libraritë e nevojshme përmes terminalit:

py -m pip install -r requirements.txt

### Hapat e nisjes
Gjenerimi i çelësave: Ekzekutoni script-in për krijimin e çelësave RSA.

1. py generate_keys.py

2. Nisja e Serverit: 
   py server.py
   
3. Nisja e Klientit:
 Në një terminal të ri, startoni klientin dhe ndiqni udhëzimet.

        py client.py

4. Shembuj të Rezultateve 
    (Execution Output)
-----------------------------------------------------------
    Server Output:
    Plaintext

    [SERVER] Serveri u nis ne porten 5000... Duke pritur lidhje...

    [SERVER] Lidhje e re nga ('127.0.0.1', 50706)

    [SERVER] JWT u leshua me sukses per jane_doe

    [SERVER] Akses i lejuar per jane_doe

    [SERVER] Perdoruesi jane_doe u dekonektua.
-----------------------------------------------------------
    Client Output:
    Plaintext

    Enter username: jane_doe
    
    Enter password: password123

    Logged in. JWT token is: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...

    Enter command ('request_data' or 'logout'): request_data

    Protected data received: {"data": "Ky eshte nje resurs i mbrojtur nga serveri FIEK."}

    Enter command ('request_data' or 'logout'): logout

    Logging out...

5. Konfigurimi i Git

Projekti përfshin një fajll .gitignore për të parandaluar ngarkimin e fajllave të panevojshëm si __pycache__ dhe çelësave privatë, duke ruajtur kështu integritetin e repository-t në GitHub.  