from decimal import Decimal
import re

class ExactMatcher:
    @staticmethod
    def match_ids(ref1: str, ref2: str) -> float:
        if not ref1 or not ref2:
            return 0.0
        return 1.0 if ref1.strip() == ref2.strip() else 0.0

class NormalizedMatcher:
    @staticmethod
    def normalize_reference(ref: str) -> str:
        if not ref:
            return ""
        # Remove special characters and spaces, convert to uppercase
        return re.sub(r'[^A-Z0-9]', '', str(ref).upper())

    @staticmethod
    def match(ref1: str, ref2: str) -> float:
        norm1 = NormalizedMatcher.normalize_reference(ref1)
        norm2 = NormalizedMatcher.normalize_reference(ref2)
        if not norm1 or not norm2:
            return 0.0
        
        if norm1 == norm2:
            return 0.95 # High confidence for normalized exact match
            
        # Prefix/Suffix matching
        if norm1 in norm2 or norm2 in norm1:
            return 0.8 # Substring match
            
        return 0.0

class FinancialMatcher:
    @staticmethod
    def match_amounts(amt1: Decimal, amt2: Decimal, tolerance: Decimal = Decimal('1.00')) -> float:
        if amt1 is None or amt2 is None:
            return 0.0
        
        diff = abs(amt1 - amt2)
        if diff == 0:
            return 1.0
        elif diff <= tolerance:
            return 0.9 # Within rounding tolerance
        
        # Check if it could be a fee-deducted amount (e.g. 2% PG fee)
        # If amt2 is approx 98% of amt1
        ratio = amt2 / amt1 if amt1 > 0 else Decimal('0')
        if Decimal('0.97') <= ratio <= Decimal('0.99'):
            return 0.8 # Plausible fee-deducted match
            
        return 0.0

class CandidateGenerator:
    """
    Multi-stage candidate generation pipeline
    """
    def __init__(self):
        self.exact = ExactMatcher()
        self.normalized = NormalizedMatcher()
        self.financial = FinancialMatcher()

    def generate_candidates(self, source_record, target_pool):
        candidates = []
        for target in target_pool:
            score = self.evaluate_match(source_record, target)
            if score > 0.5:
                candidates.append({"target": target, "score": score})
                
        # Sort by score descending
        return sorted(candidates, key=lambda x: x["score"], reverse=True)
        
    def evaluate_match(self, source, target) -> float:
        # Example weighting: 50% reference match, 50% amount match
        ref_score = self.exact.match_ids(source.get("reference"), target.get("id"))
        if ref_score == 0:
            ref_score = self.normalized.match(source.get("reference"), target.get("id"))
            
        amt_score = self.financial.match_amounts(
            Decimal(str(source.get("amount", 0))), 
            Decimal(str(target.get("amount", 0)))
        )
        
        final_score = (ref_score * 0.5) + (amt_score * 0.5)
        return final_score
