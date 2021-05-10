# BA-CrossDeviceCommunication
## Shared Screen Region
User A - der Sharer - kann eine bestimmte Region seines Bildschirmes an User B - den Accessor - freigeben.  
Der Accessor kann diese Region einsehen und auch steuern.
### Hintergrund
### Anforderungen
#### Remote Control
> Der Sharer gibt eine Region seines Bildschirms für den Accessor frei.
Der Accessor soll die Möglichkeit haben, aktiv einzugreifen.
Er kann Klicken, Eingaben machen und Dinge von seinem lokalen Gerät einfügen.
  - Streamen einer Bildschirmregion (z.B. via GStreamer) *(möglich)*
  - Weitergeben von Mouse- und Keyboard-Events
  - Funktionierende Zwischenablage *(bedingt möglich)*


#### Neues Öffnen
> In der vom Sharer geteilten Bildschirmregion liegen Verknüpfungen zu Programmen und zu Dateien.
Der Accessor soll die Möglichkeit haben, beiden zu starten. Die geöffneten Fenster sollen dann wiederum vom Accessor gesteuert werden können.

- Registrierung, dass ein neues Fenster geöffnet wurde ausgehend von der geteilten Region
- Neues Gst-Window mit Programminhalt wird geöffnet *(möglich)*
  - Kein zusätzlicher Aufwand bei der Implementierung
- ODER: Neues xpra-Window des Programms wird geöffnet *(möglich)*
  - Sharer kann neues Fenster beliebig schließen/minimierenes
  - Sharer muss nicht zusätzlichen Platz auf seinem Screen freigeben/"opfern"
  - besser Qualität
  - unkompliziertere Übertragung und Verarbeitung der Input-Events als bei einem zweiten GStream
- Für File: File wird an den Accessor gesendet und lokal bei ihm geöffnet (sinnvoll?) *(senden von Files übers Netzwerk funktioniert ab bestimmter Größe)*
  - nicht nur Accessor kann Daten an den Sharer übermitteln, sondern auch anders rum
  - Accessor hat File auch noch nach der Session zur Verfügung
  - Zwei unabhängige Dateien existieren


#### Control Access (Sharer)
> Das Festlegen, welche Region geteilt wird, soll für den Sharer so einfach wie möglich sein.
Auch während der Stream läuft soll diese Region für den Sharer klar ersichtlich sein.
Falls er die geteilte Region für sich privat braucht, ohne dass der Accessor diese weiterhin einsehen kann,
soll der Sharer die Möglichkeit haben, die geteilte Region frei auf seinem Bildschirm zu verschieben und zu skalieren.
Außerdem soll er den Stream pausieren können.

  - Größe und Position des Streams zu Beginn einfach festlegen (z.B. bestimmte Region "aufziehen") *(mit übergebenen Werten möglich)*
  - Markierung der geteilten Region auf dem Bildschirm des Sharers (z.B. farbiges Rechteck)
  - Größe und Position der geteilten Region "on-the-run" steuern (z.B. farbiges Rechteck bewegen/skalieren) *(mit übergebenen Werten möglich)*
  - Stream pausieren *(möglich)*

---

## Annotation-Tool for Screen Sharing
### Hintergrund
### Anforderungen
