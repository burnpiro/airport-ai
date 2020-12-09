## Layout parser

### Quickstart (generating layout contour)
- Copy your layout img into `layout_parser/in/` folder
- Define `OBJECT_COLORS` as a list of colors per object type `R,G,B object_name;R,G,B object_name fill min_size max_size` (More details in [Object definition](#object-string-type-definition))
- Build docker image (make sure you're in `layout_parser` directory):
```shell
docker-compose up
```

It should generate 2+ files for every layout file in `layout_parser/in/` folder:
- `image_name.json` - layout definition
- `layout-image_name.png` - contour drawn onto input image (just to chek if it's correct)
- `object_type-image_name.png` - contour of the object type drawn onto input image (one image per object type)

[Example 1990x2427](./example.png) with 5 different object types (line width is small in compare with the image resolution):

### Options

##### System ENV variables
- `OBJECT_COLORS` as a list of colors per object type `R,G,B object_name;R,G,B object_name fill min_size max_size` (More details in [Object definition](#object-string-type-definition))
- `SMALL_ITEMS` as a list of colors per object type `R,G,B object_name;R,G,B object_name fill min_size max_size` (More details in [Object definition](#object-string-type-definition)), this should be a definition of small objects only because it has max set to be 0.1% of the layout area.
- `OBJECTS_EPS` min part of the image that large objects should take to be considered ab `object` (0.01 means 1% of the image) (defaults to 0.01%)
- `SMALL_ITEMS_EPS` min part of the image that small item objects should take to be considered an `small object` (0.01 means 1% of the image) (defaults to 0%)

##### Object string type definition:
`R,G,B name fill min_size max_size`

- `R` - integer 0-255 (value for red color)
- `G` - integer 0-255 (value for green color)
- `B` - integer 0-255 (value for blue color)
- `name` - string, name of the object e.g. `restaurant`
- `fill` - string, either `fill` or `nofill` (optional, defaults to `fill`)
- `min_size` - integer, min size of the object in pixels (optional)
- `max_size` - integer, max size of the object in pixels (optional)