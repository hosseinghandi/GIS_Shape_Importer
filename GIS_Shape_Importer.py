import shapefile
import Rhino.Geometry as rg
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from ghpythonlib.component import add_warning


def move_to_center(nested_points):
    all_pts = [pt for shape in nested_points for part in shape for pt in part]
    if not all_pts:
        return nested_points

    xs = [pt.X for pt in all_pts]
    ys = [pt.Y for pt in all_pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    center_pt = rg.Point3d((min_x + max_x) / 2, (min_y + max_y) / 2, 0)
    move_vec = rg.Vector3d(-center_pt.X, -center_pt.Y, 0)

    moved = []
    for shape in nested_points:
        moved_shape = []
        for part in shape:
            moved_part = [pt + move_vec for pt in part]
            moved_shape.append(moved_part)
        moved.append(moved_shape)

    return moved


def read_shapefile_points_and_attributes(shp_path):
    try:
        sf = shapefile.Reader(shp_path)
        fields = [f[0] for f in sf.fields[1:]]  # Field names

        shapes_parts = []         # Nested point structure [shape][part][pt]
        attribute_values = []     # Flat list [shape] of field values
        attribute_keys = fields   # Single list

        # Read all shapes and split parts
        for shape_idx, shape_rec in enumerate(sf.shapeRecords()):
            shape = shape_rec.shape
            record = shape_rec.record
            points = shape.points
            parts = list(shape.parts) + [len(points)]

            part_list = []
            for i in range(len(parts) - 1):
                start = parts[i]
                end = parts[i + 1]
                part_pts = [rg.Point3d(x, y, 0) for x, y in points[start:end]]
                part_list.append(part_pts)

            shapes_parts.append(part_list)
            attribute_values.append(list(record))

        # Move all points to center
        centered_shapes = move_to_center(shapes_parts)

        # Build geometry tree: {i;j}
        points_tree = DataTree[object]()
        values_tree = DataTree[object]()
        keys_tree = DataTree[object]()

        for i, shape in enumerate(centered_shapes):
            record = attribute_values[i]
            for j, part in enumerate(shape):
                path = GH_Path(i, j)
                for pt in part:
                    points_tree.Add(pt, path)

                # Duplicate all keys and values for each part
                for k, val in enumerate(record):
                    key = attribute_keys[k] if k < len(attribute_keys) else None
                    values_tree.Add(val, path)
                    keys_tree.Add(key, path)

        return points_tree, keys_tree, values_tree

    except Exception as e:
        print("Error reading shapefile: " + str(e))
        return None, None, None


# === EXECUTION BLOCK ===

try:
    if generate and shp_path:
        try:
            sf = shapefile.Reader(shp_path)  # Validate file
        except Exception:
            raise RuntimeError("The shapefile is not valid or cannot be read.")

        points, attributes_keys, attributes_values = read_shapefile_points_and_attributes(shp_path)

    elif shp_path and not generate:
        add_warning("Set 'generate' to True to process the shapefile.")

    else:
        add_warning("Please provide a valid shapefile path and set 'generate' to True.")

except Exception as e:
    raise RuntimeError(f"An error occurred while generating geometry: {str(e)}")
