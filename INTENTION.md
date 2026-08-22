# Why prim.scene exists

An mp4 is a frozen view. A Three.js file is a program. Neither is a store an agent can open, validate, and hand to another tool.

**prim.scene is one cinematic beat as a file.** Camera, objects, duration, type, audio cite. The render is a projection. The scene is the source of truth.

If a field is in this spec, an ident failed for lack of it.

- **One scene, one duration.** A fly-through is a scene. A talking-head hold is a scene. They do not share a file.
- **`scene.json` is authority.** HTML/WebGL/mp4 are views.
- **Cite audio. Do not own the song.** music-forge cuts the bed; the scene points at it.
- **Do not clip the mesh.** A camera key that puts the lens inside an object is invalid once the renderer can measure it.

A video is not a scene. That is `prim.video`: an ordered collection of scene packs. Compose, don't merge.
