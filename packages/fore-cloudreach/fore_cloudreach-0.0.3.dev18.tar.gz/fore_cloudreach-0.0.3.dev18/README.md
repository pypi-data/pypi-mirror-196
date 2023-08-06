# FORE stand for `Fin Ops REporter`

The package is publish at: [PyPi](https://pypi.org/project/fore-cloudreach/)

## Autentication and authorization Overview
This package will be published on PyPi as downloadable package.
The main purpose of it is to Oauth2 authenticate a user of the Jupiter Notebook (**JpN**) that will need access to Google Sheets application. The security context is the current macOS user who use the Jupiter notebook and is logged in with Google's account.
In order to ustilize the Google's Sheets API the JpN code would need to:
</br>

- enable Google Sheet API in the GCP project (projectID: `invertible-star-370411`) where the application is registered.
- install the package `fore_cloudreach` from PyPi;
- recieve a file `credentials.json` from the same project and store its content as string in the AWS Secret Manager, as a secret 
named `fore/client_id`.
- Logging in the Cloudreach's google account and in the prompted window authorized the JpN application to access the Google Sheets API.
- at the time of running the JpN code, the user should provide the AWS access key id and its secret key.
</br>

As of the initial version, the authentication of the user is performed over the Google's SignIn of the currently logged user in the Google account in the browser.
The authentication token is stored in the memory for the life span of the session.
</br>

### Preparation steps
In order to star using the reports import automation, few preparation steps are required.

1. A customers mapping file must be created with two mandatory tab sheets in it.

The first tab sheet have to be named `Map` and it should contain a table starting in cell A1 with the following columns:
    * Customer_Name	- the name of the customer as it is registered in the reports
    * Customer_ID - customer ID	
    * Spreadsheet_ID - the global file ID as found in the file URL
    ![ID from URL](docs/url-img.png) 	
    * AWS_Org_ID - the AWS id for the custpmer	
    * CH_ID - the CloudHealth ID of the customer

The second tab must be named `Reports Catalog` and has a table starting at cell A1 with the following columns:
    * ID - cataloging number of the report. It will be used in the generating the reports' tab names
    * Report Name - the report's name in a snake_case naming convention. Will be used as a search criteria for finding the report ID when generating the tab names into the customers report files.

2. One file per customer with one (first, idx=0) tab sheet named `Template`.

The tamplate sheet will duplicated each time a report is being imported. Any changes in the template sheets will be reflected on the next report import only.
The global unique file ID from the URL must be properlly logged in the mapping file as described above.
The `fore_cloudreach` library will import the report name in duplicated tab sheet and write the report name in cell B1. The reports data will start being imported from cell B2 with report columns written in row 2 and the table data following below.

### Maintanence of mapping file and reports catalog 
When a new customer must be on-boarded - it should be registered in the customers mapping file in the tab sheet `Map` as a new record in the exsting table following the rules descibed above.
The same is valid for a new report - must be registered in the tab sheet `Reports Catalog`

All the files are located on Google's drive folder named `FinOps Monthly` with URL ID: `1cyeyh8dX6k6yTvDSHHO2z7-ADEvh04ZM`
</br></br>

### HowTos
</br>

1. Import customer's report data by integrating fore_cloudreach library in Jupyter notebook:
    
------    
In the main notebook `Generate FinOps Report CSVs.ipynb`:
------

- install the package `fore_cloudreach` by:
    ```python
        !pip install fore_cloudreach
    ```

- import the package by:
    ```python
        import fore_cloudreach as fc
    ```

- declare the require variables by:
    ```python
        aws_secret_name = "fore/client_id"
        aws_region_name = "eu-central-1"
    ```

- right after the cell that's establishing AWS session, create authentication object and invoke the method to get the required credentials. Also instantiate the ingester by placing the following code:
    ```python
        authenticator = fc.Auth(session, [])
        # invoke the method getting the Google's credentials
        authenticator.get_ggl_creds(aws_secret_name,aws_region_name)
        if not fc.gcreds:
            print("ERROR: Unable to located mandatory credentials! Exiting...")
            exit()
        # Instantiate the ingester object
        ingester = fc.Ingester(creds=fc.gcreds, mapping_file_id="")
        %store ingester
    ```

- In each cell that is calling the reports sub-notebooks, for the part `pm.execute_notebook` in the parameters dictionary add the customer name parameter by:
    ```python
        ... ,
        customer_name=customer['name']
        
        # to become:
        parameters=dict(
            aws_sts_creds=customer['aws_session_token'], 
            export_path=f"{temp_export_path}",
            customer_name=customer['name']
        )
    ```
------
In each AWS or CH sub-notebook:
------

- in the list of parameters for Papermill **add** the customer name by:
    ```python
        ...
        customer_name = ""
    ```

- declare a variable `skip_export_to_csv` to control the export of the report into CSV file by:
    ```python
        skip_export_to_csv = False
    ```

- in the cell where the data frame is define with `df_xxx_xxx_cleaned`, add the indexer definition and set the indexer name to the report name equal to the CSV file name by:
    ```python
        # Note: in each sub-notebook the data frame varaible will have different name in the format `df_xxx_xxx_cleaned`
        # and the indexer name should be set to a differrent report name matching the name of the CSV file and being listed into the report catalog of the customer mapping file.
        indexer = df_rightsize_recs_cleaned.index
        indexer.name = "aws_ec2_rightsizing"
    ```

- in the last cell with code which exports to CSV,  by:
    ```python
        
        # initiate the import
        %store -r ingester
        api_import_feedback = ingester.load_report(customer_name, df_rightsize_recs_cleaned)
        print(f"API feedback from the import: {api_import_feedback}")

        if not skip_export_to_csv:
            df_rightsize_recs_cleaned.to_csv(export_path)

    ```
</br>


2. Import customer's report data from pandas' DataFrame:

- using the fore_cloudreach library in Jupyter notebook:

example-1:

```python

    !pip install fore_cloudreach

    import fore_cloudreach as fc

    try:
        ing = fc.Ingester("<customers_map>")
        rsl = ing.load_from_df("customer", <data_frame>)
        
        print(rsl)

    except Exception as err:
        print(f"An exception raised: {err}!")
```

where:

- <`customers_map`> is the file ID from the URL of a Google's Sheets file containing the mapping between a customer and its report file ID.
</br>

    *Example:*
    </br>
    *The file ID to pickup from the file URL*
    ![ID from URL](docs/url-img.png)
    and then:
    ```python
        ing = fc.Ingester("1FE0KDANyCLk_zhyxCsIGPR4ifaktD9xMt...")
    ```
    The mapping file format:
    ![cstumer map sample](docs/cst-map.jpeg)
    
    **IMPORTANT !!!**
    The customer mapping tab sheet MUST be named <`Map`>!


- <`customer`> is one of customer name or customer id (as string) as it is used in the mapping file described above.

- <`data_frame`> - is pandas Data Frame with the data to be uploaded in the customers report sheet.

----

example-2:
1. Install the library

```python
    pip install fore_cloudreach

    # on Jupyter notebook:
    ! pip install fore_cloudreach
```

2. Import and usage

```python
    
    import fore_cloudreach as fc

    # ... Acquire the customer's reports data into pandas Data Frame or CSV file
    #        
    # ... create an Ingester object by next statement
    # where `mapping_file_id` is the unique file ID from the URL of the Google Sheets file. This must be a configuration file that maps 
    # the customers to their Google Sheets report file per each customer.

    ing = fc.Ingester(mapping_file_id="1fL3rZDj8tCP4povb3E2x_WmkqNmfEZIR...")

    # to load the report from pandas DF run the following code, where you need:
    # the customer name (str) and the data set as pandas Data Frame
    rsl = ing.load_report(customer="<customer_name>", data=df)

    # to load the report from CSV file run the following code, where you need:
    # the customer name (str) and the data = string as relative path to the CSV file     
    rsl2 = ing.load_report(customer="<customer_name>", data="docs/samples/aws_ec2_rightsizing.Csv")

    # the returned result will show a summary of a successful import
```

* Switch ON/OFF extended debug logging:
    When import the FORE package - there is global variable `debug_mode` that controls the extended logging feature.
    Set that variable to `True` by the following function:
    
    ```python
    switch_debug_mode(True)
    
    # see the current debug mode value:
    print(f"debug logging mode is: {debug_mode}")
    ```

* Force `pip` to re-install a specific version of the package:
    ```bash
        pip install --force-reinstall -v "fore_cloudreach==v0.0.3.dev17"
    ```
