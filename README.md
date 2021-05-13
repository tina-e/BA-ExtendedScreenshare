# BA-CrossDeviceCommunication
## Shared Screen Region
User A - der Sharer - kann eine bestimmte Region seines Bildschirmes an User B - den Accessor - freigeben.  
Der Accessor kann diese Region einsehen und auch steuern.
### Hintergrund
#### *TODO: mehr zu collaborativem Arbeiten finden*

#### Collaboration - Kim et al.
- WYSIWIS vs. independent views of remote and local user

#### Collaboration - Tang and Minneman
- VideoWhiteboard allows users (sometimes) to work more closely than if they were in the same room

#### Collaboration - Pallot et al.
(Volltext fehlt noch) This paper presents the results and discusses the findings of a survey on collaboration barriers, built from a list of collaboration distance factors, which was conducted from June 2007 to June 2008. It also explores the role of Collaborative Working Environments (CWE) and collaboration tools in creating, compressing or bridging collaborative distances and raising or overcoming related collaboration barriers.

#### Remote Lehre - Chertoff and Thompson
- interaction is important
- students need to feel connected to their classroom
- techers have to be comfortable with the software -> software so einfach/usable wie möglich machen
- student should have the possibility to monitore their progress

#### Remote Lehre - Morgan
- actively taking part
- work with peers
- students take an active role, demonstrate their competency, aquire feedback

#### Remote Lehre - He et al.
- project collaboration verbessert:
  - Qualität
  - Effizient
- gut und wichtig: automatically (save and) sync

#### Warum Bildschirmregion? - Hawkey and Inkpen
- nearly no privacy possible in classical screen sharing
- trotzdem: screen sharing for collaboration gut, weil Leute in gewohnter Umgebung effizient arbeiten
- also: balance privacy of the sharer and control of the accessor

#### Ähnliche Anwendung - Begole et al.
- Umbauen einer einzelnen Single-User-Anwendung zu einer Multi-User-Anwendung

#### Ähnliche Anwendung - Berry et al.
- presenter (active): shares
- audience (passive): watches
- presenter may want to keep certain screen area or certain parts private / to do sth else parallel
- audience may want to see evth (not interested in evth going on on the presenter's screen) / follow the presenter easier (Pointer/Annotation)

#### Ähnliche Anwendung - Tee et al. (recht alt I think)
- others can point
- sharer can blurr
- shared region is marked

#### Ähnliche Anwendung - Masaki et al.
- Grabbing certains screen area and share it
- control and pointing possible
- Communication via Tablet and PC (sperrig; mir nicht ganz klar, was hier passiert)

#### Ähnliche Anwendung - Frees and Kessler
- "ShowMe"
- Capturing certain screen area and share it
- Learning-by-Doing: Control not possible, only annotation
- Multi-User possible

> "Neu"/Vorteile hier:
> - Dateien übertragen / Zwischenablage möglich statt nur Steuerung (?)
> - Nicht nur 1 Anwendung -> mehr Flexibilität

### Anforderungen
#### Remote Control
> Der Sharer gibt eine Region seines Bildschirms für den Accessor frei.
Der Accessor soll die Möglichkeit haben, aktiv einzugreifen.
Er kann Klicken, Eingaben machen und Dinge von seinem lokalen Gerät einfügen.
  - Empfangen eines Streams einer bestimmten Bildschirmregion (z.B. via GStreamer) *(möglich)*
  - Weitergeben von Mouse- und Keyboard-Events *(TODO: x2x, xrdp, fauxcon, uinput mapper, ...)*
  - Unabhängige Eingabe auf Sharer-Gerät *(zweiter Mouse Cursor möglich, unabgängige Keyboard-Eingabe bedingt möglich)*
  - Funktionierende Zwischenablage *(bedingt möglich)*

#### Neues Öffnen
> In der vom Sharer geteilten Bildschirmregion liegen Verknüpfungen zu Programmen und zu Dateien.
Der Accessor soll die Möglichkeit haben, beiden zu starten. Die geöffneten Fenster sollen dann wiederum vom Accessor gesteuert werden können.

- Registrierung, dass ein neues Fenster geöffnet wurde ausgehend von der geteilten Region
- Neues Gst-Window mit Programminhalt wird geöffnet (vermutlich nicht sinnvoll)
- ODER: Neues xpra-Window des Programms wird geöffnet
  - Sharer kann neues Fenster beliebig schließen/minimierenes
  - Sharer muss nicht zusätzlichen Platz auf seinem Screen freigeben/"opfern"
  - besser Qualität
  - unkompliziertere Übertragung und Verarbeitung der Input-Events als bei einem zweiten GStream
- ODER: Gst-Window ändert automatisch die Größe, um neues Fenster mit anzuzeigen
  - private Dinge vom Sharer könnten freigelegt werden
- ODER: Sharer wird aufgefordert, Gst-Window anzupassen
- Für File: File wird an den Accessor gesendet und lokal bei ihm geöffnet (sinnvoll?) *(senden von Files übers Netzwerk funktioniert ab bestimmter Größe)*
  - nicht nur Accessor kann Daten an den Sharer übermitteln, sondern auch anders rum
  - Accessor hat File auch noch nach der Session zur Verfügung
  - Zwei unabhängige Dateien existieren

#### Control Access (Sharer)
> Das Festlegen, welche Region geteilt wird und mit wem, soll für den Sharer so einfach wie möglich sein.
Auch während der Stream läuft soll diese Region für den Sharer klar ersichtlich sein.
Falls er die geteilte Region für sich privat braucht, ohne dass der Accessor diese weiterhin einsehen kann,
soll der Sharer die Möglichkeit haben, die geteilte Region frei auf seinem Bildschirm zu verschieben und zu skalieren.
Außerdem soll er den Stream pausieren können.

  - geteilte Region als "Fenster"
  - Auswahl des Accessors *(möglich)*
  - Größe und Position des Streams zu Beginn einfach festlegen (z.B. bestimmte Region "aufziehen") *(mit übergebenen Werten möglich)*
  - Markierung der geteilten Region auf dem Bildschirm des Sharers (z.B. farbiges Rechteck)
  - Größe und Position der geteilten Region "on-the-run" steuern (z.B. farbiges Rechteck bewegen/skalieren) *(mit übergebenen Werten möglich)*
  - Stream pausieren *(möglich)*

---

## Annotation-Tool for Screen Sharing
### Hintergrund
#### *TODO: Mehr zu Annotation finden*

#### Annotation - Kim et al.
- (mind.) 2 verwandte Arbeiten zu Annotation

#### Annotation - Kim et al. (Comparing pointing and drawing)
- Compared 4 cases: pointing/annotation on image/video
- annotations: require fewer inputs on expert side + less cognitive load on the local worker
- pointing on video required good verbal communication + annotations need to be erased after completing each step of task

#### Remote Lehre - Chertoff and Thompson
- interaction is important
- students need to feel connected to their classroom
- techers have to be comfortable with the software -> software so einfach/usable wie möglich machen
- student should have the possibility to monitore their progress

#### Remote Lehre - Morgan
- actively taking part
- work with peers
- students take an active role, demonstrate their competency, aquire feedback

#### Warum zeichnen? - Baudisch et al.
- Mouse Cursor kann man schwer folgen/nicht gut sichtbar

#### Ähnliche Anwendung - Frees and Kessler
- "ShowMe"
- Capturing certain screen area and share it
- Learning-by-Doing: Control not possible, only annotation
- Multi-User possible

### Anforderungen
- Screen Streaming
- Mouse Events übertragen
- Drawing
