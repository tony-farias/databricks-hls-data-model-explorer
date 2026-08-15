# Databricks HLS Data Model Explorer

An interactive Databricks App for exploring Health and Life Sciences and Consumer Packaged Goods entity-relationship models. It includes Veeva CRM, pharmacovigilance, quality, clinical, Salesforce Health Cloud, NetSuite accounting, HEDIS, and Walmart Scintilla Cloud Feeds examples.

The application is a lightweight Flask server with a static Mermaid-based UI. It does not copy or query customer data. When configured, entity cards link users to the matching tables in Unity Catalog.

## What is included

- Interactive, searchable ER diagrams grouped by business domain
- Links from entities to Unity Catalog tables
- Optional links to AI/BI Genie spaces
- Four NetSuite SuiteAnalytics models: Revenue Recognition, Invoice with Amortization, Expense Amortization, and General Accounting
- Seven Walmart Scintilla models: Sales & Demand, Inventory & Availability, Item/Store/Assortment, Supply Chain, Forecasting, E-commerce, and Pricing/Funding
- A portable Databricks Apps deployment script

The included schemas are illustrative metadata models. Validate them against your licensed source-system metadata and your Unity Catalog schemas before production use. No credentials or customer records are included.

## Prerequisites

- A Databricks workspace with Databricks Apps enabled
- Databricks CLI 0.229 or later
- Python 3.10 or later
- Permission to create and deploy Databricks Apps and write to your Workspace user folder

Authenticate the CLI:

```bash
databricks auth login --host https://YOUR-WORKSPACE.cloud.databricks.com --profile customer-workspace
```

## Configure the catalog links

Edit [`static/config.js`](static/config.js):

```js
window.HLS_DATA_MODEL_CONFIG = {
  workspaceUrl: "https://YOUR-WORKSPACE.cloud.databricks.com",
  orgId: "",
  models: {
    commercial: { catalog: "main", schema: "commercial_crm" },
    safety: { catalog: "main", schema: "pharmacovigilance" },
    quality: { catalog: "main", schema: "quality_qms" },
    clinical: { catalog: "main", schema: "clinical_ctms" },
    netsuite: { catalog: "main", schema: "netsuite" },
    scintilla: {
      workspaceUrl: "https://fevm-cpg-bricks.cloud.databricks.com",
      orgId: "7474656551084241",
      catalog: "cpg_bricks_catalog",
      schema: "scintilla_us_cloudfeeds"
    }
  }
};
```

Catalog and schema names may contain hyphens. `orgId` can normally remain empty; set it only when your Databricks URL requires an `o` query parameter.

To connect a domain to Genie, add a `genieByDomain` object to that model. Domain names must exactly match the labels shown in the app.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:8000.

## Deploy as a Databricks App

```bash
chmod +x deploy.sh
DATABRICKS_CONFIG_PROFILE=customer-workspace \
APP_NAME=hls-data-models \
./deploy.sh
```

The script:

1. Resolves the authenticated Databricks username.
2. Uploads only runtime files to `/Workspace/Users/<user>/apps/<app-name>`.
3. Creates the Databricks App if it does not exist.
4. Deploys a snapshot and prints the app URL and state.

Override the upload location when needed:

```bash
WORKSPACE_PATH=/Workspace/Shared/apps/hls-data-models \
DATABRICKS_CONFIG_PROFILE=customer-workspace \
./deploy.sh
```

## Runtime structure

```text
app.py                    Flask entry point
app.yaml                  Databricks Apps command
requirements.txt          Python dependency
static/index.html         UI and model registry
static/data.js            ERD metadata
static/config.js          customer workspace/catalog configuration
static/genieflow-logo.png application logo
deploy.sh                 repeatable CLI deployment
```

## Security and operations

- Never store Databricks tokens in this repository or in `static/config.js`.
- Authentication to the app and workspace is handled by Databricks.
- Grant app users access to the Unity Catalog objects and Genie spaces they need.
- Re-run `deploy.sh` after changing configuration or UI files.

## License

MIT. See [`LICENSE`](LICENSE).
