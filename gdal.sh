
for filename in ./data/*.jpg; do
	# echo $(basename $filename .jpg);
	gdal_translate -of GTiff -a_srs EPSG:3857 $filename "data/$(basename $filename .jpg).tif"
done