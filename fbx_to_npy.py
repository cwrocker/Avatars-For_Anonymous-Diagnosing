import bpy
import numpy as np
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []
input_fbx, output_npy = argv

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=input_fbx)

armature = next((obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE'), None)
if not armature:
    print("❌ No armature found.")
    sys.exit(1)

scene = bpy.context.scene
scene.frame_set(scene.frame_start)

joint_names = [bone.name for bone in armature.pose.bones]
joint_names.sort()
frames = range(scene.frame_start, scene.frame_end + 1)

motion = []

for f in frames:
    scene.frame_set(f)
    joints = []
    for jname in joint_names:
        bone = armature.pose.bones.get(jname)
        if bone:
            pos = armature.matrix_world @ bone.head
            joints.append([pos.x, pos.y, pos.z])
    motion.append(joints)

motion = np.array(motion)  # shape: [T, J, 3]
np.save(output_npy, motion)
print(f"✅ Saved: {output_npy}")
