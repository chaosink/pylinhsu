import bpy


# ----------------------------------------------------------------------------------------------------
# Shortcuts.

O = bpy.ops
D = bpy.data
C = bpy.context


# ----------------------------------------------------------------------------------------------------
# Functions.

def delete_all():
    O.object.select_all(action='SELECT')
    O.object.delete(use_global=False, confirm=False)


def do_in_area_region(func, area_type, region_type='WINDOW'):
    for area in C.screen.areas:
        if area.type == area_type:
            for region in area.regions:
                if region.type == region_type:
                    override = C.copy()
                    override["area"] = area
                    override["region"] = region
                    with C.temp_override(**override):
                        func()


def do_in_area_space(func, area_type, space_type):
    for area in C.screen.areas:
        if area.type == area_type:
            for space in area.spaces:
                if space.type == space_type:
                    override = C.copy()
                    override["area"] = area
                    override["space_data"] = space
                    with C.temp_override(**override):
                        func()


def use_shading_type(shading_type):
    def func():
        C.space_data.shading.type = shading_type
    do_in_area_space(func, 'VIEW_3D', 'VIEW_3D')


def set_active_layer_collection_by_name(lc_name):
    layer_collection = C.view_layer.layer_collection.children[lc_name]
    C.view_layer.active_layer_collection = layer_collection


def set_active_layer_collection(lc):
    C.view_layer.active_layer_collection = lc


# No effect for the moment.
def close_layer_collections():
    def func():
        # O.outliner.expanded_toggle()
        O.outliner.show_one_level(open=False)
    do_in_area_region(func, 'OUTLINER')
