# BA_AVIOS_DATA

To store code and information related to my British Airways Avios Point Dataset and Dashboard.

## Project Background  

This project started as a passion project upon leaving employment at IAG Cargo. It is well known that the British Airways points-based flight finder search tool is notoriously difficult to use.  

After discovering a small manually captured dataset from [Rob Burgess on Head for Points](https://www.headforpoints.com/2024/08/29/how-many-avios-do-i-need-to-fly-to-2/), I realized the search tool could be improved—even if the data had the potential to become outdated.  

## Data Extraction & Transformation  

My first step was extracting the data from the website's table. Instead of copying and pasting the data into a transformation program, I wanted to use a replicable and repeatable process in case Rob updated the source. Several transformations were required to convert the data into a format suitable for Tableau.  

Additional data was incorporated using a Large Language Model (LLM), specifically ChatGPT. This was used to determine whether a location was a city or a country. If the location was a city, I requested the corresponding airport code. If the location was a country, I asked for the most relevant airport code.  

## Dashboard Design & Visualization  

I used **Figma** and **Excalidraw** to design the dashboard before loading the transformed data into **Tableau** for visualization.
