# IETT Bus Locations

Uses [İETT Sefer Gerçekleşme Web Servisi \- Veri Setleri \- İBB](https://data.ibb.gov.tr/dataset/sefer-gerceklesme-web-servisi) to fetch and visualize locations of Istanbul's public buses.

![screenshot](https://user-images.githubusercontent.com/6636020/86316998-4ad75480-bbfc-11ea-885a-5b4764eefc24.png)

Run the script that fetches all bus coordinates every two minutes

```bash
python take_snapshot.py
```

Run the Bokeh server

```bash
bokeh serve --show app.py
```

Profit!
