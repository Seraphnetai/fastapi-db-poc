# aida360 - articles_tags

## Stworzenie środowiska
Aby zainstalować środowisko przez poetry należy uruchomić komendę
```bash
poetry install
```

TODO konfiguracja jak tworzyć w katalogu projektu `.venv`
Powinien utworzyć się folder `.venv`.

## Uruchomienie aplikacji
### uvicorn
Aby uruchomić aplikację z wykorzystaniem uvicorna najpierw nalezy wejść do poetry shella z poziomu głównego katalogu:

```bash
poetry shell
```
a następnie uruchomić komendę

```bash
uvicorn app.api:app --reload --port 8000
```

Numer portu można zmienić albo nie podawać go wcale, ponieważ domyślnie wynosi on 8000

### Praca w czasie rzeczywistym, automatyczne odświeżanie aplikacji w kontenerze

```bash
docker-compose up # obraz zostanie pobrany z rejestru
```

### Praca na kontenerze w trybie release

@TODO
```bash
docker-compose -f docker-compose-release.yml up # korzysta ze wskazanej wersji release'a, odpowiedni do testowania docelowej aplikacji, już bez zależności developerskich
```

### Przebudowanie aktualnego kontenera o zmiany wprowadzone w Dockerfile

```bash
./build-local-container.sh # zostanie zbudowany lokalnie obraz i uruchomiony przez docker-compose
```

### Wyczyszczenie `całego` środowisko lokalnego w Dockerze

**UWAGA! Czyści wszystkie kontenery, sieci, obrazy i cache z lokalnego środowiska. Nawet te spoza aplikacji.**

```bash
docker system prune
```

### Testy aplikacji uruchamiane lokalnie w kontenerze

- Testy możemy uruchomić zarówno przez docker-compose odpowiednio nadpisując `command`, `entrypoint` lub łącząc się w trybie CLI pod działający kontener localdev i wywołując w konsoli odpowiednie komendy.
- Dostępne komendy:
  - `poetry run python -m pytest tests/` - testy jednostkowe
  - `flake8 --ignore=E203 --benchmark app/` - testy zgodności ze standardem kodowania

## Opis działania aplikacji

<tutaj opis działania aplikacji>


### Obsługa klienta

#### Wymagane zmienne środowisko i konfiguracje dla klienta

TBD

## Aktualizacja infrastruktury GCP dla usługi

### Praca z terraform w środowisku lokalnym

- Konfigurację można testować poprzez `docker-compose-terraform.yml` odpowiednio wywołując komendy dla wskazanego obrazu i ustawionych lokalnie zmiennych środowiskowych.
- **UWAGA! Zmienne wrażliwe nie powinny być commitowane do repozytorium. Zachowujemy je lokalnie (np. w pliku .env) i w konfiguracji CI/CD w sekcji variables na Gitlabie.**
- **UWAGA! Nie uruchamiamy komendy `apply` w środowisku lokalnym dla projektów produkcyjnych.**

#### Inicjalizacja stanu terraform

```bash
docker compose -f docker-compose-terraform.yml run --rm text_to_speech_terraform init
```

#### Formatowanie kodu zgodnie ze standardem dla plików .tf

```bash
docker compose -f docker-compose-terraform.yml run --rm text_to_speech_terraform fmt
```

#### Walidacja konfiguracji w poszukiwaniu błędów

```bash
docker compose -f docker-compose-terraform.yml run --rm text_to_speech_terraform validate
```

#### Sporządzenie planu i porównanie go ze stanem na zdalnym magazynie

```bash
docker compose -f docker-compose-terraform.yml run --rm text_to_speech_terraform plan
```

---
# ETL
* opis projektu
* jakie dane pobieramy
* jaka jest częstotliwość pobierania danych

## Przydatne linki

1. Dokumentacja projektu na wiki
2. Dokumentacja API

## Struktura repozytorium
```

├── src                                   # Pliki źródłowe dla usług ETL wchodzących w skład projektu
|   |
|   ├── bigquery                          # Źródła usług Big Query
|   ├── cloud_function                    # Źródła usług Cloud Functions
|       |
|       └── cf_nazwa_funkcji              # Katalog ze źródłami dla konkretnej funkcji
|          ├── main.py                    # Kod funkcji
|          └── requirements.txt           # Plik konfiguracyjny z wymaganymi bibliotekami
|
|
├── terraform                             # Pliki konfiguracyjne projektu dla terraform
|
├── schematy                              # Pliki składające się na schematy architektury projektu
|
└── README.md                             # Dokumentacja repozytorium
```
