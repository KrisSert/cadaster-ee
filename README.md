
Data engineering project to process, analyse and vizualize the Estonian cadastral data.

---

Cadastral Data (definition): 
contains official, legal documentation concerning the quantity, dimensions, location, value, tenure, and ownership of individual parcels of land.

### Architecture
<img src="https://docs.google.com/drawings/d/e/2PACX-1vThb-9tX8vTUEEsmdGTwmGnXUVBEAIbcfJQN05Pvh7o6H_755PkOtypvDnZ6aUT3jS4DTZ9QibfLp9b/pub?w=981&amp;h=391">

---

### Source loading:

Loading the .bdf source file (Mage pipeline) to Google Cloud Storage: "api_to_gcs"
Transformation within the pipeline converts the file to .csv and stores it in GCS bucket.


---------------------


Sourcing & transformation:
- Python
- Docker
- Terraform as IaaC
- BigQuery & dbt
- Mage

----------------------- 

Prerequsites:

- Enable Identity and Access Management (IAM) API in google cloud platform: 
	https://console.cloud.google.com/apis/library/iam.googleapis.com?
- Enable Cloud Resource Manager API:
	https://console.cloud.google.com/apis/api/cloudresourcemanager.googleapis.com 


1. clone the project in your desider machine, or VM instance: 
	- git clone *.git

2. Create service account and api key for terraform in GCS.
	- download the JSON and place the value to /terraform/keys/gcs_terraform_api_key.json"

3. To create GCS infrastructure (bucket, bigquery dataset, service accounts, roles):
   - navigate to path "terraform":
  
		```cd terraform```
	
   - run terraform init, plan & apply: 

		```terraform init``` 
  	
		``` terraform plan```  
		(to_be_created: 6 to add.)

		```terraform apply```

4. Create the api keys for "mage-service-account" and "dbt-service-account":
   	https://console.cloud.google.com/iam-admin/serviceaccounts

	- the mage-service-account api key should be placed in "/keys" folder in the project, and renamed to:
		"mage_service_account_key.json"
	- the dbt-service-account api key should be placed in "/keys" folder in the project, and renamed to:
		"dbt_service_account_key.json"