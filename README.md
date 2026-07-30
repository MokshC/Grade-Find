# Grade Grab
Create a list of and batch search [BlackMagic's DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve/) Projects for matching grades

## Installing Script
### Steps
1. In Resolve open the Fusion page, in the toolbar click “Fusion > Fusion Settings”
2. Click “Path Map” in the Fusion drop down of the settings window, and make sure “Scripts” is set to “UserPaths:Scripts”. If not, hit the “Reset” button.
3. Click "Script" in the Fusion drop down of the settings window, change selection from python 2.7 to python 3
   - This step is only Resolve version 18.1.4 or later
4. Hit the save button to update all of your changes
5. [Download this repository's latest release](https://github.com/MokshC/GradeGrab/releases)
6. Add it to your scripts path. These paths can also be found by clicking the folder icon at the bottom right of "Path Map" from step 2.
   - **LINUX**: `~/.local/share/DaVinciResolve/Fusion/Scripts/Color`
     - Hint: if you can’t find .local try hitting Ctrl+H to show hidden folders
   - **WINDOWS**: `C:\Users\{NAME}\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Color`
     - Hint: if you can’t find AppData try going to View > Hidden items in file explorer and hitting the checkbox 
   - **MAC**: `/Library/Application Support/Blackmagic Design/Fusion/Scripts/Color`
7. Restart Resolve
8. Now when you go open Resolve and, in the toolbar, click “Workspace > Scripts” it should be available.

## Using the script
### Steps
1. Open a timeline in your resolve project
2. Enable Dynamic Project Switching
3. Activate the script by clicking on it in "Workspace > Scripts"
4. At the top right select the timeline that needs color
5. At the top left confirm the naming of the powergrade album
6. Select from the 3 checkboxes you preferences. "Ignore capitalization" and "ignore version number" are for loosening your search. "Label stills with timecode" will label grabbed stills with timecode for matching clips making it easier to apply.
7. In the right panel, browse to the project and timeline you want, then hit "Add Selected" at the bottom.
8. The left panel will populate with timelines to search. When ready hit "Grab Grades" and watch it run!
