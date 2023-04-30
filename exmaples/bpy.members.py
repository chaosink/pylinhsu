from pylinhsu.bpy import *

'''
>>> C.
      active_action
      active_annotation_layer
      active_bone
      active_editable_fcurve
      active_gpencil_frame
      active_gpencil_layer
      active_nla_strip
      active_nla_track
      active_object
      active_operator
      active_pose_bone
      active_sequence_strip
      annotation_data
      annotation_data_owner
      area
      as_pointer(
      asset_file_handle
      asset_library_ref
      bl_rna
      bl_rna_get_subclass(
      bl_rna_get_subclass_py(
      blend_data
      collection
      copy()
      driver_add(
      driver_remove(
      edit_object
      editable_bones
      editable_fcurves
      editable_gpencil_layers
      editable_gpencil_strokes
      editable_objects
      engine
      evaluated_depsgraph_get(
      get(
      gizmo_group
      gpencil_data
      gpencil_data_owner
      id_data
      id_properties_clear(
      id_properties_ensure(
      id_properties_ui(
      image_paint_object
      is_property_hidden(
      is_property_overridable_library(
      is_property_readonly(
      is_property_set(
      items(
      keyframe_delete(
      keyframe_insert(
      keys(
      layer_collection
      mode
      object
      objects_in_mode
      objects_in_mode_unique_data
      particle_edit_object
      path_from_id(
      path_resolve(
      pop(
      pose_object
      preferences
      property_overridable_library_set(
      property_unset(
      region
      region_data
      rna_type
      scene
      screen
      sculpt_object
      selectable_objects
      selected_bones
      selected_editable_actions
      selected_editable_bones
      selected_editable_fcurves
      selected_editable_keyframes
      selected_editable_objects
      selected_editable_sequences
      selected_movieclip_tracks
      selected_nla_strips
      selected_objects
      selected_pose_bones
      selected_pose_bones_from_active_object
      selected_sequences
      selected_visible_actions
      selected_visible_fcurves
      sequences
      space_data
      temp_override(
      tool_settings
      type_recast(
      ui_list
      values(
      vertex_paint_object
      view_layer
      visible_bones
      visible_fcurves
      visible_gpencil_layers
      visible_objects
      visible_pose_bones
      weight_paint_object
      window
      window_manager
      workspace
'''

'''
>>> D.
      actions
      armatures
      as_pointer(
      batch_remove(
      bl_rna
      bl_rna_get_subclass(
      bl_rna_get_subclass_py(
      brushes
      cache_files
      cameras
      collections
      curves
      driver_add(
      driver_remove(
      filepath
      fonts
      get(
      grease_pencils
      hair_curves
      id_data
      id_properties_clear(
      id_properties_ensure(
      id_properties_ui(
      images
      is_dirty
      is_property_hidden(
      is_property_overridable_library(
      is_property_readonly(
      is_property_set(
      is_saved
      items(
      keyframe_delete(
      keyframe_insert(
      keys(
      lattices
      libraries
      lightprobes
      lights
      linestyles
      masks
      materials
      meshes
      metaballs
      movieclips
      node_groups
      objects
      orphans_purge(
      paint_curves
      palettes
      particles
      path_from_id(
      path_resolve(
      pointclouds
      pop(
      property_overridable_library_set(
      property_unset(
      rna_type
      scenes
      screens
      shape_keys
      sounds
      speakers
      temp_data(
      texts
      textures
      type_recast(
      use_autopack
      user_map(
      values(
      version
      volumes
      window_managers
      workspaces
      worlds
'''

'''
>>> O.
      action
      anim
      armature
      asset
      boid
      brush
      btool
      buttons
      cachefile
      camera
      clip
      cloth
      collection
      console
      constraint
      curve
      curves
      cycles
      dpaint
      ed
      export_anim
      export_mesh
      export_scene
      file
      fluid
      font
      geometry
      gizmogroup
      gpencil
      graph
      image
      import_anim
      import_curve
      import_image
      import_mesh
      import_scene
      info
      lattice
      marker
      mask
      material
      mball
      mesh
      nla
      node
      object
      outliner
      paint
      paintcurve
      palette
      particle
      pha
      polyhavenassets
      pose
      poselib
      preferences
      ptcache
      render
      rigidbody
      safe_areas
      scene
      screen
      script
      sculpt
      sculpt_curves
      sequencer
      sound
      spreadsheet
      surface
      text
      texture
      transform
      ui
      uv
      view2d
      view3d
      wm
      workspace
      world
'''

print(f'{" " * 0}D.window_managers: {len(D.window_managers)}')
print(f'{" " * 4}D.window_managers["WinMan"].windows: {len(D.window_managers["WinMan"].windows)}')
print(f'{" " * 8}D.workspaces: {len(D.workspaces)}')
print(f'{" " * 12}D.screens: {len(D.screens)}')
print()

for window_manager in D.window_managers:
    print(f'{" " * 0}window_manager: {window_manager.name}')
    for window in window_manager.windows:
        print(f'{" " * 4}window: {window}')
        workspace = window.workspace
        print(f'{" " * 8}workspace: {workspace.name}')
        for screen in workspace.screens:
            print(f'{" " * 12}screen: {screen.name}')
            for area in screen.areas:
                print(f'{" " * 16}area: {area.type}')
                for region in area.regions:
                    print(f'{" " * 20}region: {region.type}')
                for space in area.spaces:
                    print(f'{" " * 20}space: {space.type} {space}')
print()

print(f'{" " * 0}D.scenes: {len(D.scenes)}')

print(f'{" " * 4}D.scenes["Scene"].view_layers: {len(D.scenes["Scene"].view_layers)}')
print(f'{" " * 4}D.worlds: {len(D.worlds)}')
print(f'{" " * 4}D.objects: {len(D.objects)}')

print(f'{" " * 8}D.armatures: {len(D.armatures)}')
print(f'{" " * 8}D.cameras: {len(D.cameras)}')
print(f'{" " * 8}D.curves: {len(D.curves)}')
print(f'{" " * 8}D.grease_pencils: {len(D.grease_pencils)}')
print(f'{" " * 8}D.hair_curves: {len(D.hair_curves)}')
print(f'{" " * 8}D.images: {len(D.images)}')
for image in D.images:
    print(f'{" " * 16}image: {image.name}')
print(f'{" " * 8}D.lattices: {len(D.lattices)}')
print(f'{" " * 8}D.lights: {len(D.lights)}')
print(f'{" " * 8}D.lightprobes: {len(D.lightprobes)}')
print(f'{" " * 8}D.meshes: {len(D.meshes)}')
print(f'{" " * 8}D.metaballs: {len(D.metaballs)}')
print(f'{" " * 8}D.speakers: {len(D.speakers)}')
print(f'{" " * 8}D.texts: {len(D.texts)}')
print(f'{" " * 8}D.volumes: {len(D.volumes)}')
print()

print(f'{" " * 0}D.actions: {len(D.actions)}')
print(f'{" " * 0}D.collections: {len(D.collections)}')
print(f'{" " * 0}D.brushes: {len(D.brushes)}')
print(f'{" " * 0}D.fonts: {len(D.fonts)}')
print(f'{" " * 0}D.libraries: {len(D.libraries)}')
print(f'{" " * 0}D.linestyles: {len(D.linestyles)}')
print(f'{" " * 0}D.masks: {len(D.masks)}')
print(f'{" " * 0}D.materials: {len(D.materials)}')
for material in D.materials:
    print(f'{" " * 4}material: {material.name}')
print(f'{" " * 0}D.movieclips: {len(D.movieclips)}')
print(f'{" " * 0}D.node_groups: {len(D.node_groups)}')
print(f'{" " * 0}D.paint_curves: {len(D.paint_curves)}')
print(f'{" " * 0}D.palettes: {len(D.palettes)}')
print(f'{" " * 0}D.particles: {len(D.particles)}')
print(f'{" " * 0}D.pointclouds: {len(D.pointclouds)}')
print(f'{" " * 0}D.shape_keys: {len(D.shape_keys)}')
print(f'{" " * 0}D.sounds: {len(D.sounds)}')
print()

print(D.scenes['Scene'].objects.items()) # Collection of original data, ordered by add time.
print()
print(D.objects.items()) # Flattened variable for easy access. Collection of references, ordered by name.
print()
