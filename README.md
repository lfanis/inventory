# Inventory
You cannot loose what you do not know you had. 
<-- XXX Insert fancy logo here 

## Building and running
Install the requirements then run it as a regular streamlit

```shell
pip install -r requirements.txt
streamlit run main.py 
```

### Docker
If you must, a Dockerfile is provided, keep in mind the stocks.db file need to be on a persistent storage otherwise all is for naught. 

```shell
docker volume create --name inventory-st-data
docker volume ls

docker build -t inventory-st .
docker images # 
docker run -v inventory-st-data:/app/db -p 8501:8501 inventory-st 
```

## Structure 
For now sticking to two pages, one for main usage and one for component addition

### Main page
    - Display components 
    - Edit rows
    - Export to csv

### Adding new components
All the usable fields in one place, it is relatively easy to do bulk updates of "similar" items 

## TODO
- [X] Editable grid , https://discuss.streamlit.io/t/editable-data-tables-in-streamlit/529/15
- [X] export function
- [] Better search function 
- [] generate 2D QR code
- [] For datasheet, if the URL is manageable, download it, save it under /datasheets/$Manufacturer/ManufacturerPN.pdf 
- [] For images not sure yet, but either add an upload button or URL choice, if URL download it 
- [] For packaging type, I need to get the complete full list (maybe wikipedia is good enough) and dynamicaly generate it/similar to data/Manufacturer.txt
- [] Need to add a field to update the manufacturer and also the DB behind it

## Alternatives
This [Simple sheet inventory](https://docs.google.com/spreadsheets/d/1KIXDqqZXwHDRTK2vqVpYB6x4SNqN8tGn40qxSi1V7mE/edit#gid=0) is as good if not arguably better, use that .

## Generating DataMatrix /QR code
The easiest way would be to either make it free floating or on submit/add HW to generate the code using [PPF](https://github.com/adrianschlatter/ppf.datamatrix) 

```python
from ppf.datamatrix import DataMatrix
myDataMatrix = DataMatrix(Values)
```
Right now, I ran into an issues displaying the SVG with the correct size (it is tiny). ppf.datamatrix does not set viewbox. One way would be to convert it to png/jpg and then display it . 

## Rendering PDF
Maybe one day i want to render pdf inside the [app](https://discuss.streamlit.io/t/rendering-pdf-on-ui/13505/10) ?

# Links
- [Userfull packaging type](https://en.wikipedia.org/wiki/List_of_integrated_circuit_packaging_types) 