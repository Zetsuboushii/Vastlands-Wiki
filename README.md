<p align="center"><img src="/static/imgs/totv_logo.png" height="300px"  alt=""/></p>
<h1 align="center">Tome of the Vastlands</h1>
<p align="center"><strong><code>Vastlands-Wiki</code></strong></p>
<p align="center">Ein umfassendes Wiki und Wissensdatenbank für meine D&D-Kampagnen</p>
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
<!-- TOC -->

## 1. Einleitung

Dieses Wiki dient als ergänzendes Tool für Sessions, indem Lore und Gameplay-Mechaniken schnell und einfach nachgeschaut
werden können.

Die Seite ist unter https://tome.zetsuboushii.site/ erreichbar.

<p align="center"><img src="/static/imgs/logo.png" height="100px" alt=""/></p>

## 2. Mitwirkende

| Mitwirkende                                         | GitHub                                                                                                                            |
|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Luke Grasser (Zetsu)<br/>Dungeon Master, Web Master | <a href="https://github.com/zetsuboushii"><img src="https://avatars.githubusercontent.com/u/65507051?v=4" width="150px;" alt=""/> |

## 3. API-Referenz

Alle JSON-Files können unter dem Base-Path https://tome.zetsuboushii.site/static/json/ verfügbar.

### current_date.json

`current_date.json` ist ein Objekt mit folgenden Feldern:

| Feldname              | Datentyp | Erklärung               |
|-----------------------|----------|-------------------------|
| `current_ingame_date` | `string` | Aktuelles In-game Datum |

### characters.json

`characters.json` ist ein Array von Charakter-Objekten. Ein Charakter besteht aus folgenden Feldern:

| Feldname        | Datentyp | Erklärung                                                                                                                |
|-----------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| `name`          | `string` | Vorname des Charakters                                                                                                   |
| `surname`       | `string` | Nachname des Charakters                                                                                                  |
| `title`         | `string` | Titel des Charakters                                                                                                     |
| `race`          | `string` | Rasse des Charakters;<br>Verweis auf Objekte in `gentarium.json`                                                         |
| `sex`           | `string` | Geschlecht des Charakters;<br>`"m"` für "männlich", `"w"` für "weiblich"                                                 |
| `birthday`      | `string` | Geburtstag des Charakters;<br>Format: `"dd.mm.yyy"`;<br>Negatives Jahr = "v.V.", Positives Jahr = "n.V."                 |
| `aliases`       | `array`  | Aliase für den Charakter von anderen Charakteren;<br>Dokumentation [hier](#aliases)                                      |
| `measurements`  | `object` | Körpermaße des Charakters;<br>Dokumentation [hier](#measurements)                                                        |
| `functions`     | `array`  | Funktionen / Berufungen des Charakters;<br>Einzelne Funktionen sind als `string` definiert                               |
| `classes`       | `object` | Klassen des Charakters;<br>Dokumentation [hier](#classes)                                                                |
| `nationality`   | `string` | Nationalität des Charakters;<br>Verweis auf Objekte in [`places.json`](#placesjson)                                      |
| `homes`         | `array`  | Heimatorte / Besondere Orte des Charakters;<br>Dokumentation [hier](#homes)                                              |
| `alignment`     | `string` | Gesinnung des Charakters                                                                                                 |
| `affiliations`  | `array`  | Zugehörigkeiten des Charakters zu einer Organisation / Religion;<br>Einzelne Zugehörigkeiten sind als `string` definiert |
| `likes`         | `array`  | Dinge, die der Charakter mag;<br>Einzelne Dinge sind als `string` definiert                                              |
| `dislikes`      | `array`  | Dinge, die der Charakter nicht mag;<br>Einzelne Dinge sind als `string` definiert                                        |
| `status`        | `string` | Status des Charakters, ob dieser lebt usw.                                                                               |
| `relationships` | `array`  | Beziehungen des Charakters zu anderen Charakteren;<br>Dokumentation [hier](#relationships)                               |
| `alt_images`    | `array`  | Liste der Namenssuffixe für alternative Bilder des Charakters;<br>Einzelne Suffixe sind als `string` definiert           |
| `content`       | `object` | Liste der Texte des Charakterprofils;<br>Dokumentation [hier](#content)                                                  |

#### aliases

`aliases` ist ein Array von Alias-Objekten. Ein Alias besteht aus folgenden Feldern:

| Feldname | Datentyp | Erklärung               |
|----------|----------|-------------------------|
| `alias`  | `string` | Alias für den Charakter |
| `origin` | `string` | Ursprung des Alias      |

#### measurements

`measurements` ist ein Objekt mit folgenden Feldern:

| Feldname         | Datentyp | Erklärung                                          |
|------------------|----------|----------------------------------------------------|
| `height`         | `number` | Körpergröße des Charakters in Metern               |
| `weight`         | `number` | Gewicht des Charakters in Kilogramm                |
| `bust`           | `number` | Oberer Brustumfang des Charakters in Zentimetern   |
| `underbust`      | `number` | Unterer Brustumfang des Charakters in Zentimetern  |
| `waist`          | `number` | Taillenumfang des Charakters in Zentimetern        |
| `hip`            | `number` | Hüftumfang des Charakters in Zentimetern           |
| `shoulder_width` | `number` | Breite der Schultern des Charakters in Zentimetern |
| `muscle_mass`    | `number` | Muskelmasse des Charakters in Kilogramm            |

#### classes

`classes` ist ein Objekt mit folgenden Feldern:

| Feldname      | Datentyp | Erklärung                                                                     |
|---------------|----------|-------------------------------------------------------------------------------|
| `baseclass`   | `string` | Basisklasse des Charakters                                                    |
| `subclasses`  | `array`  | Subklassen des Charakters;<br>Einzelne Subklassen sind als `string` definiert |
| `masterclass` | `string` | Meisterklasse des Charakters                                                  |

#### homes

`homes` ist ein Array von Heimat-Objekten. Eine Heimat besteht aus folgenden Feldern:

| Feldname     | Datentyp | Erklärung                                                              |
|--------------|----------|------------------------------------------------------------------------|
| `place`      | `string` | Name des Ortes;<br>Verweis auf Objekte in [`places.json`](#placesjson) |
| `attachment` | `string` | Art der Verbindung, die der Charakter zu dem jeweiligen Ort hat        |

#### relationships

`relationships` ist ein Array von Beziehungs-Objekten. Eine Beziehung besteht aus folgenden Feldern:

| Feldname    | Datentyp | Erklärung                                                                                   |
|-------------|----------|---------------------------------------------------------------------------------------------|
| `character` | `string` | Name des anderen Charakters;<br>Verweis auf Objekte in [`characters.json`](#charactersjson) |
| `relation`  | `string` | Art der Beziehung, die der Charakter zu dem jeweiligen Charakter hat                        |

#### content

`content` ist ein Objekt mit folgenden Feldern:

| Feldname   | Datentyp | Erklärung                                                                            |
|------------|----------|--------------------------------------------------------------------------------------|
| `excerpt`  | `string` | Kurzzusammenfassung des Charakterprofils                                             |
| `sections` | `array`  | Liste der einzelnen Kapitel des Charakterprofils;<br>Dokumentation [hier](#sections) |

#### sections

`sections` ist ein Array von Kapitel-Objekten. Ein Kapitel besteht aus folgenden Feldern:

| Feldname | Datentyp | Erklärung                |
|----------|----------|--------------------------|
| `title`  | `string` | Überschrift des Kapitels |
| `text`   | `string` | Prosa des Kapitels       |

### places.json

`places.json` ist ein Array von Orts-Objekten. Ein Ort besteht aus folgenden Feldern:

| Feldname     | Datentyp | Erklärung                                                                                  |
|--------------|----------|--------------------------------------------------------------------------------------------|
| `name`       | `string` | Name des Ortes                                                                             |
| `supplement` | `string` | Beinamen des Ortes                                                                         |
| `title`      | `string` | Titel des Ortes                                                                            |
| `language`   | `object` | Diverse Sprachen-bezogene Informationen;<br>Dokumentation [hier](#language)                |
| `demography` | `number` | Einwohnerzahl des Ortes                                                                    |
| `placetype`  | `string` | Art des Ortes                                                                              |
| `system`     | `string` | Regierungsform des Ortes                                                                   |
| `leader`     | `object` | Regierende Person des Ortes;<br>Dokumentation [hier](#leader)                              |
| `content`    | `object` | Liste der Texte des Ortes;<br>Analoge Dokumentation [hier](#content)                       |
| `contains`   | `array`  | Liste von im Ort befindlichen Orte;<br>Rekursiver Verweis auf [`places.json`](#placesjson) |

#### language

`language` ist ein Objekt mit folgenden Feldern:

| Feldname      | Datentyp | Erklärung                                                                              |
|---------------|----------|----------------------------------------------------------------------------------------|
| `natlang`     | `string` | Name der Landessprache;<br>Verweis auf Objekte in [`linguarium.json`](#linguariumjson) |
| `natname`     | `string` | Name des Ortes in Landessprache                                                        |
| `translation` | `string` | Übersetzung von `natname` in Gemeinsprache                                             |

#### leader

`leader` ist ein Objekt mit folgenden Feldern:

| Feldname | Datentyp | Erklärung                                                                            |
|----------|----------|--------------------------------------------------------------------------------------|
| `name`   | `string` | Name der regierenden;<br>Verweis auf Objekte in [`characters.json`](#charactersjson) |
| `type`   | `string` | Titel der Regentschaft                                                               |

### calendar.json

`calendar.json` ist ein Array von Feiertags-Objekten. Ein Feiertag besteht aus folgenden Feldern:

| Feldname  | Datentyp | Erklärung                                                               |
|-----------|----------|-------------------------------------------------------------------------|
| `name`    | `string` | Name des Feiertags                                                      |
| `date`    | `string` | Datum des Feiertags;<br>Format: `"dd.mm"`                               |
| `type`    | `string` | Art des Feiertags                                                       |
| `content` | `object` | Liste der Texte zum Feiertag;<br>Analoge Dokumentation [hier](#content) |

### news.json

`news.json` ist ein Array von News-Objekten. Eine News besteht aus folgenden Feldern:

| Feldname  | Datentyp | Erklärung                     |
|-----------|----------|-------------------------------|
| `session` | `number` | Nummer der jeweiligen Session |
| `text`    | `string` | Textueller Inhalt der News    |

### actions.json

`actions.json` ist ein Array von Action-Objekten. Eine Action besteht aus folgenden Feldern:

| Feldname    | Datentyp  | Erklärung                                                                          |
|-------------|-----------|------------------------------------------------------------------------------------|
| `name`      | `string`  | Name der Action                                                                    |
| `legendary` | `boolean` | Flag, ob Action legendär ist                                                       |
| `cooldown`  | `object`  | Abklingzeit der Action;<br>Dokumentation [hier](#cooldown)                         |
| `range`     | `number`  | Reichweite der Action in Fuß                                                       |
| `aoe`       | `string`  | Area of Effect der Action in Bezug auf die Reichweite                              |
| `hitbonus`  | `number`  | Höhe des Bonus auf den Trefferwurf der Action                                      |
| `savereq`   | `object`  | Bedingung für Rettungswurf des Ziels der Action;<br>Dokumentation [hier](#savereq) |
| `damage`    | `object`  | Schaden der Action;<br>Dokumentation [hier](#damage)                               |
| `effects`   | `array`   | Liste der Effekte der Action;<br>Dokumentation [hier](#effects)                    |

#### cooldown

`cooldown` ist ein Objekt mit folgenden Feldern:

| Feldname        | Datentyp | Erklärung                                    |
|-----------------|----------|----------------------------------------------|
| `duration`      | `number` | Dauer der Abklingzeit                        |
| `duration_type` | `string` | Art der Dauer;<br>"r" für Runde, "d" für Tag |

#### savereq

`savereq` ist ein Objekt mit folgenden Feldern:

| Feldname  | Datentyp | Erklärung                             |
|-----------|----------|---------------------------------------|
| `ability` | `string` | Benötigte Fähigkeit für Rettungswurf  |
| `bound`   | `number` | Zu erreichender Wert des Rettungswurf |

#### damage

`damage` ist ein Objekt mit folgenden Feldern:

| Feldname    | Datentyp | Erklärung                   |
|-------------|----------|-----------------------------|
| `dice_term` | `string` | Würfelwurf-Term für Schaden |
| `type`      | `string` | Schadenstyp                 |

#### effects

`effects` ist ein Array von Effekt-Objekten. Ein Effekt besteht aus folgenden Feldern:

| Feldname        | Datentyp | Erklärung                                                            |
|-----------------|----------|----------------------------------------------------------------------|
| `type`          | `string` | Effekt-Typ;<br>Verweis auf Objekte in [`effects.json`](#effectsjson) |
| `dice_term`     | `string` | Würfelwurf-Term für Effekt                                           |
| `severity`      | `number` | Schwere des Effekts                                                  |
| `duration`      | `number` | Dauer des Effekts                                                    |
| `duration_type` | `string` | Art der Dauer;<br>"r" für Runde, "d" für Tag                         |

### compendia.json

`compendia.json` ist ein Array von Kompendium-Objekten. Ein Kompendium besteht aus folgenden Feldern:

| Feldname | Datentyp | Erklärung                   |
|----------|----------|-----------------------------|
| `name`   | `number` | Name des Kompendium         |
| `text`   | `string` | Beschreibung des Kompendium |

### bestiarium.json

`bestiarium.json` ist ein Array von Gegner-Objekten. Ein Gegner besteht aus folgenden Feldern:

| Feldname      | Datentyp | Erklärung                                                                                                                        |
|---------------|----------|----------------------------------------------------------------------------------------------------------------------------------|
| `name`        | `string` | Name des Gegners                                                                                                                 |
| `boss_title`  | `string` | Titel des Bossgegners                                                                                                            |
| `type`        | `string` | Art des Gegners                                                                                                                  |
| `hp`          | `number` | Anzahl der Trefferpunkte des Gegners                                                                                             |
| `ac`          | `number` | Höhe der Rüstungsklasse des Gegners                                                                                              |
| `movement`    | `array`  | Bewegungsmöglichkeiten des Gegners;<br>Dokumentation [hier](#movement)                                                           |
| `abilities`   | `object` | Fähigkeiten des Gegners;<br>Dokumentation [hier](#abilities)                                                                     |
| `weaknesses`  | `array`  | Schwächen des Gegners;<br>Einzelne Schwächen sind als `string` definiert                                                         |
| `resistances` | `array`  | Resistenzen des Gegners;<br>Einzelne Resistenzen sind als `string` definiert                                                     |
| `immunities`  | `array`  | Immunitäten des Gegners;<br>Einzelne Immunitäten sind als `string` definiert                                                     |
| `actions`     | `array`  | Aktionen des Gegners;<br>Einzelne Aktionen sind als `string` definiert;<br>Verweis auf Objekte in [`actions.json`](#actionsjson) |

#### movement

`movement` ist ein Objekt mit folgenden Feldern:

| Feldname | Datentyp | Erklärung                                 |
|----------|----------|-------------------------------------------|
| `type`   | `string` | Art der Bewegung                          |
| `range`  | `string` | Maximale Reichweite durch Bewegung in Fuß |

#### abilities

`abilities` ist ein Objekt mit folgenden Feldern:

| Feldname | Datentyp | Erklärung                                |
|----------|----------|------------------------------------------|
| `str`    | `string` | Stärkemodifikator des Gegners            |
| `dex`    | `string` | Geschicklichkeitsmodifikator des Gegners |
| `con`    | `string` | Konstitutionsmodifikator des Gegners     |
| `int`    | `string` | Intelligenzmodifikator des Gegners       |
| `wis`    | `string` | Weisheitsmodifikator des Gegners         |
| `cha`    | `string` | Charismamodifikator des Gegners          |

### theologarium.json

`theologarium.json` ist ein Array von Religions-Objekten. Eine Religion besteht aus folgenden Feldern:

| Feldname         | Datentyp | Erklärung                                                                                            |
|------------------|----------|------------------------------------------------------------------------------------------------------|
| `name`           | `string` | Name der Religion                                                                                    |
| `central_figure` | `string` | Zentrale Figur / Person der Religion;<br>Verweis auf Objekte in [`characters.json`](#charactersjson) |
| `type`           | `string` | Art der Religion                                                                                     |
| `content`        | `object` | Liste der Texte zur Religion;<br>Analoge Dokumentation [hier](#content)                              |

### linguarium.json

`linguarium.json` ist ein Array von Sprache-Objekten. Eine Sprache besteht aus folgenden Feldern:

| Feldname  | Datentyp | Erklärung                                                                   |
|-----------|----------|-----------------------------------------------------------------------------|
| `name`    | `string` | Name der Sprache                                                            |
| `type`    | `string` | Art der Religion                                                            |
| `center`  | `string` | Zentrum der Sprache;<br>Verweis auf Objekte in [`places.json`](#placesjson) |
| `content` | `object` | Liste der Texte zur Sprache;<br>Analoge Dokumentation [hier](#content)      |

### gentarium.json

`gentarium.json` ist ein Array von Rasse-Objekten. Eine Rasse besteht aus folgenden Feldern:

| Feldname      | Datentyp | Erklärung                                                                                                                                                                           |
|---------------|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`        | `string` | Name der Rasse                                                                                                                                                                      |
| `age_average` | `number` | Durchschnittliche Lebenserwartung für Individuen der Rasse                                                                                                                          |
| `domains`     | `array`  | Liste der Orte, an denen Individuen der Rasse hauptsächlich vertreten sind;<br>Einzelne Domains sind als `string` definiert;<br>Verweis auf Objekte in [`places.json`](#placesjson) |
| `content`     | `object` | Liste der Texte zur Rasse;<br>Analoge Dokumentation [hier](#content)                                                                                                                |