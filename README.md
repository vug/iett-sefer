# IETT Bus Locations

Uses [İETT Sefer Gerçekleşme Web Servisi \- Veri Setleri \- İBB](https://data.ibb.gov.tr/dataset/sefer-gerceklesme-web-servisi) to fetch and visualize locations of Istanbul's public buses every two minutes.

![screenshot](https://user-images.githubusercontent.com/6636020/86426154-f643e000-bcb4-11ea-914c-6ce77b694807.png)

("Tadpole"s tail is the position 2 minutes ago, and head is bus' current position.)

## Deployment

Run the script that fetches all bus coordinates every two minutes

```bash
python take_snapshot.py
```

Run the Bokeh server

```bash
bokeh serve --show app.py
```

Profit!
