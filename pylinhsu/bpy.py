import bpy

# Shortcuts.
O = bpy.ops
D = bpy.data
C = bpy.context

def DeleteAll():
    O.object.select_all(action='SELECT')
    O.object.delete(use_global=False, confirm=False)

def DoInAreaRegion(func, area_type, region_type='WINDOW'):
    for area in C.screen.areas:
        if area.type == area_type:
            for region in area.regions:
                if region.type == region_type:
                    override = C.copy()
                    override["area"] = area
                    override["region"] = region
                    with C.temp_override(**override):
                        func()

def DoInAreaSpace(func, area_type, space_type):
    for area in C.screen.areas:
        if area.type == area_type:
            for space in area.spaces:
                if space.type == space_type:
                    override = C.copy()
                    override["area"] = area
                    override["space_data"] = space
                    with C.temp_override(**override):
                        func()

def UseShandingType(shading_type):
    def func():
        C.space_data.shading.type = shading_type
    DoInAreaSpace(func, 'VIEW_3D', 'VIEW_3D')

def SetActiveLayerCollectionByName(lc_name):
    layer_collection = C.view_layer.layer_collection.children[lc_name]
    C.view_layer.active_layer_collection = layer_collection

def SetActiveLayerCollection(lc):
    C.view_layer.active_layer_collection = lc

# No effect for the moment.
def CloseLayerCollections():
    def func():
        # O.outliner.expanded_toggle()
        O.outliner.show_one_level(open=False)
    DoInAreaRegion(func, 'OUTLINER')
