

class HoldingEntity:
    def __init__(self, id_value, weight = None) -> None:
        self.id_value = id_value
        self.weight = weight
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    def is_weight_missing(self) -> bool:
        return self.weight is None


class PortfolioEntity:
    def __init__(self, holdings, default_id_scheme = None) -> None:
        self.default_id_scheme = "ISIN" if default_id_scheme is None else default_id_scheme
        self.holdings = [HoldingEntity(**holding) for holding in holdings]

    def to_dict(self) -> dict:
        return {
            "default_id_scheme" : self.default_id_scheme,
            "holdings" : [holding.to_dict() for holding in self.holdings]
        }
    
    def get_holdings_weight_sum(self):
        return sum(
            holding.weight for holding in 
            self.holdings if not 
            holding.is_weight_missing())

    def get_holdings_with_missing_weights(self):
        return [holding for holding in self.holdings if holding.is_weight_missing()]

    def fix_sum(self) -> bool:
        bad_holdings = self.get_holdings_with_missing_weights()
        bad_holdings_count = len(bad_holdings)

        if bad_holdings_count > 0:
            avg_weight_for_remainder = (1 - self.get_holdings_weight_sum()) / bad_holdings_count

            for bad_holding in bad_holdings:
                bad_holding.weight = avg_weight_for_remainder
            
            return True
        return False
                
