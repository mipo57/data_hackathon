# Projekt na Data Hackathon 2019
Aby przebudować projekt 
```console
foo@bar:~$ docker-compose build
```
I następnie uruchomienie
```console
foo@bar:~$ docker-compose up
```
Stroma będzie pod adresem [http://localhost](http://localhost)

## Opis serwerów
1. database_api: Jest pośednikiem za pomocą którego frontend pobiera dane
2. frontend: Serwer podający stronę internetową
3. morfeusz2: System pomocniczy, nie używany w produkcji
4. process_text: System analizujący zapytania w języku naturalnym
5. reverseproxy: Serwer który rozdziela do jakiego serwera ma iść jakie zapytanie
