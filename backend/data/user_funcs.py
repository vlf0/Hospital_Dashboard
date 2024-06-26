
class DaysSuffixManager:

    def __init__(self, num: int):
        self.num: str = str(num)
        self.num_length: int = len(self.num)

    def change_suffix(self):
        head = 'день'
        if (self.num[-1] > '4' or self.num[-1] == '0') or (self.num_length > 1 and self.num[-2] == '1'):
            head = 'дней'
        elif '1' < self.num[-1] < '5':
            head = 'дня'
        return head
