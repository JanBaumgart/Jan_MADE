# Project Plan

## Title
<!-- Give your project a short title. -->
Correlation between Covid-19 vaccination rate and school types and regions in Schlesig Holstein

## Main Question

<!-- Think about one main question you want to answer based on the data. -->
1. To what extent does the vaccination rate in Schleswig-Holstein correlate with COVID-19 case numbers in schools, categorized by school type and district, and are there significant differences in this correlation among various school types and regions?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->
Covid was and still is an important topic of Healthcare and our generation, we should get as much knowledge out of it as possible. I am going to analyse the relationship between the COVID-19 vaccination rate and the incidence of COVID-19 cases in various schools and different regions within Schleswig-Holstein. Schools will be seperated by different School Types and the Regions will be seperated in 4 clusters to see if they behave differently. The goal is to derive possible recommendations for future behavior in vaccination projects.

## Datasources

### Datasource1: COVID_19 Vacination Rates 
* Metadata URL: https://www.govdata.de/web/guest/suchen/-/details/covid-19-impfungen-in-deutschland0aef2

**Datasource1.1: by federal states**
* Data URL: https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/blob/main/Deutschland_Bundeslaender_COVID-19-Impfungen.csv
* Data Type: CSV

<!-- Description of the Data source -->

**Datasource1.2: by countys**
* Data URL: https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/blob/main/Deutschland_Landkreise_COVID-19-Impfungen.csv
* Data Type: CSV

<!-- Description of the Data source -->

### Datasource2: Number of COVID-19 cases at schools by school type
* Metadata URL: https://www.govdata.de/web/guest/suchen/-/details/anzahl-der-covid-19-falle-an-schulen-nach-schularten
* Data URL: https://opendata.schleswig-holstein.de/dataset/08263e93-6e2c-4034-888a-31ac33c91bfe/resource/eddd721d-1789-4d89-85a1-a43ac6e1fd7f/download/data.csv 
* Data Type: CSV

<!-- Description of the Data source -->

### Datasource3: Pupils in Schleswig Holstein by school type in total
* Data URL: https://www-genesis.destatis.de/genesis//online?operation=table&code=21111-0011&bypass=true&levelindex=0&levelid=1698693849295#abreadcrumb
* Data Type: CSV

<!-- Description of the Data source -->

### Datasource4: Population of germany by federal states and counties.
* Metadata URL: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.html
* Data URL: https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/04-kreise.xlsx?__blob=publicationFile
* Data Type: XLSX



## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Explore Datasources [#1][i1]
2. ...

[i1]: https://github.com/jvalue/made-template/issues/1