from PygamePaint import PygamePaint

if __name__ == "__main__":
    app = PygamePaint()
    app.start()
"""
TODO:
- A lot actually lol
- I have to add a lot of stuff to the menu bar
(
    !especially!
    |DONE|Top Menu Buttons('File', 'Edit', 'View', etc.),
    Buttons Under Top Menu Buttons('File/Open...', etc.),
    Events and handler for events
) --this is prob the hardest lol
- Add code to Tools
    --Brush = incomplete
    --Bucket = incomplete
- Add methods to ToolBar that refresh options for tools, process events, get active tool, set active tool, etc.
- Also I want to add a palette thing on the tool bar with updates constintly and has a slider under to 
-     change the color. A few buttons to quickly change to main colors would also be pretty nice.
- Add a bunch a shite to theme.json and make theme_light.json and theme_dark.json
- Add code to class EditableCanvas and its methods (same for MenuBarEvents)
- Continue digging into pygame_gui's source code
"""