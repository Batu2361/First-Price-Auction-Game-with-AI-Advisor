# First-Price Auction Game with AI Advisor

[English](#english) | [Deutsch](#deutsch)

<a id="english"></a>
## English

### Project Overview
This project is a behavioral economics experiment built with oTree that simulates a first-price auction where players can choose between their own bid or an AI-generated bid (using Google's Gemini AI). The experiment is designed to study how people interact with AI recommendations in strategic decision-making scenarios.

This project was developed as part of a bachelor thesis at the Technical University of Berlin titled "The Use of Large Language Models in First-Price Auctions: Development of an oTree Experiment". The thesis examines how AI-based decision aids can influence strategic bidding behavior in experimental economic contexts.

### Abstract
This bachelor thesis investigates the use of Large Language Models (LLMs) in first-price auctions with a focus on developing an experimental framework using oTree. In experimental economic contexts, the question increasingly arises of how AI-based decision aids can influence strategic bidding behavior. This work conceptualizes and implements a flexible oTree experiment that enables various AI strategies such as risk-averse or basic bidding behavior through the integration of Google Gemini. Particular attention is paid to creating effective LLM prompts, dynamically adapting bidding strategies, and ensuring the technical robustness of the implementation. The developed framework not only allows the investigation of different delegation and advice modes but also offers possibilities for extension with additional strategies or alternative LLMs through its modular structure. The results of this work provide methodological foundations for future research on AI-supported decision-making in economic experiments and highlight potentials as well as limitations of using LLMs in experimental auction contexts.

### Game Mechanics
1. **Basic Setup**: Players are paired anonymously and participate in a first-price auction over multiple rounds.
2. **Valuation**: Each player receives a private valuation (between 50-100) for the auctioned item.
3. **Bidding Options**:
   - Players can place their own bid
   - Players can adopt a bid suggested by Gemini AI
   - In the "Adviser" variant, players see the AI suggestions and can decide to stick with their own bid or adjust it
4. **AI Strategies**:
   - **Basic Strategy**: Standard intelligent bidding approach
   - **Risk-Averse Strategy**: Conservative bidding approach that prioritizes avoiding losses
5. **Results**: The highest bidder wins the item and earns a payoff based on their valuation minus their bid
6. **Final Payment**: One round is randomly selected for final payment calculation

### Required Tools and Dependencies

#### Software Requirements
- **Python 3.9.6**: The core programming language used (project tested with this version)
- **oTree 5.11.1**: The framework for running economic experiments (project tested with this version)
- **Web server**: For deployment (development server included with oTree)

#### Python Packages
```python
# Core oTree imports
from otree.api import *  # Main oTree functionality

# For AI integration
import google.generativeai as genai  # Google's Gemini AI API

# Standard libraries
import random  # For generating random valuations and selecting payment rounds
import json  # For handling structured data
import os  # For environment variables and file operations
```

#### External Services
- **Google API**: You need a Google API key with access to Gemini models

#### Browser Requirements
- Any modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Guide
1. **Set up a Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install oTree and dependencies**:
   ```bash
   pip install otree
   pip install google-generativeai
   ```

3. **Clone or download this project**

4. **Set up Google API key**:
   - Create a Google API key at https://makersuite.google.com/app/apikey
   - Enable the Generative AI API if required
   - Replace the placeholder in `init.py` with your key

### Configuration Options
The experiment is highly configurable with settings for:
- Showing/hiding AI explanations
- Synchronized/individualized valuations
- Including/excluding previous bids and payoffs in the AI's context
- Enabling different AI strategies
- Setting individual player permissions for bidding options

### Key Files
- **init.py**: Main game logic, models, and functions
- **settings.py**: Configuration for different session types
- **HTML templates**:
  - **introduction.html**: Game instructions
  - **bid.html**: Interface for selecting bid type
  - **ownbid.html**: Interface for manual bidding
  - **GeminiChoice.html**: Interface for the AI advisor variant
  - **results.html**: Round results display
  - **TrustQuestion.html**: Survey about AI trust
  - **FinalResults.html**: Final payment calculation

### Running the Experiment
1. **Start the oTree server**:
   ```bash
   otree devserver
   ```

2. **Access the admin interface**:
   Open http://localhost:8000/admin/ in your browser

3. **Create a session**:
   - Choose between "Auction Game (Standard)" or "Auction Game (Adviser)"
   - Set the number of participants
   - Start the session

### Extending with New Strategies
The code includes commented sections showing how to add new AI strategies (like an "aggressive" strategy). To add a new strategy:

1. Uncomment the relevant sections in init.py
2. Add the strategy implementation to the `build_prompt` function
3. Update the HTML templates to include the new strategy
4. Enable the strategy in settings.py

### Experiment Variants
- **Delegation (Standard Variant)**: Participants can choose whether to submit a self-defined bid or adopt a suggestion fully generated by the AI. The AI offers different strategies, such as "Basic" or "Risk-Averse", which differ in their risk assessment.

- **Advice (Advisory Mode)**: In this mode, participants first formulate their own bid before the AI presents differentiated suggestions for possible adjustments. This way, the AI is used as a supporting tool in the decision-making process without completely delegating personal responsibility.

---

<a id="deutsch"></a>
## Deutsch

### Projektübersicht
Dieses Projekt ist ein verhaltensökonomisches Experiment, das mit oTree erstellt wurde und eine Erstpreisauktion simuliert, bei der Spieler zwischen ihrem eigenen Gebot oder einem KI-generierten Gebot (mittels Google's Gemini AI) wählen können. Das Experiment wurde entwickelt, um zu untersuchen, wie Menschen mit KI-Empfehlungen in strategischen Entscheidungssituationen interagieren.

Dieses Projekt entstand im Rahmen einer Bachelorarbeit an der Technischen Universität Berlin mit dem Titel "Der Einsatz von Large Language Modellen in Erstpreisauktionen: Entwicklung eines oTree Experiments". Die Arbeit untersucht, wie KI-basierte Entscheidungshilfen das strategische Bietverhalten in experimentellen Wirtschaftskontexten beeinflussen können.

### Abstract
Die vorliegende Bachelorarbeit untersucht den Einsatz von Large Language Models (LLMs) in Erstpreisauktionen mit Fokus auf die Entwicklung eines experimentellen Frameworks mittels oTree. In experimentellen Wirtschaftskontexten stellt sich zunehmend die Frage, wie KI-basierte Entscheidungshilfen das strategische Bietverhalten beeinflussen können. Diese Arbeit konzipiert und implementiert ein flexibles oTree-Experiment, das verschiedene KI-Strategien wie risikoscheues oder grundlegendes Bietverhalten durch die Integration von Google Gemini ermöglicht. Dabei wird besonderes Augenmerk auf die Erstellung effektiver LLM-Prompts, die dynamische Anpassung von Bietstrategien sowie auf die technische Robustheit der Implementierung gelegt. Das entwickelte Framework erlaubt nicht nur die Untersuchung unterschiedlicher Delegations- und Advice-Modi, sondern bietet durch seine modulare Struktur auch Möglichkeiten zur Erweiterung um zusätzliche Strategien oder alternative LLMs. Die Ergebnisse dieser Arbeit liefern methodische Grundlagen für zukünftige Forschung zur KI-gestützten Entscheidungsfindung in ökonomischen Experimenten und zeigen Potenziale sowie Limitationen des Einsatzes von LLMs in experimentellen Auktionskontexten auf.

### Spielmechanik
1. **Grundaufbau**: Spieler werden anonym gepaart und nehmen über mehrere Runden an einer Erstpreisauktion teil.
2. **Bewertung**: Jeder Spieler erhält eine private Bewertung (zwischen 50-100) für den versteigerten Gegenstand.
3. **Gebotsoptionen**:
   - Spieler können ihr eigenes Gebot abgeben
   - Spieler können ein von Gemini AI vorgeschlagenes Gebot übernehmen
   - In der "Berater"-Variante sehen die Spieler die KI-Vorschläge und können entscheiden, ob sie bei ihrem eigenen Gebot bleiben oder es anpassen
4. **KI-Strategien**:
   - **Grundstrategie**: Standard-intelligenter Gebotsansatz
   - **Risikoaverse Strategie**: Konservativer Gebotsansatz, der Verlustvermeidung priorisiert
5. **Ergebnisse**: Der Höchstbietende gewinnt den Gegenstand und erhält eine Auszahlung basierend auf seiner Bewertung abzüglich seines Gebots
6. **Endabrechnung**: Eine Runde wird zufällig für die endgültige Auszahlungsberechnung ausgewählt

### Erforderliche Werkzeuge und Abhängigkeiten

#### Softwareanforderungen
- **Python 3.9.6**: Die verwendete Kernprogrammiersprache (Projekt mit dieser Version getestet)
- **oTree 5.11.1**: Das Framework zur Durchführung wirtschaftlicher Experimente (Projekt mit dieser Version getestet)
- **Webserver**: Für die Bereitstellung (Entwicklungsserver in oTree enthalten)

#### Python-Pakete
```python
# Kern-oTree-Importe
from otree.api import *  # Haupt-oTree-Funktionalität

# Für KI-Integration
import google.generativeai as genai  # Google's Gemini AI API

# Standardbibliotheken
import random  # Für die Generierung zufälliger Bewertungen und Auswahl von Zahlungsrunden
import json  # Für die Verarbeitung strukturierter Daten
import os  # Für Umgebungsvariablen und Dateioperationen
```

#### Externe Dienste
- **Google API**: Sie benötigen einen Google-API-Schlüssel mit Zugriff auf Gemini-Modelle

#### Browser-Anforderungen
- Jeder moderne Webbrowser (Chrome, Firefox, Safari, Edge)

### Installationsanleitung
1. **Python-Umgebung einrichten**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```

2. **oTree und Abhängigkeiten installieren**:
   ```bash
   pip install otree
   pip install google-generativeai
   ```

3. **Dieses Projekt klonen oder herunterladen**

4. **Google-API-Schlüssel einrichten**:
   - Erstellen Sie einen Google-API-Schlüssel unter https://makersuite.google.com/app/apikey
   - Aktivieren Sie bei Bedarf die Generative AI API
   - Ersetzen Sie den Platzhalter in `init.py` durch Ihren Schlüssel

### Konfigurationsoptionen
Das Experiment ist hochgradig konfigurierbar mit Einstellungen für:
- Anzeigen/Ausblenden von KI-Erklärungen
- Synchronisierte/individualisierte Bewertungen
- Einbeziehen/Ausschließen vorheriger Gebote und Auszahlungen im KI-Kontext
- Aktivieren verschiedener KI-Strategien
- Festlegen individueller Spielerberechtigungen für Gebotsoptionen

### Wichtige Dateien
- **init.py**: Hauptspiellogik, Modelle und Funktionen
- **settings.py**: Konfiguration für verschiedene Sitzungstypen
- **HTML-Vorlagen**:
  - **introduction.html**: Spielanleitung
  - **bid.html**: Oberfläche zur Auswahl des Gebotstyps
  - **ownbid.html**: Oberfläche für manuelle Gebote
  - **GeminiChoice.html**: Oberfläche für die KI-Berater-Variante
  - **results.html**: Anzeige der Rundenergebnisse
  - **TrustQuestion.html**: Umfrage zum KI-Vertrauen
  - **FinalResults.html**: Berechnung der Endauszahlung

### Durchführung des Experiments
1. **Den oTree-Server starten**:
   ```bash
   otree devserver
   ```

2. **Auf die Admin-Oberfläche zugreifen**:
   Öffnen Sie http://localhost:8000/admin/ in Ihrem Browser

3. **Eine Sitzung erstellen**:
   - Wählen Sie zwischen "Auction Game (Standard)" oder "Auction Game (Adviser)"
   - Legen Sie die Anzahl der Teilnehmer fest
   - Starten Sie die Sitzung

### Erweiterung mit neuen Strategien
Der Code enthält kommentierte Abschnitte, die zeigen, wie man neue KI-Strategien (wie eine "aggressive" Strategie) hinzufügen kann. Um eine neue Strategie hinzuzufügen:

1. Kommentieren Sie die relevanten Abschnitte in init.py aus
2. Fügen Sie die Strategieimplementierung zur Funktion `build_prompt` hinzu
3. Aktualisieren Sie die HTML-Vorlagen, um die neue Strategie einzubinden
4. Aktivieren Sie die Strategie in settings.py

### Experimentvarianten
- **Delegation (Standardvariante)**: Teilnehmer können wählen, ob sie ein selbstdefiniertes Gebot abgeben oder einen vollständig von der KI generierten Vorschlag übernehmen. Die KI bietet hierbei verschiedene Strategien an, wie z.B. „Basic" oder „Risk-Averse", die sich in ihrer Risikobewertung unterscheiden.

- **Advice (Beratungsmodus)**: In diesem Modus formulieren die Teilnehmer zunächst ein eigenes Gebot, bevor ihnen die KI differenzierte Vorschläge zur möglichen Anpassung präsentiert. So wird die KI als unterstützendes Werkzeug im Entscheidungsprozess genutzt, ohne die Eigenverantwortung vollständig zu delegieren.