# honeycomb.svg

This code was mostely generated with Claude 3.7 and this prompt:

```text
Create a Python program which generates an SVG file with a honeycomb field where each shifted row fits exactly between the other rows; make the program flexible and use following parameters:
columns=10 # columns per row
rows=8 # contains odd and even rows
length=50 # in mm - the length for all six honeycomb sides (each side has the same length)
angle=120 # in degrees - the angle between the top and bottom tips of the honeycomb
distance=2 # in mm - the distance between each comb in a row and the distance to the honeycombs in the next shifted row

honeycomb structure with a top and bottom tip:
/\
| |
\/

Based on these parameters the program calculates for each honeycomb the position, therefore, it’s important that the distance to the next honeycomb is the same and there is no overlapping. Write the program in a way that it will test  this constraint and adjust it self (log each adjustment).
```

See commit messages for the previous try to generate code.