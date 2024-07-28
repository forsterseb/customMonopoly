# Custom Latex monopoly
Build a custom monopoly game with these latex files.

This repository contains latex files for 
- map tiles (streets, )
- cards (streets, utility, railstations, community/chance)

## Building
To build the latex files you need the original monopoly font: Kabel Bold and Regular  
and use xelatex

After building a pdf file, you may extract a png file using `python crop_pdf.py input.pdf output.<pdf/png>`, which crops the pdf to its contents and saves the result.

Using the cropped result from `map.tex` the monopoly board can be generated with `python img_to_map.py tiles.png output.png` (and further customized with background color and image).

## Structure
├── `cardCommands.tex`: contains the basic commands for the creation of cards  
│&emsp;&emsp;├── `cards.tex`: contains the cards the players get  
│&emsp;&emsp;└── `chance.tex`: contains the chance front cards  
│&emsp;&emsp;└── `chance_back.tex`: contains the chance back card  
│&emsp;&emsp;└── `community.tex`: contains the community front cards  
│&emsp;&emsp;└── `community_back.tex`: contains the community back card  
├── `mapTiles.tex`: contains the basic commands for the creation of map tiles  
│&emsp;&emsp;├── `map.tex`: contains the actual creation of map tiles  


## Example F1 Theme
![](cards1.png)

## Example F1 Board
![](board.png)