###### **3D Assets**

Regarding the 3D assets, several constraints related to Ursina had to be considered, especially regarding the number of triangles. Some models had to be optimised quite aggressively in order to avoid unnecessary performance loss, particularly when multiple enemies, spells, and environmental elements are present on the map at the same time.



The first issue encountered involved models in the .glb format. Although this format is theoretically well suited for transporting complete models with integrated textures, Ursina did not correctly handle some files exported from Blender. In several cases, models were imported without their textures despite being correctly configured in the modelling software. Some models appeared completely white or black in the game. Several solutions were tested to work around this problem, including re-exporting with different versions of the glTF format, manually grouping textures into the same folder, and converting textures into simpler formats such as .png.



Difficulties were also encountered with .fbx files. This format was initially considered because it is widely used and normally makes animation management easier. However, Ursina did not properly support the FBX exports used in the project, and some models simply refused to load. Different export settings from Blender were tested, including the differences between FBX ASCII and Binary. Different versions of Blender were also tested to determine whether the issue came from the export pipeline. In the end, the use of FBX was limited to cases where it was strictly necessary, while other formats that were more stable with Ursina were preferred.



Another important issue involved the scale of the models. When imported into Ursina, some objects appeared extremely large or extremely small compared to the rest of the scene. This mainly came from differences in units between Blender and Ursina, as well as transformations not being fully applied before export. As a result, some assets required manual corrections directly in the code in order to maintain visual consistency between the different biomes and characters.



Several limitations related to animations were also observed. Some animations exported from Blender lost their smoothness or were not correctly recognised by Ursina. Certain armatures therefore had to be simplified, the number of bones reduced, and some keyframes reworked in order to keep the animations usable in the engine. The possibility of loading animations separately rather than directly inside the model was also explored, as this could provide better modularity for future characters. In addition, the number of animations recognised by Ursina within a single file appeared to be limited to around 15, even when Blender was able to read more.



One of the biggest issues mainly involved materials and the export process between Blender and Ursina. With .obj files, traditional textures worked relatively well when the PBR extension was enabled. However, with .glb files, a large amount of material information simply did not transfer correctly. This required a considerable amount of testing before reaching a solution that was both clean and reusable.



The technique that was eventually selected relies on a system of material palettes organised into several categories such as “dull”, “standard”, “glow”, and “metal”. These palettes were created in Blender using material node setups based on only three PNG textures: a base colour map, an attribute map, and an emission map.



The process then involved using Blender's UV Mapping editor, selecting specific faces of a model, and moving and resizing them in the UV editor so that they pointed towards a specific area of the palette. This technique took a significant amount of time at first, but it ultimately proved worthwhile because it made it possible to create consistent materials that were easy to modify and, most importantly, compatible with Ursina.



Several Blender modelling tools were used regularly throughout the project and proved to be particularly useful. This includes sculpting for the upcoming desert map, where Grand Canyon-style rocks were created, as well as the Knife tool, which was used to create the “A” from “Arkanum” on the coins. X-Ray mode was also especially useful for handling certain complex selections.



The spells were also entirely modelled by hand using different techniques such as subdivision, masks, Simple Deform, vertex groups, and vertex weight editing. Unlike the characters, the spells are not actually animated. They are simply standard .glb models that rotate around the player directly through Ursina by modifying their self.rotation\_y.



Tests were also carried out using animated strips, but this required a high level of precision regarding frames, and the overall process was particularly long to set up for a result that was not necessarily better than a static version.



One fireball spell also used Blender's particle rendering features, including systems such as Quick Smoke, domain containers, and different volumetric effects. The main issue was that Ursina did not take these effects into account during import. One possible alternative would have been to use 2D sprite sheets, but this approach was not considered particularly convincing. It would have required constantly managing sprite orientation, frames, FPS, and their appearance on the map. More importantly, the resulting PNG images did not really match the original 3D model that had been created.



Several environmental elements were also entirely modelled by hand, including the shop, different map corners, and the well-known mushroom. The mushroom was initially intended to become the main boss of the game, but its rig was particularly complicated to create because of its non-humanoid shape. A complicated rig also means longer and more difficult animation work. On top of that, it used Blender-specific Color Ramp nodes, which do not export correctly to Ursina.	 


###### **Left to do :**



menus et lobby completely(chat, avatar+level players, choice for competence, login check + room services/ui \& socketio func -> button play for host/ready for players, link map, system host shift/or destroy room) + Database sync with all fields needed



dashboard (dahsborad page -> profile data | edit/save data | delete | logout) : (arbre de cmpt choisi, leaderboard, avatar choice, xp to next level)

https://www.youtube.com/watch?v=1nxzOrLWiic

https://www.youtube.com/watch?v=CDe5wfHAlAY



forgot password link + propose username for registration when it already exists + fix sign container on mobile

escape inputs and server puts + jsonify verif + ddos prevention + threadpool limit for room creation + mutexes https://flask.palletsprojects.com/en/stable/web-security/

https://flask.palletsprojects.com/en/stable/deploying/

https://flask.palletsprojects.com/en/stable/appcontext/

https://flask.palletsprojects.com/en/stable/reqcontext/