class Category:
    def __init__(self, name, emoji):
        self.name = name
        self.emoji = emoji


class Categories:
    ECONOMY = Category("economy", "\U0001FA99")
    FAMILY = Category("family", "\U0001F46A")
    RANDOM = Category("random", "\u2753")