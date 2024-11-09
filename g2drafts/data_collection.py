import requests
import db_setup  # Импортируем файл db_setup для подключения к базе данных

LEAGUEPEDIA_API_URL = "https://lol.fandom.com/api.php"
TEAM_NAME = "G2 Esports"  # Укажите нужное имя команды
TOURNAMENT_NAME = "Worlds 2024"  # Укажите нужный турнир

# Функция для запроса данных о драфте
def get_team_draft(team_name, tournament_name):
    params = {
        "action": "cargoquery",
        "format": "json",
        "tables": "PicksAndBansS7=pb, MatchSchedule=ms",
        "fields": "ms.DateTime_UTC, pb.Team, pb.Side, pb.Champion, pb.Role, ms.Opponent, ms.Outcome, ms.Gamelength",
        "where": f"pb.Team='{team_name}' AND ms.OverviewPage='{tournament_name}'",
        "join_on": "pb.MatchId=ms.MatchId",
        "order_by": "ms.DateTime_UTC",
        "limit": "50"
    }
    response = requests.get(LEAGUEPEDIA_API_URL, params=params)
    data = response.json()
    return data["cargoquery"]

# Функция для сохранения данных в базе данных
def save_draft_to_db(draft_data):
    conn = db_setup.get_db_connection()
    cursor = conn.cursor()
    game_drafts = {}

    for draft in draft_data:
        draft_fields = draft["title"]
        match_date = draft_fields["DateTime_UTC"]
        team_name = draft_fields["Team"]
        side = draft_fields["Side"]
        champion_pick = draft_fields["Champion"]
        opponent_team = draft_fields["Opponent"]
        game_duration = draft_fields["Gamelength"]
        outcome = draft_fields["Outcome"]

        if match_date not in game_drafts:
            game_drafts[match_date] = {
                "blue_side_draft": [],
                "red_side_draft": [],
                "opponent_team": opponent_team,
                "game_duration": game_duration,
                "win_or_loss": outcome
            }
        
        if side == "Blue":
            game_drafts[match_date]["blue_side_draft"].append(champion_pick)
        elif side == "Red":
            game_drafts[match_date]["red_side_draft"].append(champion_pick)

    for match_date, draft_info in game_drafts.items():
        cursor.execute('''INSERT INTO drafts (match_date, blue_side_draft, red_side_draft, team_name, opponent_team, game_duration, win_or_loss)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                       (match_date,
                        ", ".join(draft_info["blue_side_draft"]),
                        ", ".join(draft_info["red_side_draft"]),
                        TEAM_NAME,
                        draft_info["opponent_team"],
                        draft_info["game_duration"],
                        draft_info["win_or_loss"]))
    conn.commit()
    cursor.close()
    conn.close()

# Получаем данные и сохраняем в базу данных
draft_data = get_team_draft(TEAM_NAME, TOURNAMENT_NAME)
save_draft_to_db(draft_data)
