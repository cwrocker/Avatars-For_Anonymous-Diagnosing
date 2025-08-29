import bpy
import os

# === CONFIGURATION ===
FBX_FOLDER = '/Users/chancellorwoolsey/Documents/Research Work/images_and_videos/TTY'
OUTPUT_FOLDER = '/Users/chancellorwoolsey/Documents/Research Work/images_and_videos/ES'
RENDER_WIDTH = 1280
RENDER_HEIGHT = 720
FPS = 30
FRAME_COUNT = 5 * FPS  # 5 seconds × 30 FPS = 150 frames

# === RENDER SETTINGS ===
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.constant_rate_factor = 'HIGH'
scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
scene.render.fps = FPS
scene.render.resolution_x = RENDER_WIDTH
scene.render.resolution_y = RENDER_HEIGHT

# === BACKGROUND TO NEAR-WHITE ===
bpy.data.worlds["World"].use_nodes = False
bpy.data.worlds["World"].color = (0.05, 0.05, 0.05)

# === HELPER FUNCTIONS ===

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def make_all_meshes_light_gray():
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            mat = bpy.data.materials.new(name="AvatarMaterial")
            mat.use_nodes = False
            mat.diffuse_color = (0.85, 0.85, 0.85, 1.0)  # Light gray RGBA
            obj.data.materials.clear()
            obj.data.materials.append(mat)

def ensure_camera():
    if not scene.camera:
        bpy.ops.object.camera_add(location=(5, -5, 5), rotation=(1.1, 0, 0.8))
        scene.camera = bpy.context.object

def ensure_balanced_lighting():
    # Front light
    bpy.ops.object.light_add(type='POINT', location=(4, 4, 4))
    main = bpy.context.object
    main.data.energy = 700
    main.data.shadow_soft_size = 2.0
    main.data.use_shadow = True

    # Soft fill light to reduce shadows
    bpy.ops.object.light_add(type='POINT', location=(-4, -4, 4))
    fill = bpy.context.object
    fill.data.energy = 400
    fill.data.use_shadow = False

    # Optional top-down ambient light
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
    top = bpy.context.object
    top.data.energy = 300
    top.data.shape = 'SQUARE'
    top.data.size = 10
    top.data.use_shadow = False

# === MAIN BATCH LOOP ===
for filename in os.listdir(FBX_FOLDER):
    if not filename.lower().endswith(".fbx"):
        continue

    fbx_path = os.path.join(FBX_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0] + ".mp4")

    print(f"🎞 Rendering {filename} → {output_path}")
    clear_scene()

    bpy.ops.import_scene.fbx(filepath=fbx_path)
    make_all_meshes_light_gray()
    ensure_camera()
    ensure_balanced_lighting()

    scene.frame_start = 1
    scene.frame_end = FRAME_COUNT
    scene.render.filepath = output_path

    bpy.ops.render.render(animation=True)

print("✅ All renders complete.")