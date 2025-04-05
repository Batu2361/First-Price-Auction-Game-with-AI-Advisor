from otree.api import *
import google.generativeai as genai
import random


GOOGLE_API_KEY = 'AIzaSyAiCmtsRiIqoKKhQHPbauN4ujEGlj6xreE'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')


doc = """
First-price auction where players can choose between their own bid or an AI-generated bid.
"""


class C(BaseConstants):
    PLAYERS_PER_GROUP = 2  # Anzahl der Spieler pro Gruppe
    NAME_IN_URL = 'bertrand'  # URL-Pfad für das Experiment
    NUM_ROUNDS = 3  # Anzahl der Spielrunden
    MAXIMUM_PRICE = cu(100)  # Maximaler Gebotspreis
    BUDGET = cu(100)  # Budget jedes Spielers


class Subsession(BaseSubsession):

    def creating_session(self):
        # Bestimme eine zufällige Runde für die finale Auszahlung
        if 'payment_round' not in self.session.vars:
            self.session.vars['payment_round'] = random.randint(1, C.NUM_ROUNDS)
            print(f"Auszahlungsrunde ist Runde {self.session.vars['payment_round']}")


class Group(BaseGroup):
    winning_bid = models.CurrencyField()  # Höchstes Gebot in der Gruppe
    gemini_bid = models.CurrencyField()  # KI-generiertes Gebot


class Player(BasePlayer):
    chosen_bid_type = models.StringField(blank=True)  # Ausgewählte Gebotsart (eigenes oder KI)
    bid = models.CurrencyField(
        min=0,
        max=C.MAXIMUM_PRICE,
        doc="Your final bid",
        label="Enter a bid between 0 and 100",
    )
    adjusted_bid = models.CurrencyField(blank=True, null=True)  # Angepasstes Gebot nach KI-Vorschlag

    # Felder für KI-Gebote und Erklärungen
    gemini_bid_basic = models.CurrencyField(blank=True)
    gemini_explanation_basic = models.LongStringField(blank=True)
    gemini_bid_risk_averse = models.CurrencyField(blank=True)
    gemini_explanation_risk_averse = models.LongStringField(blank=True)

    '''Für neue Strategie  
    gemini_bid_aggressive = models.CurrencyField(blank=True)
    gemini_explanation_aggressive = models.LongStringField(blank=True)
    '''

    valuation = models.CurrencyField()  # Wertschätzung des Spielers für das Auktionsobjekt
    is_winner = models.BooleanField()  # Hat der Spieler gewonnen?

    pyoff = models.CurrencyField()  # Auszahlung für den Spieler
    trust_in_ai = models.IntegerField(
        choices=[1, 2, 3, 4],
        label="How much do you trust the AI after seeing this round's result?\n(1 = No trust, 4 = Full trust)",
        widget=widgets.RadioSelect
    )


def get_gemini_bid(subsession: Subsession, player: Player, strategy: str):
    # Konfigurationseinstellungen aus der Session laden
    include_previous_bids = subsession.session.config.get("include_previous_bids", True)
    include_previous_payoffs = subsession.session.config.get("include_previous_payoffs", False)
    is_valuation_synchronized = subsession.session.config.get("is_valuation_synchronized", False)

    # Bieterhistorie des Spielers zusammenstellen, wenn aktiviert
    player_bid_history = [
        f"Round {e['round_number']}: {e['bid']}"
        for e in subsession.session.vars.get("bid_history", [])
        if e['player_id'] == player.id_in_group
    ] if include_previous_bids else []
    all_bids_summary = ", ".join(player_bid_history)

    # Auszahlungshistorie des Spielers zusammenstellen, wenn aktiviert
    player_payoff_history = [
        f"Round {e['round_number']}: {e['payoff']}"
        for e in subsession.session.vars.get("payoff_history", [])
        if e['player_id'] == player.id_in_group
    ] if include_previous_payoffs else []
    all_payoffs_summary = ", ".join(player_payoff_history)

    # Information über die Valuations im Spiel
    valuation_info = (
        "In this game, all players have the same valuation."
        if is_valuation_synchronized
        else "In this game, each player has a different valuation."
    )

    # Prompt für das KI-Modell basierend auf der Strategie erstellen
    prompt = build_prompt(strategy, valuation_info, player, all_bids_summary, all_payoffs_summary)
    print(f"[Gemini Prompt - {strategy}]:\n{prompt}")

    # API-Anfrage an das Gemini-Modell senden
    response = model.generate_content(prompt)
    if not response.candidates:
        return random.randint(0, 100), "No response received. Random bid."

    # Antwort von Gemini parsen
    text = response.candidates[0].content.parts[0].text.strip()
    print(f"Gemini's full response [{strategy}]: {text}")

    try:
        # Antwort in Gebot und Erklärung aufteilen
        bid_str, explanation = text.split(" - ", 1)
        gemini_bid = int(bid_str.strip())
        gemini_explanation = explanation.strip()

        # Gültigkeitsprüfung des Gebots
        if gemini_bid < 0 or gemini_bid > 100:
            gemini_bid = random.randint(0, 100)
    except:
        # Fehlerbehandlung bei ungültiger Antwort
        gemini_bid = random.randint(0, 100)
        gemini_explanation = "AI could not provide a valid format. Random bid."

    return gemini_bid, gemini_explanation




def build_prompt(strategy, valuation_info, player, all_bids_summary, all_payoffs_summary):
    # Erstellt den Kontext-Prompt für die KI basierend auf der Strategie und verfügbaren Informationen
    base_context = (
        f"You are participating in a first-price auction. Your valuation in this round is {player.valuation}. "
        f"{valuation_info} "
    )
    if all_bids_summary:
        base_context += f"The previous bids were: {all_bids_summary}. "
    if all_payoffs_summary:
        base_context += f"The previous payoffs were: {all_payoffs_summary}. "
    if strategy == "basic":
        prompt = (
            base_context +
            "Please make an intelligent bid between 0 and 100 and briefly explain why you chose this bid. "
            "Integer only. Answer in the format: '<Number> - <Explanation>'."
        )
        return prompt
    elif strategy == "risk_averse":
        prompt = (
            base_context +
            "You are risk-averse and want to safely avoid bidding too high or paying too much if you win. "
            "Please therefore suggest a bid between 0 and 100 that is consistent with your risk-averse position, and briefly explain your decision. "
            "Integer only. Answer in the format: '<Number> - <Explanation>'."
        )
        return prompt

    '''
    Hier ist ein Beispiel wie man ein neue Startgie einführen kann.
    elif strategy == "aggressive":
        # Neue Strategie
        prompt = (
                base_context +
                "You are an aggressive bidder and want to make sure you win the auction. "
                "Please therefore suggest a bid between 0 and 100 that is consistent with your aggressive position, and briefly explain your decision. "
                "Integer only. Answer in the format: '<Number> - <Explanation>'."
        )
        return prompt
    '''

    prompt = (
        base_context +
        "Please make any bid between 0 and 100 and briefly explain why you chose this bid. "
        "Format: '<Number> - <Explanation>'."
    )
    return prompt



def set_payoffs(group: Group):
    # Berechnet Gewinner und Auszahlungen für die Gruppe
    players = group.get_players()
    highest_bid = max([p.bid for p in players])
    winners = [p for p in players if p.bid == highest_bid]
    winner = random.choice(winners)  # Bei Gleichstand zufällig einen Gewinner wählen
    group.winning_bid = highest_bid
    bid_history = group.subsession.session.vars.get("bid_history", [])
    payoff_history = group.subsession.session.vars.get("payoff_history", [])
    for p in players:
        if p == winner:
            p.is_winner = True
            p.pyoff = C.BUDGET + p.valuation - p.bid  # Auszahlung = Budget + Bewertung - Gebot
        else:
            p.is_winner = False
            p.pyoff = C.BUDGET  # Verlierer behalten ihr Budget
        # Speichere Gebots- und Auszahlungshistorie
        bid_history.append({
            "round_number": group.round_number,
            "player_id": p.id_in_group,
            "bid": float(p.bid)
        })
        payoff_history.append({
            "round_number": group.round_number,
            "player_id": p.id_in_group,
            "payoff": float(p.pyoff)
        })
    group.subsession.session.vars["bid_history"] = bid_history
    group.subsession.session.vars["payoff_history"] = payoff_history






class Introduction(Page):
    # Einführungsseite, nur in Runde 1 angezeigt
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Bid(Page):
    # Haupt-Gebotsseite für Standardmodus
    form_model = 'player'
    form_fields = ['chosen_bid_type', 'bid']

    @staticmethod
    def is_displayed(player: Player):
        return not player.session.config.get("variant_mode", False)

    @staticmethod
    def vars_for_template(player: Player):
        # Vorbereitungen der Variablen für die Gebotsseite
        sc = player.session.config
        if sc.get('is_valuation_synchronized', False):
            # Wenn alle Spieler die gleiche Bewertung haben sollen
            round_key = f"shared_valuation_round_{player.subsession.round_number}"
            if player.subsession.session.vars.get(round_key) is None:
                shared_valuation = random.randint(50, 100)
                player.subsession.session.vars[round_key] = shared_valuation
            player.valuation = player.subsession.session.vars[round_key]
        else:
            # Individuelle Bewertungen für jeden Spieler
            if player.field_maybe_none('valuation') is None:
                player.valuation = random.randint(50, 100)

        # Prüfe, welche Strategien aktiviert sind
        basic_strategy_enabled = sc.get("basic_strategy", False)
        risk_averse_strategy_enabled = sc.get("risk_averse_strategy", False)

        '''Für neue Stratgie
        aggressive_strategy_enabled = sc.get("aggressive_strategy", False)
        '''

        # Prüfe die spielerspezifischen Rechte
        own_bid_enabled = sc.get(f"player{player.id_in_group}_own_bid", False)
        gemini_basic_enabled = sc.get(f"player{player.id_in_group}_geministrategy_basic", False)
        gemini_risk_averse_enabled = sc.get(f"player{player.id_in_group}_geministrategy_risk_averse", False)

        '''Für neue Strategie
        gemini_aggressive_enabled = sc.get(f"player{player.id_in_group}_geministrategy_aggressive", False)  # Neu
        '''

        # Bestimme, welche Optionen der Spieler in der Auswahlliste hat
        allowed_options_for_player = []
        if own_bid_enabled:
            allowed_options_for_player.append("own_bid")
        if basic_strategy_enabled and gemini_basic_enabled:
            # KI-Gebot nur bei Bedarf generieren
            if player.field_maybe_none('gemini_bid_basic') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "basic")
                player.gemini_bid_basic = gbid
                player.gemini_explanation_basic = gexp
            allowed_options_for_player.append("basic")
        if risk_averse_strategy_enabled and gemini_risk_averse_enabled:
            # Risikoaverse KI-Strategie
            if player.field_maybe_none('gemini_bid_risk_averse') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "risk_averse")
                player.gemini_bid_risk_averse = gbid
                player.gemini_explanation_risk_averse = gexp
            allowed_options_for_player.append("risk_averse")

        '''Für neue Strategie 
        if aggressive_strategy_enabled and gemini_aggressive_enabled:
            if player.field_maybe_none('gemini_bid_aggressive') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "aggressive")
                player.gemini_bid_aggressive = gbid
                player.gemini_explanation_aggressive = gexp
            allowed_options_for_player.append("aggressive")
        '''

        # Aktuelle Feldwerte für das Template
        bid_value = player.field_maybe_none("bid")
        gemini_risk_explanation= player.field_maybe_none("gemini_explanation_risk_averse")
        gemini_basic_explanation= player.field_maybe_none("gemini_explanation_basic")
        gemini_basic_value = player.field_maybe_none("gemini_bid_basic")
        gemini_risk_value= player.field_maybe_none("gemini_bid_risk_averse")

        '''Für neue Strategie 
        gemini_aggressive_explanation = player.field_maybe_none("gemini_explanation_aggressive")
        gemini_aggressive_value = player.field_maybe_none("gemini_bid_aggressive")
        '''

        return dict(
            valuation=player.valuation,
            allowed_options_for_player=allowed_options_for_player,
            gemini_bid_basic=gemini_basic_value if gemini_basic_value is not None else "",
            gemini_explanation_basic=gemini_basic_explanation if gemini_basic_explanation is not None else "",
            gemini_bid_risk_averse=gemini_risk_value if gemini_risk_value is not None else "",
            gemini_explanation_risk_averse=gemini_risk_explanation if gemini_risk_explanation is not None else "",

            #Für neue Stratgie
            #gemini_bid_aggressive=gemini_aggressive_value if gemini_aggressive_value is not None else "",
            #gemini_explanation_aggressive=gemini_aggressive_explanation if gemini_aggressive_explanation is not None else "",

            own_bid=bid_value if bid_value is not None else ""
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Verarbeite die Gebotsauswahl des Spielers
        chosen = player.chosen_bid_type or ''
        if chosen == 'own_bid':
            if player.bid is None:
                player.bid = cu(0)
        elif chosen == 'basic':
            player.bid = player.gemini_bid_basic
        elif chosen == 'risk_averse':
            player.bid = player.gemini_bid_risk_averse
        else:
            player.bid = cu(0)

        '''Für neue Strategie 
        Der Code muss vor else: eingefügt werden
        elif chosen == 'aggressive':  # Neu hinzufügen
            player.bid = player.gemini_bid_aggressive
        '''


class OwnBid(Page):
    # Seite für eigenes Gebot im Variantenmodus
    form_model = 'player'
    form_fields = ['bid']

    @staticmethod
    def is_displayed(player: Player):
        # Nur anzeigen, wenn variant_mode aktiv ist und nicht die GeminiChoice genutzt wird
        return player.session.config.get("variant_mode", False) and not player.session.config.get("use_gemini_choice", False)

    @staticmethod
    def vars_for_template(player: Player):
        # Initialisiere Bewertung für den Spieler
        sc = player.session.config
        if sc.get('is_valuation_synchronized', False):
            round_key = f"shared_valuation_round_{player.subsession.round_number}"
            if player.subsession.session.vars.get(round_key) is None:
                shared_valuation = random.randint(50, 100)
                player.subsession.session.vars[round_key] = shared_valuation
            player.valuation = player.subsession.session.vars[round_key]
        else:
            if player.field_maybe_none('valuation') is None:
                player.valuation = random.randint(50, 100)
        return dict(
            valuation=player.valuation
        )


class GeminiChoice(Page):
    # Seite für KI-Gebotsvorschläge im Variantenmodus
    form_model = 'player'
    form_fields = ['chosen_bid_type', 'adjusted_bid']

    @staticmethod
    def is_displayed(player: Player):
        # Wird nur angezeigt, wenn variant_mode=True in den Session-Konfigurationen
        return player.session.config.get("variant_mode", False)

    @staticmethod
    def vars_for_template(player: Player):
        sc = player.session.config
        show_explanations = sc.get("show_gemini_explanation", False)

        # Globale Einstellungen
        global_basic = sc.get("basic_strategy", False)
        global_risk_averse = sc.get("risk_averse_strategy", False)

        '''Für neue Strategie
        global_aggressive = sc.get("aggressive_strategy", False)  # Neu
        '''

        # Spielerspezifische Rechte
        player_own_bid_enabled = sc.get(f"player{player.id_in_group}_own_bid", False)
        player_gemini_basic = sc.get(f"player{player.id_in_group}_geministrategy_basic", False)
        player_gemini_risk_averse = sc.get(f"player{player.id_in_group}_geministrategy_risk_averse", False)

        '''Für neue Strategie
        player_gemini_aggressive = sc.get(f"player{player.id_in_group}_geministrategy_aggressive", False)  # Neu
        '''

        # Setze allowed_options_for_player
        # (gibt an, welche Optionen der jeweilige Spieler in der Auswahlliste hat)
        allowed_options_for_player = []

        # Option: Eigenes Gebot
        if player_own_bid_enabled:
            allowed_options_for_player.append("own_bid")

        # Option: Gemini Basic
        if global_basic and player_gemini_basic:
            # Falls die Werte noch nicht generiert sind, hole sie
            if player.field_maybe_none('gemini_bid_basic') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "basic")
                player.gemini_bid_basic = gbid
                player.gemini_explanation_basic = gexp
            allowed_options_for_player.append("basic")
        else:
            # Falls nicht erlaubt, sorge dafür, dass die Felder None sind
            player.gemini_bid_basic = None
            player.gemini_explanation_basic = None

        # Option: Gemini Risk-Averse
        if global_risk_averse and player_gemini_risk_averse:
            if player.field_maybe_none('gemini_bid_risk_averse') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "risk_averse")
                player.gemini_bid_risk_averse = gbid
                player.gemini_explanation_risk_averse = gexp
            allowed_options_for_player.append("risk_averse")
        else:
            player.gemini_bid_risk_averse = None
            player.gemini_explanation_risk_averse = None

        '''
        # Option: Gemini Aggressive
        if global_aggressive and player_gemini_aggressive:
            if player.field_maybe_none('gemini_bid_aggressive') is None:
                gbid, gexp = get_gemini_bid(player.subsession, player, "aggressive")
                player.gemini_bid_aggressive = gbid
                player.gemini_explanation_aggressive = gexp
            allowed_options_for_player.append("aggressive")
        else:
            player.gemini_bid_aggressive = None
            player.gemini_explanation_aggressive = None
        '''

        # Aktuelle Werte (können None sein)
        bid_value = player.field_maybe_none("bid")
        gemini_basic_value = player.field_maybe_none("gemini_bid_basic")
        gemini_basic_explanation = player.field_maybe_none("gemini_explanation_basic")
        gemini_risk_value = player.field_maybe_none("gemini_bid_risk_averse")
        gemini_risk_explanation = player.field_maybe_none("gemini_explanation_risk_averse")

        '''Für neue Strategie
        gemini_aggressive_value = player.field_maybe_none("gemini_bid_aggressive")  # Neu
        gemini_aggressive_explanation = player.field_maybe_none("gemini_explanation_aggressive")  # Neu
        '''

        '''
        Prüfen, ob mindestens eine Gemini-Strategie existiert
        Für neue Strategie:
        Ändere strategy in ["basic", "risk_averse"] zu strategy in ["basic", "risk_averse", "aggressive"]
        '''
        enable_gemini = any(
            strategy in allowed_options_for_player for strategy in ["basic", "risk_averse"])

        return dict(
            show_explanations=show_explanations,
            maximum_price=C.MAXIMUM_PRICE,
            valuation=player.valuation,

            # Eigener Bid im Template
            own_bid=bid_value if bid_value is not None else "",

            # Basic Strategy
            gemini_bid_basic=gemini_basic_value if gemini_basic_value else "",
            gemini_explanation_basic=gemini_basic_explanation if gemini_basic_explanation else "",

            # Risk-Averse
            gemini_bid_risk_averse=gemini_risk_value if gemini_risk_value else "",
            gemini_explanation_risk_averse=gemini_risk_explanation if gemini_risk_explanation else "",

            #Für neue Strategie
            #gemini_bid_aggressive=gemini_aggressive_value if gemini_aggressive_value else "",
            #gemini_explanation_aggressive=gemini_aggressive_explanation if gemini_aggressive_explanation else "",

            # Diese Variable steuert, ob wir die Gemini-Vorschläge überhaupt anzeigen
            enable_gemini=enable_gemini,

            # Welche Optionen der Spieler hat (own_bid, basic, risk_averse, aggressive)
            allowed_options_for_player=allowed_options_for_player,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Wenn Spieler "adjust" auswählt und ein angepasstes Gebot abgegeben wurde
        if player.chosen_bid_type == 'adjust' and player.adjusted_bid is not None:
            player.bid = player.adjusted_bid

        # Wenn das Gebot immer noch None sein sollte, setze es auf 0
        if player.bid is None:
            player.bid = cu(0)


class ResultsWaitPage(WaitPage):
    # Warteseite nach Geboten, berechnet Ergebnisse wenn alle Spieler fertig sind
    after_all_players_arrive = set_payoffs


class Results(Page):
    # Ergebnisseite zeigt Ausgang der Auktion
    @staticmethod
    def vars_for_template(player: Player):
        sc = player.session.config
        show_explanations = sc.get("show_gemini_explanation", False)

        # Überprüfe globale und spielerspezifische Einstellungen:
        basic_strategy_enabled = sc.get("basic_strategy", False) and sc.get(
            f"player{player.id_in_group}_geministrategy_basic", False)
        risk_averse_strategy_enabled = sc.get("risk_averse_strategy", False) and sc.get(
            f"player{player.id_in_group}_geministrategy_risk_averse", False)

        '''Für neue Strategie
        aggressive_strategy_enabled = sc.get("aggressive_strategy", False) and sc.get(
            f"player{player.id_in_group}_geministrategy_aggressive", False)  # Neu
        '''

        return dict(
            valuation=player.valuation,
            is_winner=player.is_winner,
            winning_bid=player.group.winning_bid,
            pyoff=player.pyoff,
            basic_strategy_enabled=basic_strategy_enabled,
            risk_averse_strategy_enabled=risk_averse_strategy_enabled,

            #Für neue Startegie
            #aggressive_strategy_enabled=aggressive_strategy_enabled,

            show_explanations=show_explanations,
        )

class TrustQuestion(Page):
    # Fragt nach Vertrauen in die KI nach jeder Runde
    form_model = 'player'
    form_fields = ['trust_in_ai']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'pyoff': player.pyoff,
            'valuation': player.valuation,
            'is_winner': player.is_winner,
        }


class FinalResults(Page):
    # Zeigt endgültige Auszahlung am Ende des Experiments
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        # Stelle sicher, dass eine Auszahlungsrunde festgelegt ist
        if 'payment_round' not in player.session.vars:
            player.session.vars['payment_round'] = random.randint(1, C.NUM_ROUNDS)
        payment_round = player.session.vars['payment_round']
        final_payoff_in_game_points = player.in_round(payment_round).pyoff
        player.payoff = final_payoff_in_game_points  # Setze die endgültige Auszahlung
        return dict(
            payment_round=payment_round,
            final_payoff=final_payoff_in_game_points,
        )


page_sequence = [
    Introduction,
    Bid,
    OwnBid,
    GeminiChoice,
    ResultsWaitPage,
    Results,
    TrustQuestion,
    FinalResults
]