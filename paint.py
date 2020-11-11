from PygamePaint import PygamePaint

if __name__ == "__main__":
    app = PygamePaint()
    app.start()
"""
                        ~~TODO~~
- A lot actually lol

- I have to add a lot of stuff to the menu bar
(
    !especially!
    |DONE|Top Menu Buttons('File', 'Edit', 'View', etc.),
    Buttons Under Top Menu Buttons('File/Open...', etc.),
    Events and handler for events
) --this is prob the hardest lol

- Add code to Tools
    --Brush = probably complete
    --Bucket = incomplete (~1%)

- Add methods to ToolBar that 
-    (|DONE|refresh options for tools), 
-    (process events[~82%]), 
-    (|DONE|get active tool, set active tool),
-    a method called every update cycle, etc.

-|DONE| Also I want to add a palette thing on the tool bar
-   (|Not Gonna Happen| and has a slider under to change the color).
-   (|Prob won't happen either|A  buttons to quickly change to main colors would also be pretty nice.)

- Add a bunch a shite to theme.json and make theme_light.json and theme_dark.json

- Add code to class EditableCanvas and its methods[~100%] (same for MenuBarEvents)

- |DONE|Make CanvasWindow Scrollable (did it early cause its prob the easiest lol)

- on_event() method in class PygamePaint

- Continue digging into pygame_gui's source code (I'M DYINGGG)
"""