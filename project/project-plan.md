# Project Plan

## Title
Correlation between Covid-19 vaccination rate and school types / regions in Schlesig Holstein

## Main Question

1. To what extent does the vaccination rate in Schleswig-Holstein correlate with COVID-19 case numbers in schools, categorized by school type.
2. Are there significant differences in this correlation among various school types and regions?

## Description

Covid was and still is an important topic of Healthcare and our generation, we should get as much knowledge out of it as possible. I am going to analyse the relationship between the COVID-19 vaccination rate and the incidence of COVID-19 cases in various schools and different regions within Schleswig-Holstein. Schools will be separated by different School Types and the Regions will be separated in 4 clusters to see if they behave differently. The goal is to derive possible recommendations for future behavior in vaccination projects.

## Datasources

### Datasource1: COVID_19 Vacination Rates 
* Metadata URL: https://www.govdata.de/web/guest/suchen/-/details/covid-19-impfungen-in-deutschland0aef2
* License: Public Domain Mark 1.0 (PDM) (https://creativecommons.org/publicdomain/mark/1.0/)

**Datasource1.1: by federal states**
* Data URL: https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/blob/main/Deutschland_Bundeslaender_COVID-19-Impfungen.csv
* Data Type: CSV
 
A collection of data showing the vaccination rates broken down by German federal states


**Datasource1.2: by counties**
* Data URL: https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/blob/main/Deutschland_Landkreise_COVID-19-Impfungen.csv
* Data Type: CSV

A collection of data showing the vaccination rates broken down by counties (in SH)


### Datasource2: Number of COVID-19 cases at schools by school type
* Metadata URL: https://www.govdata.de/web/guest/suchen/-/details/anzahl-der-covid-19-falle-an-schulen-nach-schularten
* Data URL: https://opendata.schleswig-holstein.de/dataset/08263e93-6e2c-4034-888a-31ac33c91bfe/resource/eddd721d-1789-4d89-85a1-a43ac6e1fd7f/download/data.csv 
* Data Type: CSV
* License: Public Domain Mark 1.0 (PDM) (https://creativecommons.org/publicdomain/mark/1.0/)

The data source provides data on COVID-19 cases at schools, separated by type of school in Germany


### Datasource3: Pupils in Germany by Schooltype in 2021/2022
* Metadata URL: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bildung-Forschung-Kultur/Schulen/_inhalt.html#_ccbho9pou
* Data URL: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bildung-Forschung-Kultur/Schulen/Publikationen/Downloads-Schulen/statistischer-bericht-allgemeinbildende-schulen-2110100227005.xlsx?__blob=publicationFile
* Data Type: XLSX
* License: Data licence Germany – attribution – version 2.0 (https://www.destatis.de/EN/Service/Legal-Notice/CopyrightGENESISOnlineDatabase.html)

The data from the Federal Statistical Office shows the number of pupils, broken down by federal state, school year, gender, school type and year group


### Datasource4: Population of germany by federal states and counties.
* Metadata URL: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html
* Data URL: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.xlsx?__blob=publicationFile
* Data Type: XLSX
* License: Data licence Germany – attribution – version 2.0 (https://www.destatis.de/EN/Service/Legal-Notice/CopyrightGENESISOnlineDatabase.html)

This data (also from the Federal Statistical Office) provides an overview of all independent cities and districts by area, population and population density

### Datasource5: Number of COVID-19 cases at schools by counties
* Metadata URL: https://www.govdata.de/web/guest/suchen/-/details/anzahl-der-covid-19-falle-an-schulen-nach-kreisen
* Data URL. https://opendata.schleswig-holstein.de/dataset/acd37a65-b4ad-4abd-b318-a39fc37838f7/resource/5c7d0685-5ec2-441c-ab9e-dc5a691bef29/download/data.csv
* Data Type: CSV
* License: Public Domain Mark 1.0 (PDM) (https://creativecommons.org/publicdomain/mark/1.0/)


## Work Packages

1. Explore Datasources [#1][i1]
2. Build and improve Pipeline [#2][i2]
3. Implement automated tests [#3][i3]
4. Improve the Structure of Data in the Repository [#4][i4]
5. Adding another source for the complete analysis [#5][i5]

[i1]: https://github.com/JanBaumgart/Jan_MADE/issues/1
[i2]: https://github.com/JanBaumgart/Jan_MADE/issues/2
[i3]: https://github.com/JanBaumgart/Jan_MADE/issues/3
[i4]: https://github.com/JanBaumgart/Jan_MADE/issues/4
[i5]: https://github.com/JanBaumgart/Jan_MADE/issues/5
