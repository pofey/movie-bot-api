from moviebotapi import Session


class PluginApi:
    def __init__(self, session: Session):
        self._session: Session = session
