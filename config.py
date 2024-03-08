# Ayın günleri
day_of_months = [31,29,46,30,31,45,31,31,45,31,30,46] # Her ay için gün sayısı
weekdays_of_months = [22,21,21,18,20,17,22,21,21,22,21,22] # Her ay için çalışma günü sayısı

# Vergi
tax_bracket_ceilings = [110000, 230000, 580000, 3000000] # Vergi dilimi tavanları
tax_rates = [0.15, 0.2, 0.27, 0.35, 0.4] # Vergi dilimi vergi oranları
tax_bracket_amounts = [16500, 40500, 135000, 982000] # Vergi dilimi sabit vergileri
minimum_wage_tax_exempt = [2550.32,2550.32,2550.32,2550.32,2550.32,2550.32] # Asgari vergi istisnası
minimum_wage_stamp_exempt = [151.82,151.82,151.82,151.82,151.82,151.82] # Asgari damga istisnası

# Yemek
food_payment = [178,178,178,178,178,178] # Günlük yemek ücreti
food_pay_insurance = [20.26,20.26,20.26,20.26,20.26,20.26] # Yemekten ödenecek olan sigorta
food_pay_tax = [7.95,7.95,7.95,7.95,7.95,7.95] # Yemekten ödenecek olan vergi 

# Sendikal
union_cut = 0.7 # Sendika kesintisi (gün olarak, %70 için 0.7)
social_payment = [744.35,744.35,744.35,744.35,744.35,744.35] # Sosyal tazminat
fuel_payment = [136.95,136.95,136.95,136.95,136.95,136.95] # Yakacak yardımı

# Rapor durumları
allowed_times_of_sick_leave = 5 # Bir yıl içerisinde izin verilen rapor sayısı
days_allowd_per_sick_days = 2 # Bir rapor alındığında işveren tarafından karşılanan max gün sayısı

# İkinci altı ay için enflasyon oranları(%5 için 1.05)
inflation = [1.067,1.0453,1,1,1,1]