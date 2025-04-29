## Frontend

- **Build Config**
  - **Name:** `gwells-frontend`
  - **File Name:** `frontendBuildConfig.yaml`
  - **Repo File Path:** `GWELLS/openshift/frontendBuildConfig.yaml`

- **Deploy Config**
  - **Name:** `gwells-frontend`
  - **File Names:**  
    - `frontendDeployConfigDev.yaml`  
    - `frontendDeployConfigTest.yaml`  
    - `frontendDeployConfigProd.yaml`
  - **Repo File Path:** `GWELLS/openshift/`

- **Name in Namespace:** `gwells-application`  
- **ImageStream Name:** `gwells-application`

---

## Backend

- **Build Config**
  - **Name:** `gwells-backend`
  - **File Name:** `backendBuildConfig.yaml`
  - **Repo File Path:** `GWELLS/openshift/backendBuildConfig.yaml`

- **Deploy Config**
  - **Name:** `gwells-backend`
  - **File Names:**  
    - `backendDeployConfigDev.yaml`  
    - `backendDeployConfigTest.yaml`  
    - `backendDeployConfigProd.yaml`
  - **Repo File Path:** `GWELLS/openshift/`

- **Name in Namespace:** `gwells-backend`  
- **ImageStream Name:** `gwells-backend`

---

## Database

- **Deploy Config**
  - **Name:** `gwells-pg12-development`
  - **File Names:**  
    - `databaseDeployConfigDev.yaml`  
    - `databaseDeployConfigTest.yaml`
  - **Repo File Path:** `GWELLS/openshift/`

- **Name in Namespace:** `gwells-pg12-development`