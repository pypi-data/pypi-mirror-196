from django.utils import timezone
from decimal import Decimal

REFPERCENT = 0.15
WITHDRAWAL_STATUS = (
        (1, 'Approved & Paid'),
        (0, 'Cancelled'),
        (2, 'Processing'),
        (3,'Pending')
    )
PROFIT = "PROFIT"
HOLDINGS = "HOLDINGS"
PROFIT_AND_HOLDINGS = "PROFIT AND HOLDINGS"
REFERALL_BONUS = "REFERALL BONUS"
REFERALL_BONUS_REINVESTMENT = "REFERRAL BONUS REINVESTMENT"
INVESTMENT_REINVESTMENT = "INVESTMENT REINVESTMENT"

WITHDRAWAL_TYPE = (
    (PROFIT, PROFIT),
    (HOLDINGS,HOLDINGS),
    (PROFIT_AND_HOLDINGS, PROFIT_AND_HOLDINGS),
    (REFERALL_BONUS, REFERALL_BONUS),
    (REFERALL_BONUS_REINVESTMENT,REFERALL_BONUS_REINVESTMENT),
    (INVESTMENT_REINVESTMENT,INVESTMENT_REINVESTMENT)
)

class PackExtension: 
    @property
    def profit_x2(self):
        reinvested_packs =self.reinvested_packs
        if reinvested_packs:
            return 'REINVESTED'
        if hasattr(self,'packagesubscription'):
            print('was here')
        
        if timezone.now() < self.time_of_completion:
            number_of_days_obj = timezone.now() - self.time_of_subscription
            
        else:
            number_of_days_obj = self.time_of_completion+timezone.timedelta(days=1) - self.time_of_subscription        
        profit_as_of_today = (Decimal(round(self.package.daily_percentage/100,2)) * self.amount * number_of_days_obj.days)
        
        profit_withdrawals = self.profit_withdrawals
        profit_withdrawable_ = round((self.amount + profit_as_of_today) - profit_withdrawals,2) 
        
        if self.completion_status:
            if profit_withdrawals >= profit_as_of_today:
                profit_withdrawable_ = profit_withdrawable_
            else:
                profit_withdrawable_ = profit_withdrawable_
        else:
            
            if profit_withdrawable_ == self.amount:
                
                profit_withdrawable_ = 0
            if profit_withdrawable_ <= self.amount:
                profit_withdrawable_ = profit_withdrawable_
            if profit_withdrawable_ >= self.amount:
                profit_withdrawable_ -= self.amount
            """
            else:
                profit_withdrawable_ = profit_withdrawable_ - self.amount
            """
        
        

        if profit_withdrawable_ < 1:
            profit_withdrawable_ = 0
        
        """
        if self.withdrawal_request_active:
            
            
            Withdrawal.
        """
        
        return round(profit_withdrawable_,2) 


