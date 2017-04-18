# Search Engine for the UCL Website
##### UCL Computer Science - COMPM052 Information Retrieval and Data Mining
###### GROUP27

### How to run
##### Add database credentials
Create a `.pgpass` file in your home directory of your computer with the following contents: 
`<hostname>:<port>:<database>:<username>:<password>`

followed by modifying access permission of the file:
`chmod 600 ~/.pgpass`

##### Install all requirements
~~~~
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~~

##### Run the search engine
From the top-level directory, run `python -m app.search_engine`