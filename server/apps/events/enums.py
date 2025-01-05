from enum import Enum


class RecurringType(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def values(cls):
        return [choice.value for choice in cls]

    @classmethod
    def names(cls):
        return [choice.name for choice in cls]
