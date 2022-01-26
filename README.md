# Tetris-Game-Python
This is an object-oriented implementation of Tetris in Python. No images assets are used for this project; everything is being drawn using a Tkinter wrapper library.

Using the Tkinter wrapper in `graphics.py` I define a class `Block` which is used as a building block for each of the Tetris shapes. Each tetris shape gets its own class which is inheretid from the `Shape` class to draw our shape. The `Shape` class contains the relative position of the blocks for each particular shape, along with the shape position on the board. Additionally each shape has a color assigned to it randomly at the time of instantiation. You get the idea!

<p align=center>
<img width="414" alt="Tetris" src="https://user-images.githubusercontent.com/65843134/151255374-48910cff-cc3f-424a-8a5f-e6c51af84c91.png">
<img width="414" alt="Tetris 2" src="https://user-images.githubusercontent.com/65843134/151255373-0da9e8ac-367c-470c-9797-1586bab2f03a.png">
</p>
