# 🎵 Pitch Range Detector

**Analiză gamă vocală / instrument offline**

Aplicație Windows cu interfață grafică modernă pentru detectarea și analiza gamei de frecvențe din fișiere audio.

## 📋 Caracteristici

- ✅ Încărcare fișiere audio (WAV, MP3, OGG, FLAC)
- ✅ Detectare automată frecvențe minime și maxime
- ✅ Conversie frecvențe → note muzicale (ex: A4, F#3)
- ✅ Afișare statistici:
  - Frecvența minimă (Hz + nota)
  - Frecvența maximă (Hz + nota)
  - Frecvența mediană (Hz + nota)
  - Gama în note (ex: C3 — G5)
  - Nivel de încredere a detecției
- ✅ Funcționare 100% offline
- ✅ Interfață grafică modernă și intuitivă (PyQt5)
- ✅ Algoritm robust de detectare pitch (librosa pYIN)

## 🚀 Instalare și Rulare

### Cerințe

- Python 3.8 sau mai nou
- Windows 10/11

### Instalare Dependențe

1. Deschide Command Prompt sau PowerShell în directorul proiectului

2. Instalează dependențele:
```bash
pip install -r requirements.txt
```

### Rulare Aplicație

```bash
python main.py
```


### Notă despre dimensiunea executabilului

Executabilul va avea aproximativ 200-400 MB datorită bibliotecilor numpy, scipy și librosa. Aceasta este normal pentru aplicații cu procesare audio avansată.

## 📖 Mod de Utilizare

1. **Pornește aplicația** - dublu-click pe `PitchRangeDetector.exe` sau rulează `python main.py`

2. **Deschide fișier audio** - Click pe butonul "📂 Deschide Fișier Audio" și selectează un fișier WAV, MP3, OGG sau FLAC

3. **Analizează** - Click pe butonul "🔍 Analizează" pentru a începe procesarea

4. **Vezi rezultatele** - Rezultatele vor apărea în secțiunea "Rezultate Analiză":
   - Frecvența minimă și nota corespunzătoare
   - Frecvența maximă și nota corespunzătoare
   - Frecvența mediană și nota corespunzătoare
   - Gama completă în note muzicale
   - Nivelul de încredere al detecției (%)

## 🎯 Cazuri de Utilizare

- **Analiza vocii**: Determină gama vocală (soprano, alto, tenor, bas)
- **Analiza instrumentelor**: Identifică gama frecvențelor unui instrument
- **Producție muzicală**: Verifică gama tonală a unor înregistrări
- **Educație muzicală**: Învață despre pitch și frecvențe

## 🛠️ Structura Proiectului

```
PitchRangeDetector/
├── main.py                      # Aplicația principală cu GUI
├── audio_analyzer.py            # Modul de analiză audio
├── requirements.txt             # Dependențe Python
├── PitchRangeDetector.spec     # Configurație PyInstaller
├── README.md                    # Acest fișier
└── .gitignore                   # Fișiere ignorate de Git
```

## 🔧 Tehnologii Utilizate

- **PyQt5**: Interfață grafică modernă
- **librosa**: Procesare și analiză audio profesională
- **numpy**: Calcule numerice eficiente
- **soundfile**: Citire fișiere audio

## 📝 Algoritm de Detecție

Aplicația folosește algoritmul **pYIN** (Probabilistic YIN) din librosa, care este:
- Robust la zgomot
- Precis pentru voce și instrumente melodice
- Oferă informații despre încrederea detecției
- Optimizat pentru gama frecvențelor umane (65 Hz - 2093 Hz)

## ⚠️ Limitări

- Funcționează cel mai bine cu surse melodice (voce, vioară, flaut, etc.)
- Poate avea dificultăți cu instrumente polifonice complexe (acorduri de pian)
- Precisiunea depinde de calitatea înregistrării audio
- Necesită sunet vocal/instrumental clar, fără zgomot excesiv

## 🐛 Troubleshooting

### Eroare la pornire: "DLL load failed"
- Reinstalează dependențele: `pip install --force-reinstall -r requirements.txt`

### Aplicația nu detectează frecvențe
- Verifică că fișierul audio conține sunet vocal sau instrumental clar
- Încearcă cu un fișier de test cunoscut (ex: o înregistrare vocală clară)

### Executabilul este prea mare
- Aceasta este normal - bibliotecile științifice ocupă mult spațiu
- Poți folosi versiunea cu fișiere separate în loc de --onefile

### Erori la compilare cu PyInstaller
- Asigură-te că ai ultima versiune: `pip install --upgrade pyinstaller`
- Folosește fișierul spec inclus: `pyinstaller PitchRangeDetector.spec`

## 📄 Licență

Acest proiect este open-source și disponibil pentru uz personal și educațional.

## 👨‍💻 Autor

Creat pentru analiza offline a gamei vocale și instrumentale.

---

**Versiune**: 1.0.0  
**Data**: 2025  
**Platform**: Windows 10/11
