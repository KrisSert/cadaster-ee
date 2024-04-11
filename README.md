
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


Sourcing:
Python


Docker

Terraform as IaaC

dbt

Mage

-- 

Google Cloud servers

Google Cloud SQL (PostgreSQL)

Google Data Studio 




1. clone the project in your desider machine, or VM instance: 
	- git clone *.git

2. Create service account and api key for terraform in GCS.
	- download the JSON and place the value to /terraform/keys/gcs_terraform_api_key.json"

3. To create GCS infrastructure, in path "terraform" run:
	- terraform init 
	- terraform plan  (to_be_created: 1 bucket, 1 bigquery dataset, 1 service account key)
	- terraform apply
