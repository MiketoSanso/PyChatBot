class Constants:
    def __init__(self):
        self.BOT_TOKEN = "8588091640:AAGz9_NJxTciE7MszsJRccWq109ULyrJET8"
        self.TOKEN_PAYMENTS = "1744374395:TEST:e1139428288af4683452"

        self.MAX_CHARS_AI = 1000000
        self.MAX_COUNT_MESSAGES = 100
        self.MAX_COUNT_CHARS_ANSWER = self.MAX_CHARS_AI / self.MAX_COUNT_MESSAGES / 2
        self.MAX_COUNT_CHARS_MESSAGE = self.MAX_CHARS_AI / self.MAX_COUNT_MESSAGES / 2