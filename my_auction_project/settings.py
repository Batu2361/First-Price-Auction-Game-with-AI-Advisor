from os import environ

SESSION_CONFIGS = [
    dict(
        name='auction_game',
        display_name="Auction Game (Standard)",
        app_sequence=['auction_game'],
        num_demo_participants=2,
        show_gemini_explanation=True,  # Erklärt Strategien der KI
        is_valuation_synchronized=False,  # Wenn True, haben alle Spieler dieselbe Bewertung
        include_previous_bids=True,  # Gibt der KI Zugriff auf frühere Gebote
        include_previous_payoffs=True,  # Gibt der KI Zugriff auf frühere Auszahlungen

        # Globale KI-Strategien - aktiviert/deaktiviert Strategien für alle Spieler
        basic_strategy=True,  # Allgemeine Basis-Strategie aktivieren
        risk_averse_strategy=True,  # Risikoaverse Strategie aktivieren

        # Für neue Strategie
        # aggressive_strategy=False,  # Neue aggressive Strategie (deaktiviert)

        # Zugriffsrechte pro Spieler - feingranulare Kontrolle der verfügbaren Strategien
        player1_own_bid=True,  # Spieler 1 kann eigenes Gebot abgeben
        player1_geministrategy_basic=True,  # Spieler 1 kann Basis-KI-Strategie nutzen
        player1_geministrategy_risk_averse=True,  # Spieler 1 kann risikoaverse KI-Strategie nutzen

        # Für neue Strategie
        # player1_geministrategy_aggressive=True,  # Spieler 1 kann aggressive KI-Strategie nutzen

        player2_own_bid=True,  # Spieler 2 kann eigenes Gebot abgeben
        player2_geministrategy_basic=True,  # Spieler 2 kann Basis-KI-Strategie nutzen
        player2_geministrategy_risk_averse=True,

        # player2_geministrategy_aggressive=True, # Spieler 2 kann aggressive KI-Strategie nutzen

        #Für mehr Spieler
        #player3_own_bid=True,
        #player3_geministrategy_basic=True,
        #player3_geministrategy_risk_averse=True,

        #player4_own_bid=True,
        #player4_geministrategy_basic=True,
        #player4_geministrategy_risk_averse=True,

        variant_mode=False
    ),
    dict(
        name='auction_game_variant',
        display_name="Auction Game (Adviser)",
        app_sequence=['auction_game'],
        num_demo_participants=2,
        show_gemini_explanation=True,
        is_valuation_synchronized=False,
        include_previous_bids=True,
        include_previous_payoffs=True,
        basic_strategy=True,
        risk_averse_strategy=True,

        # Für neue Stratgie
        # aggressive_strategy=False,

        # Zugriffsrechte pro Spieler hinzufügen
        player1_own_bid=True,
        player1_geministrategy_basic=True,
        player1_geministrategy_risk_averse=True,

        # Für neue Stratgie
        # player1_geministrategy_aggressive=True,

        player2_own_bid=True,
        player2_geministrategy_basic=True,
        player2_geministrategy_risk_averse=True,

        # Für neue Stratgie
        # player2_geministrategy_aggressive=True,

        # Für mehr Spieler
        # player3_own_bid=True,
        # player3_geministrategy_basic=True,
        # player3_geministrategy_risk_averse=True,

        # player4_own_bid=True,
        # player4_geministrategy_basic=True,
        # player4_geministrategy_risk_averse=True,

        variant_mode=True
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt'
    ),
    dict(
        name='live_demo',
        display_name='Room for live demo (no participant labels)'
    ),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

SECRET_KEY = 'YOUR_SECRET_KEY_HERE'
INSTALLED_APPS = ['otree']
