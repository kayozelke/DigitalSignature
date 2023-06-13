# Autor

Imię i nazwisko, nr indeksu (na platformie ekursy)
Data wykonania: 6.06.2023

# Repozytorium

https://github.com/kayozelke/DigitalSignature

# Wywołanie skryptów

Utworzenie kluczy, podpisu
python A.py -filePath <ścieżka do pliku>

Weryfikacja podpisu
python B.py -filePath <ścieżka do pliku>

np.
PS: python A.py -filePath .\test_message_to_send.txt
Given filePath: .\test_message_to_send.txt
Signature created! Path: sharedfile/shared_signature.txt

PS: python B.py -filePath .\test_message_to_send.txt
Given filePath: .\test_message_to_send.txt
Files match!


Przed wywołaniem można usunąć zawartość folderów:
- keys
- shared_file

PROSZĘ NIE USUWAĆ WYMIENIONYCH FOLDERÓW, A JEDYNIE ICH ZAWARTOŚĆ.


# Opis działania

Część użytkownika A.

1. Wartości P i Q są wyznaczanie z wykorzystaniem TRNG zaimplementowanego w stronę "instaqram.pl", z poprzedniego sprawozdania. Fragment komentarza z kodu:
	- Liczby p i q są odnajdowane przez przeszukiwanie zawartości "trng_numbers.txt".
        - Liczba p jest przeszukiwana co bit dla wyrazu 512-bitowego od początku pliku
        - Liczba q jest przeszukiwana co bit dla wyrazu 512-bitowego od konca pliku
Jeśli liczby spełniają warunki liczb p i q, to są zapisywane do pamięci.

2. Obliczane są brakujące wartości, wyznaczane są klucze (folder "keys")
3. Wyznaczany jest skrót podanego w argumentach pliku i utworzony zostaje plik z podpisem (shared_sign/shared_signature.txt)

Część użytkownika B.

1. Odczytywany jest plik podawany w argumencie - plik, który jest podpisywany
2. Wyznaczany jest skrót podanego w argumentach pliku.
3. Następuje deszyfrowanie z użyciem klucza publicznego i weryfikacja.
