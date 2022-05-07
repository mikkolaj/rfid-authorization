from client.persistance.EventType import EventType


class Log:
    def __init__(self, id: int, created_at: float, event_type: EventType, tag_id: int):
        self.id = id
        self.created_at = created_at
        self.event_type = event_type
        self.tag_id = tag_id
