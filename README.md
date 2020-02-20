# PostgreProject

Preferowana metoda uruchomienia tego projektu to:
1. Pobranie postgresa przez dockera i stworzenie kontenera, z którym nastąpi komunikacja
```
docker pull postgres:12
docker run -itd -e POSTGRES_PASSWORD=dayne --name posts -p 54320:5432 postgres:12
```
Komendy zostały zapisane przy założeniu posiadania dockera i dodaniu się do grupy dockera (aby nie używać sudo przy każdej komendzie)
Jeśli nie ma się w swoich grupach dockera (można to sprawdzić z id) kod nie będzie w stanie dokonać updata bazy danych - 
muszę być w stanie z poziomu pythona wykonać zmianę bazy danych, oczywiście bez uprawnień admina (sudo...)

2. Pobranie pythonowych bibliotek, w zależności od używanego package managera:
```
conda --file=requirements.txt # Zapuścić w folderze projektu - tam jest plik requirements.txt
```
albo
```
pip install -r requirements.txt # Zapuścić w folderze projektu - tam jest plik requirements.txt
```

3. Uruchomienie projektu
```
python flaskk/base.py # Z folderu projektu
```
