# Katkıda Bulunma Rehberi

Bu projeye katkıda bulunmak istediğiniz için teşekkürler! Bu rehber, projeye nasıl katkıda bulunabileceğinizi açıklar.

## 🚀 Başlarken

### Geliştirme Ortamını Kurma

1. Repository'yi fork edin
2. Yerel makinenizde clone edin:
   ```bash
   git clone https://github.com/YOUR_USERNAME/2d-3d-asset-downloader.git
   cd 2d-3d-asset-downloader
   ```

3. Sanal ortam oluşturun:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

5. Geliştirme bağımlılıklarını yükleyin:
   ```bash
   pip install -r requirements-dev.txt  # Eğer varsa
   ```

## 📝 Katkı Türleri

### 🐛 Hata Bildirimi

Hata bildirirken lütfen şunları ekleyin:
- İşletim sistemi ve Python sürümü
- Hata mesajının tam metni
- Hatanın nasıl oluşturulduğu
- Beklenen davranış

### ✨ Yeni Özellik Önerisi

Yeni özellik önerirken:
- Özelliğin amacını açıklayın
- Kullanım senaryolarını belirtin
- Varsa örnek kod ekleyin

### 🔧 Kod Katkısı

Kod katkısında bulunurken:

1. **Branch oluşturun**:
   ```bash
   git checkout -b feature/yeni-ozellik
   # veya
   git checkout -b fix/hata-duzeltmesi
   ```

2. **Değişikliklerinizi yapın**

3. **Test edin**:
   ```bash
   python main.py --help
   python main.py interactive
   ```

4. **Commit edin**:
   ```bash
   git add .
   git commit -m "feat: yeni özellik eklendi"
   ```

5. **Push edin**:
   ```bash
   git push origin feature/yeni-ozellik
   ```

6. **Pull Request oluşturun**

## 📋 Commit Mesajları

Commit mesajlarınızı şu formatta yazın:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Commit Türleri:
- `feat`: Yeni özellik
- `fix`: Hata düzeltmesi
- `docs`: Dokümantasyon değişikliği
- `style`: Kod formatı değişikliği
- `refactor`: Kod yeniden düzenleme
- `test`: Test ekleme veya düzenleme
- `chore`: Yapılandırma değişikliği

### Örnekler:
```
feat(scraper): yeni site desteği eklendi
fix(downloader): bağlantı hatası düzeltildi
docs(readme): kurulum talimatları güncellendi
```

## 🧪 Test Etme

### Manuel Test
```bash
# Temel işlevsellik testi
python main.py --help
python main.py stats

# Scraping testi
python main.py scrape --site kenney --limit 5

# İnteraktif mod testi
python main.py interactive
```

### Kod Kalitesi
- PEP 8 standartlarına uyun
- Type hints kullanın
- Docstring'ler ekleyin
- Gereksiz import'ları kaldırın

## 🔒 Güvenlik

### Web Scraping Kuralları
- Rate limiting'e uyun
- Robots.txt dosyalarını kontrol edin
- User agent'ları düzgün ayarlayın
- Gecikme sürelerini kullanın

### Güvenlik Kontrol Listesi
- [ ] Kullanıcı girdilerini doğrulayın
- [ ] SQL injection'a karşı koruma
- [ ] Dosya yollarını güvenli hale getirin
- [ ] Hassas bilgileri açıklamayın

## 📚 Dokümantasyon

### Kod Dokümantasyonu
- Tüm fonksiyonlar için docstring ekleyin
- Karmaşık algoritmaları açıklayın
- Örnek kullanım ekleyin

### README Güncellemeleri
- Yeni özellikler için dokümantasyon ekleyin
- Kurulum talimatlarını güncelleyin
- Örnek kullanımları ekleyin

## 🎯 Katkı Alanları

### Öncelikli Alanlar
1. **Yeni Site Desteği**: Daha fazla asset sitesi ekleme
2. **GUI Arayüzü**: Kullanıcı dostu grafik arayüzü
3. **API Geliştirme**: REST API endpoint'leri
4. **Performans İyileştirmeleri**: Daha hızlı scraping
5. **Test Coverage**: Unit test'ler ekleme

### Teknik İyileştirmeler
- Async/await optimizasyonu
- Veritabanı şeması iyileştirmeleri
- Hata yönetimi geliştirmeleri
- Logging sistemi

## 🤝 İletişim

- **GitHub Issues**: Hata bildirimi ve özellik önerileri
- **Discussions**: Genel tartışmalar
- **Pull Requests**: Kod katkıları

## 📄 Lisans

Bu projeye katkıda bulunarak, katkılarınızın MIT lisansı altında yayınlanacağını kabul etmiş olursunuz.

## 🙏 Teşekkürler

Katkıda bulunan herkese teşekkürler! Bu proje topluluk katkıları sayesinde daha iyi hale geliyor. 

git branch -M main
git remote add origin https://github.com/EmreCibikci/2d_3d_asset_scrapper.git 
git push -u --force origin main 