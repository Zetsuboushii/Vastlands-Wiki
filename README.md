<p align="center"><img src="/static/imgs/totv_logo.png" height="300px"  alt=""/></p>
<h1 align="center">Tome of the Vastlands</h1>
<p align="center"><strong><code>Vastlands-Wiki</code></strong></p>
<p align="center">Ein umfassendes Wiki und Wissensdatenbank für D&D-Kampagnen</p>
<p align="center">
  <img src="https://img.shields.io/maintenance/yes/2025"  alt=""/>
</p>


<!-- TOC -->

* [1. Einleitung](#1-einleitung)
* [2. Mitwirkende](#2-mitwirkende)
* [3. API-Referenz](#3-api-referenz)
    * [current_date.json](#current_datejson)
    * [characters.json](#charactersjson)
        * [aliases](#aliases)
        * [measurements](#measurements)
        * [classes](#classes)
        * [homes](#homes)
        * [relationships](#relationships)
        * [content](#content)
        * [sections](#sections)
    * [places.json](#placesjson)
        * [language](#language)
        * [leader](#leader)
    * [calendar.json](#calendarjson)
    * [news.json](#newsjson)
    * [actions.json](#actionsjson)
        * [cooldown](#cooldown)
        * [savereq](#savereq)
        * [damage](#damage)
        * [effects](#effects)
    * [compendia.json](#compendiajson)
    * [bestiarium.json](#bestiariumjson)
        * [movement](#movement)
        * [abilities](#abilities)
    * [theologarium.json](#theologariumjson)
    * [linguarium.json](#linguariumjson)
    * [gentarium.json](#gentariumjson)
    * [effects.json](#effectsjson)
    * [classarium.json](#classariumjson)
* [4. Ausführen eines lokalen Builds](#4-ausführen-eines-lokalen-builds)

<!-- TOC -->

## 1. Einleitung

Dieses Wiki dient als ergänzendes Tool für Sessions, indem Lore und Gameplay-Mechaniken schnell und einfach nachgeschaut
werden können.

Die Seite ist unter https://tome.zetsuboushii.site/ erreichbar.

<p align="center"><img src="/static/imgs/logo.png" height="100px" alt=""/></p>

## 2. Mitwirkende

| Mitwirkender                                                               | Profilbild                                                                                                                          |
|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| [Zetsu](https://github.com/Zetsuboushii)<br/>Dungeon Master, Web Master    | <a href="https://github.com/zetsuboushii"><img src="https://avatars.githubusercontent.com/u/65507051?v=4" width="150px;" alt=""/>   |
| [Knick](https://github.com/knick21)<br/>Unterstützung für Lore Consistency | <a href="https://github.com/knick21"><img src="https://avatars.githubusercontent.com/u/115408270?v=4" width="150px;" alt=""/>       |
| Bayda<br/>Illustratorin                                                    | <img src="https://cdn.discordapp.com/avatars/334334362696810496/12fa2a7cae7800da70efee6927ec234c?size=1024" width="150px;" alt=""/> |

## 3. Ausführen eines lokalen Builds

Der Source Code ist getestet unter Python 3.13.

Repository klonen:

```bash
git clone https://github.com/Zetsuboushii/Vastlands-Wiki
```

Dependencies installieren:

```bash
pip install -r requirements.txt
```

Flask-Applikation bauen und ausführen:

```bash
flask --app app.py --debug run
```