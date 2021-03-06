from client.persistence.Authorization import Authorization


class User:
    def __init__(self, tag_id: int, is_authorized: Authorization, date: float):
        self.tag_id = tag_id
        self.is_authorized = is_authorized
        self.date = date

    def __str__(self) -> str:
        return f"""tag: {self.tag_id}, isAuth: {self.is_authorized}, date: {self.date}"""
