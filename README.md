# Pygame-World-Generation
Simple world generation and visualization using Pygame and noise

take a look at the game.py file 

How a seed works:
the first 4 values are for x
the last 4 values are for y

the calc_new_map() function takes these x and y values and uses them to generate a grayscale map
this map then gets converted into an map containing 4 different value types:
water, sand, land, mountain

the game then renders the map using both the tilesize and colors for each tile types and renders them to a surface

![alt_text](https://github.com/N0t3nl1sh/Pygame-World-Generation/blob/main/img.png)

you can also use the white box to generate new maps with different seeds.
