# ShapeFile_Geometry_Attribute_Reader

This component reads **ESRI Shapefiles (.shp)**, converts geometry into **Grasshopper DataTrees**, extracts **attribute keys and values**, and automatically moves the dataset to the **Rhino origin center**.

It automatically extracts:

* shape geometry points
* multipart boundaries
* attribute field names
* attribute values
* shape-part tree structure
* centered geometry

This helps users **reduce the time and complexity of GIS preprocessing**, especially when preparing shapefile-based workflows for:

* urban design
* GIS-to-Rhino conversion
* parcel studies
* road networks
* simulation boundaries
* Ladybug preprocessing

---

## How to Use

### 1. Connect the shapefile

* Provide the **`.shp` file path**
* Make sure the **PyShp library** is available:
Install if needed:

```python
pip install pyshp
```
and 

```python
import shapefile
```

### 2. Run the component

* Switch the **Boolean toggle to `True`**

### 3. Use the outputs

The component returns:

* points_tree
* attributes_keys
* attributes_values
* multipart tree structure shape_index;part_index

### 4. Connect to downstream workflows

Use the generated geometry directly in:

* Rhino modeling
* urban heat workflows
* zoning visualization
* road analysis
* Ladybug simulations

---

## Citation and Project Use

If you use this tool in research, publications, teaching, or professional projects, please cite the repository and kindly inform the author.

**Author:** Hossein Ghandi

Feedback, case studies, and derived applications are highly appreciated and help support future development of the workflow.
