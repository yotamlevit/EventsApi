def parse_event(event_data: list) -> dict:
    return {
        'id': event_data[0],
        'name': event_data[1],
        'start_time': event_data[2],
        'team1': event_data[3],
        'team2': event_data[4],
        'location': event_data[5],
        'creation_time': event_data[6]
    }