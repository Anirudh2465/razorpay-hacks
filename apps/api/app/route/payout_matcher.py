from decimal import Decimal
from typing import List, Dict

class PayoutMatcher:
    @staticmethod
    def match_bank_statement_to_payouts(bank_statement: List[Dict], expected_payouts: List[Dict]) -> List[Dict]:
        """
        Matches actual bank settlement lines to expected vendor payouts.
        """
        matches = []
        unmatched_bank = []
        
        # Simple exact match on UTR / Reference
        for stmt in bank_statement:
            matched = False
            for expected in expected_payouts:
                if stmt.get("reference") == expected.get("payout_id"):
                    matches.append({
                        "bank_transaction": stmt,
                        "expected_payout": expected,
                        "status": "matched"
                    })
                    matched = True
                    break
            
            if not matched:
                unmatched_bank.append(stmt)
                
        return matches
