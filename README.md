# Brütten Nete Maaş Hesaplama Aracı

## Tanım
2024 yılı için aylık olarak matrahları, sigortaları, vergileri ve net ödenecek miktarı hesaplar; sonuçları bir txt dosyasına yazar.

## Özellikler
### Sosyal Ödemeler
Yakacak yardımı, sosyal yardım, yemek parası, yol parası gibi ek ödemeleri hesaba katar
### 6 aylık enflasyon
Enflasyon oranlarını girerek ikinci altı ayda yatacak olan maaşı enflasyon oranına göre hesaplar
### Sendika Aidatı
Sendikanın brüt ücret üzerinden aldığı aidatı hesaba katar.

## Kullanım
### Config
Config kısmındaki veriler çalışma şartlarında göre düzenlenir
#### Ayın Günleri
day_of_months -> Her ay için gün sayısı kısmında her üç ayda bir 15 gün prim alınacakmış gibi veri girilmiştir.

weekdays_of_months -> Haftada 5 gün çalışan birisi için resmi tatiller hesaba katılarak aylık iş günü verisi oluşturulmuştur
#### Vergi
tax_bracket_ceilings -> Vergi dilimi tavanları

tax_rates -> Vergi dilimlerindeki vergi oranları

tax_bracket_amounts -> Vergi dilimleri doldurulduğunda ödenmiş olan miktar

minimum_wage_tax_exempt -> Asgari ücret vergi istisnası

minimum_wage_stamp_exempt -> Asgari ücret damga vergisi istisnası
#### Yemek
food_payment -> Her ay için günlük yemek ücretleri

food_pay_insurance -> Her ay için günlük yemek ücretinden ödenen sigorta

food_pay_tax -> Her ay için günlük yemek ücretinden ödenen vergi
#### Sendikal
union_cut -> Sendika kesintisi (gün olarak, %70 için 0.7)

social_payment -> Aylık sosyal ödemeler

fuel_payment -> Aylık yakacak ödemesi
#### Rapor
allowed_times_of_sick_leave -> Bir yıl içerisinde izin verilen rapor sayısı

days_allowd_per_sick_days -> Bir rapor alındığında işveren tarafından karşılanan en yüksek gün sayısı

#### inflation -> Ocak ayından başlayarak aylık enflasyon oranları

### print_bordro Fonksiyonun Çağırılması
print_bordro fonksiyonu aylık rapor günleri, izinler, günlük brüt ücret ve haziranda zam olup olmayacağı belirtilerek çağırılır ve bordro.txt oluşturulur
#### Parametreler
sick_days -> bir dizin şeklinde 12 aylık her ay için raporlu gün sayısı. Örneğin ocak ve martta 2 gün, temmuzda 4 gün rapor alındıysa : [2,0,2,0,0,0,4,0,0,0,0,0]

vacation -> Yine bir dizin şeklinde 12 aylık her ay alınan izin sayısı. Örneğin ocakta 5, mayısta 7 ve aralıkta 10 gün izin alan biri için: [5,0,0,0,7,0,0,0,0,0,0,10]

wage -> Ocaktaki günlük brüt ücret

june_raise -> Haziran sonu zam olma durumu
