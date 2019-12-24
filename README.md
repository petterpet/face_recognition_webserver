# Face recognition with Webserver for Docker
# Gesichtserkennung inkl. Webserver für Docker

Das Docker Image basiert auf dem [face_recognition](https://github.com/ageitgey/face_recognition) Projekt. \
Das [Beispiel](https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/web_service_example.py) wurde so erweitert, dass beliebig viele bekannte Gesichter berücksichtigt werden können.


### *License / Lizenz*
The license can be found [here](https://raw.githubusercontent.com/ageitgey/face_recognition/master/LICENSE). \
Die Linzenz befindet sich [hier](https://raw.githubusercontent.com/ageitgey/face_recognition/master/LICENSE).


## Vorbereitung

1. In den Ordner ``data/known_faces`` müssen Bilder der bekannten Personen abgelegt werden. Der Dateiname sollte der Name der jeweiligen Person sein.

2. Container starten

```bash
docker-compose up -d
```

oder

```bash
docker build -t face_recognition:latest . && docker run -p 5001:5001 -v ./data/:/root/face_rec face_recognition
```

## Gesichter vergleichen

Auf den Webserver kann nun unter ``http://\<IP-Docker-Host\>:5001`` zugegriffen werden. \
Nun kann ein Bild hochgeladen werden und als Rückgabe erhält man folgendes JSON:

```JSON
{
  "status": "'OK' or 'ERROR'",
  "number_of_known_faces": "number",
  "face_found_in_image": "boolean",
  "known_face_found_in_image": "boolean",
  "persons_name": "string"
}
```

Der Status ist *ERROR*, falls der Ordner ``known_faces`` keine Bilder mit erkennbaren Gesichtern enthält.

Hinweis: Nachdem neue Bilder hinzugefügt wurden muss der Container neugestartet werden, damit die bekannten Gesichter neu eingelesen werden können.
