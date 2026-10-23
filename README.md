# NFL Fantasy Draft Assistant (2024)

NFL fantasy football draft'ı sırasında yardımcı olan bir Tkinter masaüstü uygulaması. Haftalık oyuncu puanlarını içeren bir Excel dosyasını okur, her oyuncunun ortalama puanını hesaplar, oyuncuları pozisyona göre sıralar ve snake draft sırasına göre hangi seçimde kimin kalabileceğini tahmin eder.

> Sadece yardımcı bir araçtır; önerileri geçmiş puan ortalamalarına dayanır ve kesin sonuç vermez.

**Sürümler:** Bu repo projenin **2024** sürümüdür. Sonraki sezonlar ayrı repolarda geliştirildi:
[nfl-fantasy-draft-assistant-2025](https://github.com/muhammetaliyoldar/nfl-fantasy-draft-assistant-2025) ve
[nfl-draft-asistant-2026](https://github.com/muhammetaliyoldar/nfl-draft-asistant-2026).

## Özellikler

- **Excel'den veri yükleme:** `.xlsx` dosyasındaki tüm sayfalar birleştirilir; her oyuncunun `TOTAL` puanlarının ortalaması alınır.
- **Pozisyon listeleri:** QB, RB, WR ve TE oyuncuları ortalama puana göre azalan sırada ayrı listelerde gösterilir.
- **Snake draft tahmini:** Takım sayısı ve kendi draft sıranız girildiğinde 13 turluk snake draft sırası çıkarılır; yapılmış seçimler yerinde tutulur, kalan seçimler en yüksek ortalamalı uygun oyuncuyla doldurularak "Muhtemel" listesi oluşturulur. İlk 7 seçimden sonrakiler "(Yedek)" olarak işaretlenir.
- **Seçim takibi:** Seçilen oyuncular "Takımım"a ya da başkalarının seçimi olarak "Draftlandı" listesine taşınır; takımınızın toplam ortalama puanı gösterilir.

## Teknoloji yığını

Python 3, Tkinter, pandas (Excel okumak için `openpyxl` gerekir).

## Klasör yapısı

```
nfl_fantasy_draft_assistant.py   # uygulamanın tamamı (FantasyDraftAssistant sınıfı)
FantasyFootballWeekly.xlsx       # örnek veri: FF_Week1 ... FF_Week18 sayfaları
read_me.txt                      # kısa not
.idea/                           # PyCharm proje ayarları
```

## Kurulum

```bash
git clone https://github.com/muhammetaliyoldar/nfl_fantasy_draft_assistant.git
cd nfl_fantasy_draft_assistant
pip install pandas openpyxl
```

Linux'ta Tkinter ayrı bir paket olabilir (ör. Ubuntu'da `sudo apt install python3-tk`).

## Kullanım

```bash
python nfl_fantasy_draft_assistant.py
```

1. **XLSX Dosyasını Yükle** ile `FantasyFootballWeekly.xlsx` dosyasını (ya da aynı biçimde bir dosyayı) seçin.
2. **Draft Ekranına Geç**'e tıklayın, takım sayısını ve kendi draft sıranızı girip **Başla**'ya basın.
3. Draft ilerledikçe pozisyon listelerinden oyuncu seçip **Takıma Ekle** (sizin seçiminiz) ya da **Draftlandı Ekle** (başka takımın seçimi) düğmesine basın.
4. "Muhtemel" listesi her seçimden sonra güncellenir; **Güncelle** ile listeleri yeniden hesaplatabilirsiniz.

### Veri biçimi

Her sayfa bir haftayı temsil eder ve en az şu sütunları içermelidir: `PLAYER NAME`, `PLAYER POSITION`, `TOTAL`. Örnek dosyada ayrıca takım, rakip, projeksiyon ve pas/koşu/yakalama istatistik sütunları bulunur.

## Bilinen sorunlar

- **Oyuncu Ara** düğmesi hata veriyor: `search_player` içindeki `rename(columns({...}))` çağrısı `rename(columns={...})` olmalı.
- **Listeden Kaldır**, oyuncunun pozisyonunu liste metninden bulmaya çalışıyor ama metinde pozisyon olmadığı için oyuncu pozisyon listesine geri konamıyor.
- Takımdaki ve draftlanan oyuncuların listeleri kaydedilmiyor; uygulama kapanınca sıfırlanır.

## Proje durumu

2 Eylül 2024'te yayımlandı (3 commit) ve o tarihten beri güncellenmedi. Geliştirme 2025 ve 2026 repolarında devam ediyor. Repoda lisans dosyası yok.
