# uap_pro03 - Übersetzung von TRIPLA in TRAM-Code

Drittes Projekt des Moduls *Übersetzung und Analyse von Programmen*.

Name: Patrick Weil  
Matr.-Nr.: 1133410  
Kennung: s4paweil


## Anleitung zum Ausführen des Compilers

- Wie zuvor enthält *requirements.txt* (unverändert zu Projekt 2) alle erforderlichen Abhängigkeiten.
- In *main.py* kann im *main-Block* angegeben werden, welches Tripla-Programm übersetzt werden soll. Hierzu muss lediglich der Pfad zum Tripla-Programm angegeben werden.  
Die Methode *ast.to_code()* liefert den überstezten TRAM-Code zurück.
 - Ausgabe: Das Programm kann auf der Konsole ausgegeben oder in ein *.txt*-File geschrieben werden.
    - Ausgabe auf Konsole:  
        Die Methode *instruction.print_prog(tram_code)* printed das Programm auf der Konsole aus.
    - Ausgabe in File:  
        Die Methode *instruction.write_tramCode_to_file(tram_code)* schreibt den übersetzten Code in das File *tram_code.txt*. In dieser Methode kann selbstverständlich das File, in dem der TRAM-Code gespeichert werden soll, angepasst werden.


