<p align="center"><br><br><img src="/static/imgs/logo.png" height="260"  alt=""/></p>

<h1 align="center">Tome of the Vastlands</h1>
<p align="center"><strong><code>Vastlands-Wiki</code></strong></p>
<p align="center">Ein umfassendes Wiki für meine D&D-Kampagnen</p>
<br>
<p align="center">
  <img src="https://img.shields.io/maintenance/yes/2025"  alt=""/>
</p>

<h2>Table of Contents</h3>
<!-- TOC -->

* [1. Einleitung](#1-einleitung)
* [2. Mitwirkende](#2-mitwirkende)
* [3. API-Referenz](#3-api-referenz)
    * [characters.json](#charactersjson)
        * [`aliases`](#aliases)

<!-- TOC -->

## 1. Einleitung

Dieses Wiki dient als ergänzendes Tool für Sessions, indem Lore und Gameplay-Mechaniken schnell und einfach nachgeschaut
werden können.

Die Seite ist unter https://v3.tome.zetsuboushii.site/ erreichbar.

## 2. Mitwirkende

| Mitwirkende                                         | GitHub                                                                                                                            |
|-----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Luke Grasser (Zetsu)<br/>Dungeon Master, Web Master | <a href="https://github.com/zetsuboushii"><img src="https://avatars.githubusercontent.com/u/65507051?v=4" width="150px;" alt=""/> |

## 3. API-Referenz

Alle JSON-Files können unter dem Base-Path https://v3.tome.zetsuboushii.site/static/json/ verfügbar.

### `characters.json`

`characters.json` ist ein Array von Charakter-Objekten. Ein Charakter besteht aus folgenden Feldern:

| Feldname       | Datentyp | Erklärung                                                                                                |
|----------------|----------|----------------------------------------------------------------------------------------------------------|
| `name`         | `string` | Vorname des Charakters                                                                                   |
| `surname`      | `string` | Nachname des Charakters                                                                                  |
| `title`        | `string` | Titel des Charakters                                                                                     |
| `race`         | `string` | Rasse des Charakters;<br>Verweis auf Objete in `gentarium.json`                                          |
| `sex`          | `string` | Geschlecht des Charakters;<br>`"m"` für "männlich", `"w"` für "weiblich"                                 |
| `birthday`     | `string` | Geburtstag des Charakters;<br>Format: `"dd.mm.yyy"`;<br>Negatives Jahr = "v.V.", Positives Jahr = "n.V." |
| `aliases`      | `array`  | Aliase für den Charakter von anderen Charakteren; Dokumentation [hier](#aliases)                         |
| `measurements` | `object` | Körpermaße des Charakters; Dokumentation [hier](#measurements)                                           |
| `functions`    | `array`  | Funktionen/Berufungen des Charakters; Einzelne Funktionen sind als `string` definiert                    |
| `classes`      | `object` | Klassen des Charakters; Dokumentation [hier](#classes)                                                   |

#### `aliases`

`aliases` ist ein Array von Alias-Objekten. Ein Alias besteht aus folgenden Feldern:

| Feldname | Datentyp | Erklärung               |
|----------|----------|-------------------------|
| `alias`  | `string` | Alias für den Charakter |
| `origin` | `string` | Ursprung des Alias      |

#### `measurements`

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

#### `classes`

`classes` ist ein Objekt mit folgenden Feldern:

| Feldname     | Datentyp | Erklärung                                                                  |
|--------------|----------|----------------------------------------------------------------------------|
| `baseclass`  | `string` | Basisklasse des Charakters                                                 |
| `subclasses` | `array`  | Subklassen des Charakters; Einzelne Subklassen sind als `string` definiert |
