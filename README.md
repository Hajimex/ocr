# OCR
## API List
### OCR
This API does preprosessing and return OCRed text
```
./bin/ocr.py -i image_url -k GCP_APIKEY -a anchor_photo_url -p relative_positions_by_JSON
this will create the cropped images and return OCRed texts
```
- sample
```
python bin/ocr.py -i "http://hajimek.com/ANH10-0001549.jpg" -k XXXX -a "http://hajimek.com/anchor/crop.png" -p '[{"y1": 34, "x2": 380, "x1": 152, "y2": 60}, {"y1": 119, "x2": 1321, "x1": 1000, "y2": 138}]' -s '{"width": 1718, "height":1205}'
```
### Similarity
This API receives an anchor photo and the registered file list first, and this returns the similarity score for each registered document.
```
python bin/similarity.py  -i anchor_photo_url -p documents_path
```
- sample
```
 python bin/similarity.py  -i "http://hajimek.com/anchor/crop.png" -p "./data/documents"
```


## Flow image
https://docs.google.com/presentation/d/11keDKTe93SGOldR3mkXgmSGsbbMNW7dyhYISISn67D0/edit?pli=1#slide=id.p
