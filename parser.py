import re

def parser(content):
    players = []
    total_points = 0
    counter = 0
    name, points = None, None

    # Estrae i punti totali
    total_points_tag = content.find('div', class_='squadrons-counter__value')
    if total_points_tag:
        try:
            total_points = int(total_points_tag.text.strip())
        except ValueError:
            total_points = 0

    for dataItem in content.findAll('div', attrs={"class": "squadrons-members__grid-item"}):
        if counter == 7:
            a_tag = dataItem.find('a')
            if a_tag and a_tag.get('href'):
                name = a_tag.get('href').replace('en/community/userinfo/?nick=', '')
            else:
                name = None
        elif counter == 8:
            points = re.sub(r'\s+', '', dataItem.text)
        elif counter == 12:
            if name and points:
                players.append({
                    'name': name,
                    'points': int(points) if points.isdigit() else 0
                })
            counter = 6  # Reset counter per il prossimo giocatore
        counter += 1

    # Aggiunge l'ultimo giocatore se mancante
    if name and points and {'name': name, 'points': int(points) if points.isdigit() else 0} not in players:
        players.append({'name': name, 'points': int(points) if points.isdigit() else 0})

    return players, total_points
