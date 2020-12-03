## Layout parser

### Quickstart (generating layout contour)
- Copy your layout img into `layout_parser/in/` folder
- Build docker image (make sure you're in `layout_parser` directory):
```shell
docker-compose up
```

It should generate 2 files for every layout file in `layout_parser/in/` folder:
- `image_name.json` - layout definition
- `with-ctn-image_name.png` - contour drawn onto input image (just to chek if it's correct)

example (line width is small in compare with the image resolution):
![](./out_sample.png)