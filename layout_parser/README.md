## Layout parser

### Quickstart (generating layout contour)
- Copy your layout img into `layout_parser/in/` folder
- Define `OBJECT_COLORS` as a list of colors per object type `R,G,B object_name;R,B,G object_name2`
- Build docker image (make sure you're in `layout_parser` directory):
```shell
docker-compose up
```

It should generate 2+ files for every layout file in `layout_parser/in/` folder:
- `image_name.json` - layout definition
- `layout-image_name.png` - contour drawn onto input image (just to chek if it's correct)
- `object_type-image_name.png` - contour of the object type drawn onto input image (one image per object type)

[Example 1990x2427](./example.png) with 5 different object types (line width is small in compare with the image resolution):
