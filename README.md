# 2D/3D Asset Downloader

Ücretsiz 2D ve 3D oyun asset'lerini çeşitli sitelerden otomatik olarak indiren Python uygulaması.

## 🎯 Özellikler

- **Çoklu Site Desteği**: Kenney, OpenGameArt, Itch.io, GameIcons ve daha fazlası
- **Akıllı Scraping**: Rate limiting ve etik scraping kuralları
- **Veritabanı Yönetimi**: SQLite tabanlı asset veritabanı
- **Filtreleme ve Arama**: Asset türü, kategori ve site bazında filtreleme
- **Toplu İndirme**: Çoklu asset indirme desteği
- **İnteraktif Mod**: Kullanıcı dostu komut satırı arayüzü

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adım 1: Projeyi İndirin

```bash
git clone https://github.com/kullaniciadi/2d-3d-asset-downloader.git
cd 2d-3d-asset-downloader
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

## 📖 Kullanım

### Komut Satırı Kullanımı

```bash
# Yardım menüsü
python main.py --help

# Tüm sitelerden asset'leri tara
python main.py scrape --site all

# Belirli bir siteden asset'leri tara
python main.py scrape --site kenney --limit 50

# Asset'leri indir
python main.py download --type 2d --limit 10

# Asset'leri ara
python main.py search "character sprite"

# Asset'leri listele
python main.py list --type 3d --limit 20

# İstatistikleri göster
python main.py stats

# İnteraktif mod
python main.py interactive
```

### İnteraktif Mod Komutları

```
> scrape kenney          # Kenney sitesinden asset'leri tara
> download 2d            # 2D asset'leri indir
> search "platformer"    # "platformer" kelimesini ara
> list 3d                # 3D asset'leri listele
> stats                  # İstatistikleri göster
> help                   # Yardım menüsü
> quit                   # Çıkış
```

## 🎮 Desteklenen Siteler

| Site | Durum | Açıklama |
|------|-------|----------|
| Kenney | ✅ Aktif | Ücretsiz oyun asset'leri |
| OpenGameArt | ✅ Aktif | Açık kaynak oyun sanatı |
| Itch.io | ✅ Aktif | Oyun asset'leri |
| GameIcons | ✅ Aktif | Oyun ikonları |
| CraftPix | ⚠️ Sınırlı | Kayıt gerekli |
| Freepik | ❌ Devre Dışı | Bot koruması |
| Pixabay | ❌ Devre Dışı | Bot koruması |

## 📁 Proje Yapısı

```
2d-3d-asset-downloader/
├── main.py                 # Ana uygulama dosyası
├── asset_manager.py        # Asset yönetimi
├── database.py            # Veritabanı işlemleri
├── downloader.py          # İndirme işlemleri
├── config.py              # Yapılandırma
├── requirements.txt       # Python bağımlılıkları
├── scrapers/              # Site-specific scraper'lar
│   ├── kenney_scraper.py
│   ├── opengameart_scraper.py
│   └── ...
├── downloads/             # İndirilen dosyalar
├── data/                  # Veri dosyaları
├── logs/                  # Log dosyaları
└── security/              # Güvenlik modülleri
```

## ⚙️ Yapılandırma

`config.py` dosyasında aşağıdaki ayarları değiştirebilirsiniz:

- **Rate Limiting**: Site bazında istek sınırları
- **İndirme Ayarları**: Eş zamanlı indirme sayısı, timeout değerleri
- **Site Ayarları**: Hangi sitelerin aktif olduğu
- **User Agent**: Tarayıcı kimliği

## 🔒 Güvenlik ve Etik

Bu uygulama etik web scraping kurallarına uygun olarak tasarlanmıştır:

- **Rate Limiting**: Sunucuları aşırı yüklememek için istek sınırları
- **User Agent Rotation**: Gerçek tarayıcı kimlikleri
- **Gecikme Süreleri**: İstekler arası rastgele gecikmeler
- **Robots.txt Uyumu**: Site kurallarına uyum

## 🐛 Sorun Giderme

### Yaygın Sorunlar

1. **Bağlantı Hatası**: İnternet bağlantınızı kontrol edin
2. **Rate Limiting**: Daha uzun gecikme süreleri ayarlayın
3. **Veritabanı Hatası**: `assets.db` dosyasını silip yeniden oluşturun

### Log Dosyaları

Hata ayıklama için `logs/` klasöründeki log dosyalarını kontrol edin.

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## ⚠️ Sorumluluk Reddi

Bu uygulama eğitim amaçlıdır. Kullanıcılar, hedef sitelerin kullanım şartlarına uygun olarak kullanmaktan sorumludur. Geliştirici, bu araçların kötüye kullanımından sorumlu değildir.

## 📞 İletişim

Sorularınız için GitHub Issues kullanın veya [email@example.com] adresine e-posta gönderin.

---

**Not**: Bu uygulama sadece ücretsiz ve açık kaynak asset'ler için tasarlanmıştır. Telif hakkı korumalı içeriklerin indirilmesi için kullanılmamalıdır.
"# 2d_3d_asset_scrapper" 
