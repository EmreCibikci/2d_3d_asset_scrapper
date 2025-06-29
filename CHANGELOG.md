# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecektir.

Format [Keep a Changelog](https://keepachangelog.com/tr/1.0.0/) standardına dayanmaktadır,
ve bu proje [Semantic Versioning](https://semver.org/spec/v2.0.0.html) kullanmaktadır.

## [1.0.0] - 2024-01-XX

### Eklenen
- İlk sürüm yayınlandı
- Çoklu site desteği (Kenney, OpenGameArt, Itch.io, GameIcons)
- SQLite veritabanı entegrasyonu
- Komut satırı arayüzü
- İnteraktif mod
- Rate limiting ve etik scraping
- Asset filtreleme ve arama
- Toplu indirme özelliği
- User agent rotation
- Güvenlik modülleri

### Özellikler
- `scrape` komutu: Sitelerden asset'leri tarama
- `download` komutu: Asset'leri indirme
- `search` komutu: Asset'leri arama
- `list` komutu: Asset'leri listeleme
- `stats` komutu: İstatistikleri gösterme
- `interactive` komutu: İnteraktif mod

### Desteklenen Siteler
- Kenney (kenney.nl)
- OpenGameArt (opengameart.org)
- Itch.io (itch.io)
- GameIcons (game-icons.net)
- CraftPix (craftpix.net) - Sınırlı
- Freepik (freepik.com) - Devre dışı
- Pixabay (pixabay.com) - Devre dışı

### Güvenlik
- Rate limiting implementasyonu
- User agent rotation
- Gecikme süreleri
- Robots.txt uyumu
- Proxy desteği (devre dışı)

### Teknik Detaylar
- Python 3.8+ desteği
- Async/await kullanımı
- SQLite veritabanı
- BeautifulSoup4 ile HTML parsing
- Requests ve aiohttp ile HTTP istekleri
- Pillow ile görüntü işleme

## [Unreleased]

### Planlanan
- Daha fazla site desteği
- GUI arayüzü
- API endpoint'leri
- Docker desteği
- Daha gelişmiş filtreleme
- Asset önizleme
- Otomatik güncelleme sistemi 