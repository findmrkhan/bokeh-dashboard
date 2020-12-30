# Creating a World-map dashboard of immunization data using Bokeh
In this post I will demonstrate how to create an interactive dashboard showing country-wise immunization data on a World-map in Python's Bokeh library. This countrywise map is also known as a Chloropleth diagram.

[Dashboard](Bokeh-Chloropleth-Dashboard.png)


## The dataset
I will use the immunization data set from Unicef which shows the immunization percentages for all years from 1980 till 2019 for all major countries.
 [Source Unicef](https://data.unicef.org/topic/child-health/immunization/)

## Features of the dashboard
The map shows all the countries' political border. The colors shows the percentage of immunization for each country. The tooltip shows the vaccine names, country and the percentage of immunization. The slider on the right can select the year. On changing the slider the map updates instantly showing the data foe the chosen year. The choiceboxes on the left can select the drugs the user is interested in. Again, on choosing the choiceboxes the map gets updated instantly.


## The code explained
Let us first see the file structure of the project.



## Conclusion

