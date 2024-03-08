import json
import math
from config import day_of_months, weekdays_of_months
from config import tax_bracket_ceilings, tax_rates, tax_bracket_amounts, minimum_wage_tax_exempt, minimum_wage_stamp_exempt 
from config import social_payment, fuel_payment, union_cut, food_payment, food_pay_insurance, food_pay_tax
from config import allowed_times_of_sick_leave, days_allowd_per_sick_days
from config import inflation

# Her ay çalışılan günler
worked_days = []

# Aylık ödemeler
monthly_gross_pay = [] # Brüt günlük kazançlar
monthly_food_pay = [] # Yemek yardımı
total_gross = []

# Taxable amounts
insurance_income = [] # Sigorta matrahı
stamped_income = [] # Damga matrahı
tax_income_total = [] # Gelir vergisi matrahı

# Deductions
insurance_deduction = [] # SGK kesintisi
job_insurance_deduction = [] # İşsizlik sigortası
income_taxes_deduction = [] # Gelir vergisi
stamp_tax_deduction = [] # Damga vergisi
union_deduction = [] # Sendika aidatı

# Global değişkenleri sıfırlar
def reset_variables():
    worked_days.clear()
    monthly_gross_pay.clear()
    monthly_food_pay.clear()
    total_gross.clear()
    insurance_income.clear()
    stamped_income.clear()
    tax_income_total.clear()
    insurance_deduction.clear()
    job_insurance_deduction.clear()
    income_taxes_deduction.clear()
    stamp_tax_deduction.clear()
    union_deduction.clear()

# Ilk 6 ayın enflayonuna göre ikinci altı ayın ödemelerini ekler
def adjust_inflation():
    # Ilk altı ayın enflasyonunu hesapla
    half_year_inflation = 1
    for inf in inflation:
        half_year_inflation *= inf
    # Sonra da asgari ücrete ve maaşa enflasyon oranının yansıdığını varsayarak yeni hesaplamalar yap
    for i in range(6):
        minimum_wage_tax_exempt.append(minimum_wage_tax_exempt[0] * half_year_inflation)
        minimum_wage_stamp_exempt.append(minimum_wage_stamp_exempt[0] * half_year_inflation)
        food_pay_insurance.append(food_pay_insurance[0] * half_year_inflation)
        food_pay_tax.append(food_pay_tax[0] * half_year_inflation)
        social_payment.append(social_payment[0] * half_year_inflation)
        fuel_payment.append(fuel_payment[0] * half_year_inflation)
        food_payment.append(food_payment[0] * half_year_inflation)
    return half_year_inflation

# Aylık brüt kazançları hesaplar
def calculate_monthly_gross(daily_gross_pay, sick_days):
    sick_leave_total = 0
    for i in range(12):
        payed_day_count = day_of_months[i]
        if sick_days[i] != 0:
            sick_leave_total += 1
            if sick_leave_total > allowed_times_of_sick_leave:
                payed_day_count = day_of_months[i] - sick_days[i]
            else:
                if sick_days[i] > days_allowd_per_sick_days:
                    payed_day_count = day_of_months[i] - (sick_days[i] - days_allowd_per_sick_days)
        gross = (payed_day_count * daily_gross_pay[i]) + social_payment[i] + fuel_payment[i]
        monthly_gross_pay.append(payed_day_count * daily_gross_pay[i])
        total_gross.append(gross)

# Aylık vergi hesaplar
def calculate_monthly_taxes(worked_days, daily_wage):
    taxed_income = 0 # şu ana kadar vergilendirilmiş gelir 
    total_payed_tax = 0 # şu ana kadar ödenmiş vergi
    for i in range(12):
        monthly_tax = 0  # Her ayın vergisini sıfırla
        insured_income = round(total_gross[i] + food_pay_insurance[i] * worked_days[i], 2) # Sigorta Matrahı
        insurance_income.append(insured_income)
        insurance = round(insured_income * 0.14, 2) # sigorta
        insurance_deduction.append(insurance)
        job_insurance = round(insured_income * 0.01, 2) # işsizlik
        job_insurance_deduction.append(job_insurance)
        union_subscription = round(daily_wage[i] * union_cut, 2)
        union_deduction.append(union_subscription)
        wage_to_be_taxed = round(total_gross[i] - insurance - job_insurance - union_subscription + (food_pay_tax[i] * worked_days[i]), 2) # Vergi matrahı
        tax_income_total.append(wage_to_be_taxed)
        stampable_income = round(total_gross[i] + worked_days[i] * food_pay_tax[i], 2) # Damga matrahı
        stamped_income.append(stampable_income)
        stamp = round(stampable_income * 0.00759 - minimum_wage_stamp_exempt[i], 2) # damga vergisi
        stamp_tax_deduction.append(stamp)
        cumulative_total = taxed_income + wage_to_be_taxed # kümülatif toplam
        if cumulative_total <= tax_bracket_ceilings[0]:
            monthly_tax = round(wage_to_be_taxed * tax_rates[0], 2)
        elif cumulative_total <= tax_bracket_ceilings[1]:
            second_bracket_amount = cumulative_total - tax_bracket_ceilings[0]
            monthly_tax =  round((second_bracket_amount * tax_rates[1] + tax_bracket_amounts[0]) - total_payed_tax, 2)
        elif cumulative_total <= tax_bracket_ceilings[2]:
            third_bracket_amount = cumulative_total - tax_bracket_ceilings[1]
            monthly_tax =  round((third_bracket_amount * tax_rates[2] + tax_bracket_amounts[1]) - total_payed_tax, 2)
        elif cumulative_total <= tax_bracket_ceilings[3]:
            fourth_bracket_amount = cumulative_total - tax_bracket_ceilings[2]
            monthly_tax =  round((fourth_bracket_amount * tax_rates[3] + tax_bracket_amounts[2]) - total_payed_tax, 2)
        else:
            fifth_bracket_amount = cumulative_total - tax_bracket_ceilings[3]
            monthly_tax =  round((fifth_bracket_amount * tax_rates[4] + tax_bracket_amounts[3]) - total_payed_tax, 2)
        total_payed_tax += monthly_tax # toplam ödenmiş vergiyi arttır
        taxed_income += wage_to_be_taxed # vergiye tabi tutulmuş miktarı arttır
        income_taxes_deduction.append(monthly_tax - minimum_wage_tax_exempt[i])

# Aylık kaç gün çalışıldığını ve yemek ücretini hesaplar
def calculate_food_and_workdays(sick_days, vacation):
    for i in range(12):
        days_worked = weekdays_of_months[i] - vacation[i] - sick_days[i]
        food = (food_payment[i] * days_worked)
        worked_days.append(days_worked)
        monthly_food_pay.append(food)

def print_bordro(sick_days, vacation, wage, june_raise=True):
    if june_raise:
        inflation = adjust_inflation()
        inflated_wage = wage * inflation
        monthly_wage = [wage,wage,wage,wage,wage,wage,inflated_wage,inflated_wage,inflated_wage,inflated_wage,inflated_wage,inflated_wage]
    else:
        monthly_wage = [wage,wage,wage,wage,wage,wage,wage,wage,wage,wage,wage,wage]
    calculate_monthly_gross(monthly_wage, sick_days)
    calculate_food_and_workdays(sick_days, vacation)
    calculate_monthly_taxes(worked_days, monthly_wage)
    with open(f"Bordro.txt", "w", encoding="utf-8") as file:
        file.write(f"Oluşturulmuş Bordro (Powered By LightFoe):\n")
        total = 0
        for i in range(12):
            total += round(monthly_gross_pay[i] + social_payment[i] + fuel_payment[i] + monthly_food_pay[i] - (insurance_deduction[i] + job_insurance_deduction[i] + income_taxes_deduction[i] + stamp_tax_deduction[i]) - union_deduction[i], 2)
        file.write(f"Toplam Yıllık Kazanç: {total}")
        file.write("\n")
        file.write(f"Ortalama Aylık Net kazanç: {total/12}")
        file.write("\n")
        for i in range(12):
            if i == 0:
                month = "Ocak"
            elif i == 1:
                month = "Şubat"
            elif i == 2:
                month = "Mart"
            elif i == 3:
                month = "Nisan"
            elif i == 4:
                month = "Mayıs"
            elif i == 5:
                month = "Haziran"
            elif i == 6:
                month = "Temmuz"
            elif i == 7:
                month = "Ağustos"
            elif i == 8:
                month = "Eylül"
            elif i == 9:
                month = "Ekim"
            elif i == 10:
                month = "Kasım"
            elif i == 11:
                month = "Aralık"
            file.write(f"{month} Bordro Zarfı\n")
            file.write("    KAZANÇLAR:\n")
            file.write(f"        - Günlük Brüt Ücret: {monthly_wage[i]}\n")
            file.write(f"        - Brüt Ücret: {round(monthly_gross_pay[i], 2)}\n")
            file.write(f"        - Sosyal Yardım: {round(social_payment[i], 2)}\n")
            file.write(f"        - Yakacak Yardımı: {round(fuel_payment[i], 2)}\n")
            file.write(f"        - Yemek Yardımı: {round(monthly_food_pay[i], 2)}\n")
            file.write("    MATRAHLAR:\n")
            file.write(f"        - Sigorta Matrahı: {round(insurance_income[i], 2)}\n")
            file.write(f"        - Gelir Vergisi Matrahı: {round(tax_income_total[i], 2)}\n")
            file.write(f"        - Damga Vergisi Matrahı: {round(stamped_income[i], 2)}\n")
            file.write("    KESİNTİLER:\n")
            file.write(f"        - SGK Kesintisi: {round(insurance_deduction[i], 2)}\n")
            file.write(f"        - İşsizlik Sigortası: {round(job_insurance_deduction[i], 2)}\n")
            file.write(f"        - Gelir Vergisi: {round(income_taxes_deduction[i], 2)}\n")
            file.write(f"        - Damga Vergisi: {round(stamp_tax_deduction[i], 2)}\n")
            file.write(f"        - Sendika/Dayanışma Aidatı: {round(union_deduction[i], 2)}\n")
            file.write("    Özet: \n")
            file.write(f"        - Brüt Ücret: {round(monthly_gross_pay[i], 2)}\n")
            file.write(f"        - Kazançlar Toplamı: {round(monthly_gross_pay[i] + social_payment[i] + fuel_payment[i] + monthly_food_pay[i], 2)}\n")
            file.write(f"        - Yasal Kesinti Toplamı: {round(insurance_deduction[i] + job_insurance_deduction[i] + income_taxes_deduction[i] + stamp_tax_deduction[i], 2)}\n")
            file.write(f"        - Özel Kesinti Toplamı: {round(union_deduction[i], 2)}\n")
            file.write(f"        - Net Ödenecek: {round(monthly_gross_pay[i] + social_payment[i] + fuel_payment[i] + monthly_food_pay[i] - (insurance_deduction[i] + job_insurance_deduction[i] + income_taxes_deduction[i] + stamp_tax_deduction[i]) - union_deduction[i], 2)}\n")
            file.write("")

print_bordro([0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], 2424.2)