from decimal import Decimal
from typing import Dict, List, Tuple

class RouteSplitCalculator:
    """
    Deterministic calculator for Razorpay Route vendor/platform splits,
    incorporating fee allocation and refund distribution rules.
    """
    PG_FEE_RATE = Decimal('0.02') # 2% standard
    GST_RATE = Decimal('0.18')   # 18% GST on PG fee

    @staticmethod
    def calculate_split(
        total_amount: Decimal, 
        vendor_share_pct: Decimal, 
        fee_borne_by: str = "platform"
    ) -> Dict[str, Decimal]:
        """
        Calculates the exact amount credited to vendor vs platform linked accounts.
        """
        pg_fee = (total_amount * RouteSplitCalculator.PG_FEE_RATE).quantize(Decimal('0.01'))
        gst_on_fee = (pg_fee * RouteSplitCalculator.GST_RATE).quantize(Decimal('0.01'))
        total_fee = pg_fee + gst_on_fee

        net_settlement = total_amount - total_fee

        # Calculate logical shares
        vendor_logical = (total_amount * vendor_share_pct).quantize(Decimal('0.01'))
        platform_logical = total_amount - vendor_logical

        if fee_borne_by == "vendor":
            vendor_actual = vendor_logical - total_fee
            platform_actual = platform_logical
        elif fee_borne_by == "platform":
            vendor_actual = vendor_logical
            platform_actual = platform_logical - total_fee
        else: # split proportionally
            vendor_fee = (total_fee * vendor_share_pct).quantize(Decimal('0.01'))
            platform_fee = total_fee - vendor_fee
            vendor_actual = vendor_logical - vendor_fee
            platform_actual = platform_logical - platform_fee
            
        # Ensure we don't return negative values if fee exceeds share
        # (in real Route, Razorpay debits a balance account, but here we cap at 0 and track negative balance separately)
        vendor_negative = Decimal('0.00')
        platform_negative = Decimal('0.00')
        
        if vendor_actual < 0:
            vendor_negative = abs(vendor_actual)
            vendor_actual = Decimal('0.00')
            
        if platform_actual < 0:
            platform_negative = abs(platform_actual)
            platform_actual = Decimal('0.00')

        return {
            "vendor_payout": vendor_actual,
            "platform_payout": platform_actual,
            "total_fee": total_fee,
            "net_settlement": net_settlement,
            "vendor_negative_balance": vendor_negative,
            "platform_negative_balance": platform_negative
        }

    @staticmethod
    def calculate_refund_allocation(
        refund_amount: Decimal,
        original_vendor_payout: Decimal,
        original_platform_payout: Decimal,
        refund_borne_by: str = "vendor"
    ) -> Dict[str, Decimal]:
        """
        Determines how a refund is recovered from the vendor and platform.
        """
        # Simplistic logic: normally refund is borne by the vendor who provided the service
        if refund_borne_by == "vendor":
            vendor_recovery = refund_amount
            platform_recovery = Decimal('0.00')
        elif refund_borne_by == "platform":
            vendor_recovery = Decimal('0.00')
            platform_recovery = refund_amount
        else:
            # Proportional recovery
            total_original = original_vendor_payout + original_platform_payout
            if total_original > 0:
                vendor_ratio = original_vendor_payout / total_original
                vendor_recovery = (refund_amount * vendor_ratio).quantize(Decimal('0.01'))
                platform_recovery = refund_amount - vendor_recovery
            else:
                vendor_recovery = Decimal('0.00')
                platform_recovery = refund_amount

        return {
            "vendor_recovery_amount": vendor_recovery,
            "platform_recovery_amount": platform_recovery
        }
