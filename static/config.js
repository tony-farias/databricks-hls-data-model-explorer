// Customer configuration. No credentials belong in this file.
// workspaceUrl is the URL users open in their browser, for example:
// https://my-workspace.cloud.databricks.com
window.HLS_DATA_MODEL_CONFIG = {
  workspaceUrl: "https://YOUR-WORKSPACE.cloud.databricks.com",
  // Optional. Usually needed only for multi-workspace hosts.
  orgId: "",
  models: {
    commercial: { catalog: "main", schema: "commercial_crm" },
    safety: { catalog: "main", schema: "pharmacovigilance" },
    quality: { catalog: "main", schema: "quality_qms" },
    clinical: { catalog: "main", schema: "clinical_ctms" },
    netsuite: { catalog: "main", schema: "netsuite" },

    // Optional domain-to-Genie mappings. Example:
    // safety: {
    //   catalog: "main",
    //   schema: "pharmacovigilance",
    //   genieByDomain: {
    //     "Case Processing": "https://YOUR-WORKSPACE/genie/rooms/YOUR-SPACE-ID"
    //   }
    // }
  }
};
