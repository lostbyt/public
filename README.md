Some python programs developped for post production:

-Auto beauty: This tool for Nuke software, will allow the user to import a multi render pass from Cycle(Blender) or Redshift and reconstruct to match the beauty. Some options like denoise, sharpen, and grade are directly implemented in the menu.

-Fake parallax: This tool for Nuke software is based on a Alexander Hanneman tutorial (https://www.youtube.com/watch?v=avtDQcZNThI), it allows to quickly create a "push in zoom" with parallax even with 2D elements. It uses a uv distortion map.
The tool automates all the process, the user has just to plug his rotos and setup the movment he wants.

-Reads cleaner: This is a tool I wrote to help organize the reads node in a nuke script. You can order them by ascending/ descending frame range lenght or by name.

-ReadGeo renamer: I like to import in Nuke software my 3D geometry in separate readgeo nodes, I feel it is more convenient and flexible to manage your projections. Renaming each nodes can be tedious. Thoses few lines of code will do it for you, with the same name used in your 3D package.
