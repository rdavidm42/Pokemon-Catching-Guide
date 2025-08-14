# Pokemon Catching Guide

A tracker/catching guide to assist in completing the Pokedex in each generation of mainline Pokemon games. Since every generation of Pokemon games require trading between multiple games to complete the Pokedex, I created this tracker as a way to help plan and carry out the completion of the Pokedex in each generation.
In each dataframe, the Pokemon's name, number, whether it has been caught, and location it can be caught in is included.

An important note: The caught column is reset every time the generation is changed. If you want to save this data and switch the viewer to a different generation, please save the pokedex and reload it when you want to return to that particular generation.

## Search Options
Below is an outline of the search options available.

### Generation
Switch back and forth between the different generations. This reloads the entire dataset.

### Get Pokemon in (Blank) Game(s) but not (Blank) Game(s)
This option lets you pick which Pokemon appear based on which games they appear in. If "All of" is selected, only Pokemon that appear in all of the games listed will be returned in the search. If "At least one of" is selected, Pokemon that appear in any one of the games chosen will appear.

For example, Lunatone will appear if one picks Ruby and Sapphire, and selects "At least one of," since it appears in Sapphire, but will not appear if "All of" is selected, since it does not appear in Ruby.

In the second option, any Pokemon that appear in the games you choose will *not* appear.

For example, if Ruby and Sapphire are selected in the first textbox, and Emerald is selected in the second textbox, then Roselia will appear, since it appears in Ruby and Sapphire, but not Emerald.
### Keywords
This ensures only Pokemon whose description includes the included keywords appear. For example, if "Route 1" is in the textbox, only Pokemon found in Route 1 will appear in the search.
### Searching Within Dataframe
If you want to search within a returned dataframe (e.g. for a specific Pokemon), you can use the built in searchbar feature. Click on the magnifying glass in the upper righthand corner of the dataframe, and type the terms you wish to search for.
## Saving and Reloading
To save the dataframe, either click on the "Download Pokedex" button or download the data by clicking on the download button in the upper righthand corner of the dataframe. This will download the current data as a .csv file, which can be opened in Excel or another spreadsheet program.

To reload a previous datasheet, use the "Upload" file button to select a previously downloaded file. Note that the generation selected needs to match the file prior to upload, otherwise the file will not load.
