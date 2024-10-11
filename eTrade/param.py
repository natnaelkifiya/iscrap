from datetime import datetime

class parameters:
    def __init__(self) -> None:
        current_time = datetime.now().date()  # Assign current time to a variable
        self.eTradeParam = {
            'batch_size': 5,
            'base_url': 'https://etrade.gov.et/business-license-checker',
            'csv_path': 'etrade_logs/' + str(current_time) + '.csv',  # Use the variable here
            'tuple_per_csv': 20000,
            'mode': True,
            'fieldName': ['first_name', 'middle_name', 'last_name']
        }

    # @property
    # def eTradeParam(self) -> dict:
    #     """Return the eTrade parameters as a dictionary."""
    #     return self._eTradeParam
