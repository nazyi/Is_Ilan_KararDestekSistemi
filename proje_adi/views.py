from django.shortcuts import render  
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import os
import csv
from django.http import JsonResponse
from django.conf import settings
from django.utils.html import mark_safe
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import subprocess
from django.http import Http404

from django.contrib import messages
def homepage(request):
    error_message = None  # Başlangıçta hata mesajı None (boş) olmalı

    if request.method == 'POST':
        # Şirket girişi kontrolü
        if 'company_login' in request.POST:
            company_name_input = request.POST.get('company_name', '')
            password_input = request.POST.get('password', '')

            file_path1 = 'company_name.csv'
            with open(file_path1, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)

                # CSV dosyasındaki her satır için kontrol yap
                for row in reader:
                    if len(row) == 3:  # Satırda tam 3 sütun varsa
                        company_name_csv = row[1]  # 2. sütun: şirket adı
                        password_csv = row[2]  # 3. sütun: şifre

                    # Şirket adı ve şifreyi kontrol et
                        if company_name_csv == company_name_input and password_csv == password_input:
                            request.session['company_name'] = company_name_csv.strip()
                            return redirect('company_homepage', company_name=company_name_csv)
                         

                    elif len(row) > 3:  # Satırda 3'ten fazla sütun varsa
                        company_name_csv = row[1]  # 2. sütun: şirket adı
                        password_csv = row[-1]  # Son sütun: şifre

                    # Şirket adı ve şifreyi kontrol et
                    if company_name_csv == company_name_input and password_csv == password_input:
                        request.session['company_name'] = company_name_csv.strip()
                        return redirect('company_homepage', company_name=company_name_csv)

                # Eğer eşleşme bulunmazsa, hata mesajı ver
                error_message = "Şirket adı veya şifre yanlış!"  # Giriş başarısız

        # Personel girişi kontrolü
        elif 'personnel_login' in request.POST:
            personel_email_input = request.POST.get('personel_email', '')
            password_input = request.POST.get('personel_password', '')

            # Personel verilerini kontrol et
            file_path = 'personel-bilgi.csv'
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)

                # CSV dosyasındaki her satır için kontrol yap
                for row in reader:
                    if len(row) == 7:  # Satırda 7 sütun varsa (ID + diğer bilgiler)
                        personel_email_csv = row[5]  # 6. sütun: personel maili
                        password_csv = row[6] 
                        personel_id = row[0]
                        # Personel adı ve şifreyi kontrol et
                        if personel_email_csv == personel_email_input and password_csv == password_input:
                            request.session['personel_email'] = personel_email_csv.strip()
                            request.session['personel_password'] = password_csv.strip()
                            request.session['personel_id'] = personel_id.strip()
                            return redirect('personel_homepage', personel_email=personel_email_csv)

                # Eğer eşleşme bulunmazsa, hata mesajı ver
                error_message = "Personel adı veya şifre yanlış!"  # Giriş başarısız

    return render(request, 'homepage.html', {
        'error_message': error_message  # Hata mesajı
    })
def get_new_id():
    id_file_path = 'id_file.txt'
    # ID'yi saklayan dosya var mı kontrol et
    if os.path.exists(id_file_path):
        with open(id_file_path, 'r') as f:
            last_id = int(f.read().strip())  # Son ID'yi oku
        new_id = last_id + 1

    # Yeni ID'yi sakla
    with open(id_file_path, 'w') as f:
        f.write(str(new_id))

    return new_id
def write_headers_if_not_exists(file_path):
    file_path = 'company_name.csv'
    # Dosya yoksa başlıkları yaz
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Konum','Telefon Numarası', 'Açık Adres', 
                             'Sektör', 'Şirket Türü', 'Çalışan Sayısı'])
@csrf_exempt
def about(request):
    file_path = 'company_name.csv'

    # Başlıkları kontrol edip yazdır
    write_headers_if_not_exists(file_path)

    if request.method == 'POST':
        # Formdan gelen verileri al
        company_name = request.POST.get('company_name', '')
        location = request.POST.get('location', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        sector = request.POST.get('sector', '')
        company_type = request.POST.get('company_type', '')
        employee_count = request.POST.get('employee_count', '')
        password = request.POST.get('password', '')

        company_id = get_new_id()
        
        # Verileri CSV dosyasına yaz
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([company_id,company_name, location, phone, address, sector, company_type, employee_count, password])

        print(f"Yeni şirket kaydedildi:  {company_id},{company_name}, {location}, {phone}, {address}, {sector}, {company_type}, {employee_count}, {password}")
       # return HttpResponse("Şirket başarıyla kaydedildi!")

    return render(request, 'about.html')
def read_csv(request):
    data = []
    with open('company_name.csv', mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return JsonResponse({'companies': data})
def company_homepage(request, company_name):
    
    company_name_from_session = request.session.get('company_name', 'Anonim')
    # Şirket bilgilerinin olduğu CSV dosyasının yolu
    company_file_path = os.path.join(settings.BASE_DIR, 'company_name.csv')

    # İlanların olduğu CSV dosyasının yolu
    job_file_path = os.path.join(settings.BASE_DIR, 'sayfa1.csv')

    try:
        # Şirket doğrulama işlemi
        with open(company_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Başlık satırını atla

            company_found = False
            for row in reader:
                if len(row) == 3:  # 3 sütunlu satırlar için
                    _, company_name_csv, password_csv = row
                elif len(row) > 3:  # Daha fazla sütun varsa
                    _, company_name_csv, *_, password_csv = row

                if company_name_csv == company_name:
                    company_found = True
                    break

        if not company_found:
            return HttpResponse("Şirket bulunamadı!", status=404)

        # Şirket ilanlarını filtreleme işlemi
        jobs = []
        with open(job_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Şirket adını 'SirketAdi' sütununda kontrol ediyoruz
                if row.get('SirketAdi', '').strip().lower() == company_name.strip().lower():
                    jobs.append({
                        'Ilan_id': row.get('Ilan_id', '').strip(),  # İlanın ID'sini alıyoruz
                        'sektor': row.get('Sektor', '').strip(),
                        'konum': row.get('Konum', '').strip(),
                        'aciklama': mark_safe(row.get('Aciklama', '').strip().replace('\n', '<br>')),
                        'pozisyon': row.get('Pozisyon', '').strip(),
                        'deneyim': row.get('Deneyim', '').strip(),
                        'egitim': row.get('Egitim', '').strip(),
                        'calisma_sekli': row.get('CalismaSekli', '').strip(),
                    })
                    
        # Template'e veri gönder
        return render(request, 'company_homepage.html', {
            'company_name': company_name,
            'jobs': jobs,
            
        })
    
    except FileNotFoundError:
        return HttpResponse("CSV dosyası bulunamadı!", status=500)
def get_ilan_id():
    ilan_id_path = 'ilan_id.txt'
    # ID'yi saklayan dosya var mı kontrol et
    if os.path.exists(ilan_id_path):
        with open(ilan_id_path, 'r') as f:
            last_id = int(f.read().strip())  # Son ID'yi oku
        new_id = last_id + 1

    # Yeni ID'yi sakla
    with open(ilan_id_path, 'w') as f:
        f.write(str(new_id))

    return new_id
def add_job(request):

    if request.method == 'POST':
        # Form verilerini al
        sektor = request.POST.get('sektor')
        konum = request.POST.get('konum')
        aciklama = request.POST.get('aciklama')
        pozisyon = request.POST.get('pozisyon')
        deneyim = request.POST.get('deneyim')
        egitim = request.POST.get('egitim')
        calisma_sekli = request.POST.get('calisma_sekli')

        # Giriş yapan şirketin adı
        company_name = request.session.get('company_name')

        # Yeni ID al
        ilan_id = get_ilan_id()

        # CSV dosyasının yolu
        csv_file_path = os.path.join(settings.BASE_DIR, 'sayfa1.csv')

        # CSV dosyasına yaz
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([ilan_id, company_name, sektor, konum, aciklama, pozisyon, deneyim, egitim, calisma_sekli])

        # İlanlar sayfasına yönlendir
        return HttpResponseRedirect(reverse('add_job'))

    return render(request, 'add_job.html')
def edit_job(request, company_name, job_id):
    company_file_path = os.path.join(settings.BASE_DIR, 'company_name.csv')
    job_file_path = os.path.join(settings.BASE_DIR, 'sayfa1.csv')

    # Şirket doğrulama işlemi
    try:
        # Şirket kontrolü
        with open(company_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Başlık satırını atla

            company_found = False
            for row in reader:
                if len(row) == 3:  # 3 sütunlu satırlar için
                    _, company_name_csv, password_csv = row
                elif len(row) > 3:  # Daha fazla sütun varsa
                    _, company_name_csv, *_, password_csv = row

                if company_name_csv == company_name:
                    company_found = True
                    break

        if not company_found:
            return HttpResponse("Şirket bulunamadı!", status=404)

        # İlanı job_id ile bulma
        job = None
        with open(job_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('Ilan_id', '').strip() == str(job_id).strip():
                    job = {
                        'job_id': row.get('Ilan_id', '').strip(),
                        'sektor': row.get('Sektor', '').strip(),
                        'konum': row.get('Konum', '').strip(),
                        'aciklama': mark_safe(row.get('Aciklama', '').strip().replace('\n', '<br>')),
                        'pozisyon': row.get('Pozisyon', '').strip(),
                        'deneyim': row.get('Deneyim', '').strip(),
                        'egitim': row.get('Egitim', '').strip(),
                        'calisma_sekli': row.get('CalismaSekli', '').strip(),
                    }
                    break

        if not job:
            return HttpResponse("İlan bulunamadı!", status=404)

        # POST isteği ile gelen verileri işleme
        if request.method == 'POST':
            company_name = request.session.get('company_name')
            password = request.session.get('password')

            sektor = request.POST.get('sektor')
            konum = request.POST.get('konum')
            pozisyon = request.POST.get('pozisyon')
            deneyim = request.POST.get('deneyim')
            egitim = request.POST.get('egitim')
            calisma_sekli = request.POST.get('calisma_sekli')
            aciklama = request.POST.get('aciklama')

            # CSV dosyasını güncelleme
            updated_jobs = []
            job_found = False  # İlanı bulup bulmadığımızı kontrol etmek için

            with open(job_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = ['Ilan_id', 'SirketAdi', 'Sifre', 'Sektor', 'Konum', 'Pozisyon', 'Deneyim', 'Egitim', 'CalismaSekli', 'Aciklama']

                # Tüm ilanları oku ve sadece ilgili ilanı güncelle
                for row in reader:
                    if row.get('Ilan_id', '').strip() == str(job_id).strip():
                        job_found = True
                        row['SirketAdi'] = company_name  # Şirket adını güncelliyoruz
                        row['Sifre'] = password  # Şifreyi güncelliyoruz
                        row['Sektor'] = sektor
                        row['Konum'] = konum
                        row['Pozisyon'] = pozisyon
                        row['Deneyim'] = deneyim
                        row['Egitim'] = egitim
                        row['CalismaSekli'] = calisma_sekli
                        row['Aciklama'] = aciklama  # Aciklamayı güncelliyoruz
                        row['Ilan_id'] = job_id

                    updated_jobs.append({k: row[k] for k in fieldnames})  # Tüm ilanları ekliyoruz

            if not job_found:
                return HttpResponse("İlan bulunamadı!", status=404)

            # Güncellenmiş veriyi CSV dosyasına yazıyoruz
            with open(job_file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_jobs)  # Tüm ilanları yazarız

            return redirect('company_homepage', company_name=company_name)

        return render(request, 'edit_job.html', {
            'company_name': company_name,
            'job': job
        })
    
    except FileNotFoundError:
        return HttpResponse("CSV dosyası bulunamadı!", status=500)
@csrf_exempt
def personel_uye_ol(request):
    file_path = 'personel-bilgi.csv'

    # Başlıkları kontrol edip yazdır
    write_headers_if_not_exists2(file_path)

    if request.method == 'POST':
        # Formdan gelen verileri al
        name = request.POST.get('name', '')
        telefon_no = request.POST.get('phone', '')
        cinsiyet = request.POST.get('gender', '')
        yas = request.POST.get('age', '')
        mail = request.POST.get('mail', '')
        sifre = request.POST.get('sifre', '')

        new_id = get_new_id2(file_path)

        
        # Verileri CSV dosyasına yaz
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([new_id,name, telefon_no, cinsiyet, yas, mail, sifre])
        return redirect('personel_uye_ol')  # Başarılı bir kayıt sonrası sayfayı tekrar yükle

    return render(request, 'personel_uye_ol.html')
def write_headers_if_not_exists2(file_path):

    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Ad/Soyad', 'Telefon No', 'Cinsiyet', 'Yaş', 'Mail', 'Şifre'])
def get_new_id2(file_path):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return 1  # Eğer dosya yoksa veya boşsa, ID 1'den başlasın
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Eğer dosya sadece başlık satırından oluşuyorsa (yani veri yoksa)
        if len(rows) == 1:  # Başlık satırını içerir
            return 1

        last_row = rows[-1]  # Son satırı al
        last_id = int(last_row[0])  # ID sütunu
        return last_id + 1  # Son ID'yi 1 arttır
    
def personel_homepage(request, personel_email):
    # Oturumdaki 'personel_email' bilgisini alıyoruz
    personel_email = request.session.get('personel_email', None)
    personel_password = request.session.get('personel_password', None)
    
    if not personel_email or not personel_password:
        return HttpResponse("Giriş yapmanız gerekiyor.", status=401)

    # CSV dosyasındaki bilgileri okuma
    file_path = 'personel-bilgi.csv'

    personel_name = None
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # CSV dosyasındaki her satır için kontrol yap
            for row in reader:
                if len(row) >= 7:  # Satırda en az 7 sütun olduğunu kontrol et
                    # Personel e-posta ve şifreyi kontrol et
                    personel_email_csv = row[5].strip()  # E-posta adresi 6. sütunda
                    personel_password_csv = row[6].strip()  # Şifre 7. sütunda

                    # E-posta ve şifreyi karşılaştır
                    if personel_email == personel_email_csv and personel_password == personel_password_csv:
                        personel_name = row[1].strip()  # Ad bilgisi 2. sütunda
                        break  # Eşleşme bulduktan sonra döngüyü sonlandır

    basvuru_listesi = []
    with open('basvurular.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Her satırda mail sütunu en son sütundur (index -1)
        for row in reader:
            if row[-1] == personel_email:  # Mail eşleşmesi
                basvuru_listesi.append(row)  # Eşleşen başvuruyu listeye ekle

    # Eğer personel bulunamazsa
    if not personel_name:
        return HttpResponse("Personel bilgileri bulunamadı.", status=404)

    return render(request, 'personel_homepage.html', {'personel_name': personel_name, 'basvuru_listesi': basvuru_listesi})

def job_application(request):
    # Filtre parametrelerini al
    sector_filter = request.GET.get('sector', '')
    location_filter = request.GET.get('location', '')
    position_filter = request.GET.get('position', '')
    company_name_filter = request.GET.get('company_name', '')

    # CSV dosyasını okuma işlemi
    with open('sayfa1.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    # Filtreleme işlemi
    filtered_rows = []
    for row in rows:
        if len(row) > 8:
            # Filtreleme koşullarını ekle
            if (sector_filter.lower() in row[2].lower() or not sector_filter) and \
               (location_filter.lower() in row[3].lower() or not location_filter) and \
               (position_filter.lower() in row[5].lower() or not position_filter) and \
               (company_name_filter.lower() in row[1].lower() or not company_name_filter):
                filtered_rows.append(row)

    # Sayfalama işlemi
    paginator = Paginator(filtered_rows, 5)  # Her sayfada 5 ilan
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recommended_jobs = get_recommended_jobs_for_user(request)

    # Render'a gönderilecek veriler
    return render(request, 'job_application.html', {
        'page_obj': page_obj,
        'sector_filter': sector_filter,
        'location_filter': location_filter,
        'position_filter': position_filter,
        'company_name_filter': company_name_filter,
        'recommended_jobs': recommended_jobs,
    })
def add_cv(request):
    if request.method == 'POST':
        # CV formundan gelen bilgileri al
        konum = request.POST.get('konum')
        diller = request.POST.get('diller')
        egitim_seviyesi = request.POST.get('egitim_seviyesi')
        okul = request.POST.get('okul')
        bolum = request.POST.get('bolum')
        yetenekler = request.POST.get('yetenekler')
        tecrube_senesi = request.POST.get('tecrube_senesi')
        tanitma_metni = request.POST.get('tanitma_metni')
        kullanici_mail = request.session.get('personel_email')  # Kullanıcı oturumu e-posta ile takip ediliyor

        # Kullanıcının temel bilgilerini personel_bilgi.csv'den al
        temel_bilgiler = []
        with open('personel-bilgi.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[5] == kullanici_mail:  # E-posta eşleşmesi
                    temel_bilgiler = row
                    break

        if temel_bilgiler:
            # CV bilgileriyle birleştirip cv_bilgileri.csv'ye yaz
            with open('cv_bilgileri.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(temel_bilgiler + [konum, diller, egitim_seviyesi, okul, bolum, yetenekler, tecrube_senesi, tanitma_metni])


            return render(request, 'add_cv.html', {'cv_kaydedildi': True})

    return render(request, 'add_cv.html')

def job_detail(request, ilan_id):
    # CSV dosyasını okuma işlemi
    with open('sayfa1.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # İlanı ID'ye göre bul
    ilan_detay = None
    for row in rows:
        if row[0] == ilan_id:  # İlk sütun ilan ID
            ilan_detay = {
                'ilan_id': row[0],
                'company_name': row[1],
                'sector': row[2],
                'location': row[3],
                'description': row[4],
                'position': row[5],
                'experience': row[6],
                'education': row[7],
                'work_type': row[8],
            }
            break


    # Detay sayfasını render et
    return render(request, 'job_detail.html', {'ilan_detay': ilan_detay})
def job_apply(request, ilan_id):
    # Başvuru işlemi için CSV dosyasını aç
    with open('sayfa1.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
    personel_email = request.session.get('personel_email', None)
    # Başvurulacak ilanı bul
    ilan = next((row for row in rows if row[0] == ilan_id), None)

    if not ilan:
        return HttpResponseRedirect(reverse('job_detail', args=[ilan_id]))

    # Başvuru bilgilerini CSV'ye kaydet
    with open('basvurular.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Başvuran kişinin e-posta adresini ve ilanın bilgilerini yaz
        writer.writerow([ilan[0], ilan[1], ilan[2], ilan[3], ilan[5], ilan[6], ilan[7], ilan[8], personel_email])  # request.user.email başvuran kişinin e-posta adresi

    # Başvuruyu başarıyla kaydettikten sonra aynı sayfada kal
    return HttpResponseRedirect(reverse('job_detail', args=[ilan_id]))
import pandas as pd
def sirket_job_detail(request, company_name, job_id):
    # CSV dosyalarının yolu
    job_file_path = 'sayfa1.csv'  # İş ilanlarını içeren CSV dosyasının yolu
    basvuru_file_path = 'basvurular.csv'  # Başvuruların olduğu CSV dosyasının yolu
    cv_file_path = 'cv_bilgileri.csv'  # Başvuranların CV bilgilerini içeren CSV dosyasının yolu

    job = None  # Başlangıçta iş ilanı yok
    applicants = []  # Başvuran kişileri tutacağız

    # İş ilanlarını CSV dosyasından oku
    with open(job_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            ilan_id = row[0]
            if ilan_id.strip() == job_id:  # job_id ile eşleşen ilanı bul
                job = {
                    'Ilan_id': row[0],
                    'company_name': row[1],
                    'sektor': row[2],
                    'konum': row[3],
                    'aciklama': row[4],
                    'pozisyon': row[5],
                    'deneyim': row[6],
                    'egitim': row[7],
                    'calisma_sekli': row[8]
                }
                break  # Eşleşen ilan bulunduysa döngüyü sonlandır

    if job is None:
        raise Http404("İş ilanı bulunamadı.")

    # Başvuran kişileri `basvurular.csv` dosyasından oku
    with open(basvuru_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            basvuru_job_id = row[0]
            basvuru_email = row[8].strip()
            if basvuru_job_id.strip() == job_id:  # Başvurulan işin ID'si ile eşleşenleri bul
                applicants.append(basvuru_email)  # Başvuran kişinin mailini ekle

    applicant_details = []
    with open(cv_file_path, mode = 'r', newline = '', encoding = 'utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cv_email = row[5].strip()
            if cv_email in applicants:
                applicant_details.append({
                    'email':row[5],
                    'isim':row[1],
                    'telefon':row[2],
                    'cinsiyet':row[3],
                    'yas':row[4],
                    'konum':row[7],
                    'dil':row[8],
                    'egitim_seviyesi':row[9],
                    'okul':row[10],
                    'bolum':row[11],
                    'yetenek':row[12],
                    'tecrube':row[13],
                    'tanitmaMetni':row[14],
                })

    recommended_candidates = get_recommended_candidates(ilan_id)

    return render(request, 'sirket_job_detail.html', {'job': job, 'company_name': company_name,'recommended_candidates':recommended_candidates, 'applicant_details':applicant_details})

def get_recommended_candidates(job_id):
    # CSV dosyalarını yükle
    skor_df = pd.read_csv('skor.csv')
    cv_df = pd.read_csv('cv_bilgileri.csv')

    # İlgili ilan_id'ye göre skorları filtrele
    job_scores = skor_df[skor_df['ilan_id'].astype(str) == job_id]

    # Skorlara göre sırala ve en yüksek 5 adayı seç
    top_scores = job_scores.sort_values(by='Benzerlik_Skoru', ascending=False).head(5)

    # Skorları CV bilgileriyle birleştir
    recommended_candidates = pd.merge(
        top_scores, 
        cv_df[['id', 'AdSoyad', 'eMail', 'Telefon', 'Cinsiyet', 'Yas', 'Okul', 'Bolum', 'Yetenekler', 'TanıtmaMetni', 'Konum', 'Dil', 'EgitimSeviyesi', 'Tecrube']], 
        on='id', 
        how='left'
    )

    # Gerekli sütunları seçerek döndür
    return recommended_candidates.to_dict(orient='records')

def get_recommended_jobs_for_user(request):
    # skor.csv ve job detaylarını yükleme
    personel_email = request.session.get('personel_email')

    personel_id = get_user_id_from_email(personel_email)
    skor_df = pd.read_csv('skor.csv')
    job_df = pd.read_csv('sayfa1.csv')  # İlanların detayları burada olacak, iş ilanı hakkında açıklama vs.
    
    # Kullanıcı ID'sine göre skorları filtreleme
    user_scores = skor_df[skor_df['id'] == personel_id]

    # En yüksek skorları al
    top_jobs = user_scores.sort_values(by='Benzerlik_Skoru', ascending=False).head(5)
    
    # İlan detaylarını almak
    recommended_jobs = pd.merge(top_jobs, job_df, left_on='ilan_id', right_on='Ilan_id', how='left')
    return recommended_jobs.to_dict(orient='records')


def get_user_id_from_email(email):
    cv_df = pd.read_csv('cv_bilgileri.csv')
    user_info = cv_df[cv_df['eMail'] == email]
    if not user_info.empty:
        return user_info.iloc[0]['id']  # Eşleşen kişinin ID'sini döndür
    else:
        return None  # E-posta bulunmazsa None döner
    
from django.shortcuts import render # type: ignore
from utils.sayfa1 import process_data

def yeni_ilan_ekle_anlamli(request):
    if request.method == "POST":
        # NLP işlemleri burada yapılır
        process_data()  # Örneğin, CSV dosyasını işleyen bir fonksiyon
        return render(request, "success.html", {"message": "NLP işlemleri başarıyla tamamlandı!"})
    
    # Eğer GET ile erişilirse
    return render(request, "add_job.html")

from django.shortcuts import render # type: ignore
from utils.eslestirme import ilan_cv_eslestirme
import pandas as pd # type: ignore


def eslestirme(request):
    if request.method=="POST":
        ilan_cv_eslestirme()
        return render(request, "success.html", {"message": "NLP işlemleri başarıyla tamamlandı!"})


from django.shortcuts import render # type: ignore
from utils.skor import skor_hesapla
import pandas as pd # type: ignore

def SkorHesapla(request):
    if request.method=="POST":
        skor_hesapla()
        return render(request, "success.html", {"message": "NLP işlemleri başarıyla tamamlandı!"})
    
from django.shortcuts import render # type: ignore
from utils.ozgecmis import ozgecmis_eslesme
import pandas as pd # type: ignore

def Ozgecmis(request):
    if request.method=="POST":
        ozgecmis_eslesme()
        return render(request, "success.html", {"message": "NLP işlemleri başarıyla tamamlandı!"})
