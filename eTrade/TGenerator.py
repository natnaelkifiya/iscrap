class TGenerator:
    def __init__(self):
        self.generator = self._generate_numbers()

    def _generate_numbers(self):
        for i in range(100000000):  # 0 to 99999999
            yield f'{i:08}'  # Format as 8-digit string, e.g., '00000000'

    def get_next_numbers(self, n):
        return [next(self.generator) for _ in range(n)]
    
    
    


