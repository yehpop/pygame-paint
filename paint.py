from PygamePaint import PygamePaint

if __name__ == "__main__":
    app = PygamePaint()
    app.start()
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TODO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- A lot actually lol

- Improve the Undo/Redo so you don't have to refocus the canvas everytime [~0%] 

- Completely remove the bucket and add like a straight line tool, etc. instead or start coding the bucket

- I have to add a lot of stuff to the menu bar
(
    !especially!
    |DONE|Top Menu Buttons('File', 'Edit', 'View', etc.),
    |~DONE|Buttons Under Top Menu Buttons('File/Open...', etc.),
    |~DONE|Events and handler for events
) --this is prob the hardest lol

- Add code to Tools
    --Brush = probably complete
    
    --Bucket = incomplete (~1%) # oh god how am I gonna make this
    --maybe I could like calculate the distance between the same colors or sth but, 
    --I don't know if that would be nice or if I could programm that lol

- Add methods to ToolBar that 
-    (|DONE|refresh options for tools), 
-    (process events[~DONE]), 
-    (|DONE|get active tool, set active tool),
-    (|DONE|a method called every update cycle), etc.

-|DONE| Also I want to add a palette thing on the tool bar
-   (|Not Gonna Happen| and has a slider under to change the color).
-   (|Prob won't happen either|A  buttons to quickly change to main colors would also be pretty nice.)

- Add a bunch a shite to theme.json and |DONE!|<-make theme_light.json and theme_dark.json [~DONE]

- Add code to class EditableCanvas and its methods|DONE|
- Same for MenuBarEvents[~DONE]

- |DONE|Make CanvasWindow Scrollable (did it early cause its prob the easiest lol)

- on_event() method in class PygamePaint[~DONE]

- Continue digging into pygame_gui's source code (I'M DYINGGG)

#######################################################################################################
"""