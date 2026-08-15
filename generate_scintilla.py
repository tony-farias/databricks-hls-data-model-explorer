#!/usr/bin/env python3
"""Generate the seven Walmart Scintilla Cloud Feeds models from UC metadata."""

import json
import subprocess
from pathlib import Path


PROFILE = "fe-vm-cpg-bricks"
WAREHOUSE_ID = "c434d5722052b51b"
CATALOG = "cpg_bricks_catalog"
SCHEMA = "scintilla_us_cloudfeeds"
OUTPUT = Path(__file__).parent / "static" / "data.js"
START = "// BEGIN GENERATED SCINTILLA MODELS"
END = "// END GENERATED SCINTILLA MODELS"

MODELS = [
    {
        "const": "SCINTILLA_SALES_DEMAND",
        "domain": "Sales & Demand",
        "blurb": "Store, omni-channel and UPC sales with returns and the Walmart merchandising calendar for item, store, channel and period performance analysis.",
        "tables": ["store_sales", "omni_sales", "upc_sales", "store_customer_return", "calendar_dim", "item_dim", "store_dim"],
        "edges": [
            ("item_dim", "store_sales", "wm_item_nbr"), ("store_dim", "store_sales", "store_nbr"),
            ("item_dim", "omni_sales", "wm_item_nbr"), ("store_dim", "omni_sales", "store_nbr"),
            ("store_dim", "upc_sales", "store_nbr"), ("item_dim", "store_customer_return", "wm_item_nbr"),
            ("store_dim", "store_customer_return", "store_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_INVENTORY",
        "domain": "Inventory & Availability",
        "blurb": "Store, hourly and distribution-center inventory, adjustments and out-of-stock root causes for availability, weeks-of-supply and lost-sales analysis.",
        "tables": ["store_invt", "hourly_store_invt", "dc_invt", "oos_root_cause", "invt_adj", "bkrm_adj", "item_dim", "store_dim", "dc_dim"],
        "edges": [
            ("item_dim", "store_invt", "wm_item_nbr"), ("store_dim", "store_invt", "store_nbr"),
            ("store_dim", "hourly_store_invt", "store_nbr"), ("item_dim", "dc_invt", "wm_item_nbr"),
            ("dc_dim", "dc_invt", "dc_nbr"), ("item_dim", "oos_root_cause", "wm_item_nbr"),
            ("store_dim", "oos_root_cause", "store_nbr"), ("item_dim", "invt_adj", "wm_item_nbr"),
            ("store_dim", "invt_adj", "store_nbr"), ("item_dim", "bkrm_adj", "wm_item_nbr"),
            ("store_dim", "bkrm_adj", "store_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_ASSORTMENT",
        "domain": "Item, Store & Assortment",
        "blurb": "Item and product attributes connected to store traits, modular plans and UPC placements for assortment coverage and modular execution analysis.",
        "tables": ["item_dim", "prod_dim", "omni_item_dim", "store_dim", "store_modular", "modular_plan", "modular_plan_upc", "modular_trait", "modular_upc_loc", "item_trait", "store_trait", "traits", "upc_attr", "upc_custom_attr", "future_valid_item"],
        "edges": [
            ("item_dim", "item_trait", "wm_item_nbr"), ("store_dim", "store_trait", "store_nbr"),
            ("traits", "item_trait", "trait_nbr"), ("traits", "store_trait", "trait_nbr"),
            ("modular_plan", "modular_plan_upc", "modular_plan_id"), ("modular_plan", "modular_trait", "modular_plan_id"),
            ("modular_plan", "modular_upc_loc", "modular_plan_id"), ("store_dim", "store_modular", "store_nbr"),
            ("item_dim", "future_valid_item", "wm_item_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_SUPPLY_CHAIN",
        "domain": "Supply Chain & Replenishment",
        "blurb": "Purchase orders, destinations, DC receipts, transfers, alignment and OTIF measures for supplier service-level and replenishment analysis.",
        "tables": ["purchase_order", "po_line", "po_line_destination", "po_alloc_order", "po_dc_receiver", "po_dc_receiver_line", "po_stock_transfer", "po_stk_trnsfr_xref", "dc_alignment", "dc_dim", "item_dim", "store_dim", "omni_otif", "mtr", "store_returns"],
        "edges": [
            ("purchase_order", "po_line", "oms_po_nbr"), ("po_line", "po_line_destination", "oms_po_nbr"),
            ("purchase_order", "po_dc_receiver", "oms_po_nbr"), ("po_dc_receiver", "po_dc_receiver_line", "rcvr_nbr"),
            ("item_dim", "po_line", "wm_item_nbr"), ("dc_dim", "po_dc_receiver", "dc_nbr"),
            ("purchase_order", "omni_otif", "oms_po_nbr"), ("item_dim", "omni_otif", "wm_item_nbr"),
            ("dc_dim", "omni_otif", "dc_nbr"), ("dc_dim", "dc_alignment", "dc_nbr"),
            ("store_dim", "dc_alignment", "store_nbr"), ("po_stock_transfer", "po_stk_trnsfr_xref", "sto_nbr"),
            ("item_dim", "mtr", "wm_item_nbr"), ("store_dim", "mtr", "store_nbr"),
            ("item_dim", "store_returns", "wm_item_nbr"), ("store_dim", "store_returns", "store_nbr"),
            ("dc_dim", "store_returns", "dc_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_FORECASTING",
        "domain": "Forecasting",
        "blurb": "Daily, weekly long-range and order forecasts tied to item and store dimensions for forecast accuracy, bias and forward order planning.",
        "tables": ["dly_dmnd_fcst", "store_demand_forecast", "order_demand_forecast", "item_dim", "store_dim", "calendar_dim", "store_sales"],
        "edges": [
            ("item_dim", "dly_dmnd_fcst", "wm_item_nbr"), ("store_dim", "dly_dmnd_fcst", "store_nbr"),
            ("item_dim", "store_demand_forecast", "wm_item_nbr"), ("store_dim", "store_demand_forecast", "store_nbr"),
            ("item_dim", "order_demand_forecast", "wm_item_nbr"), ("item_dim", "store_sales", "wm_item_nbr"),
            ("store_dim", "store_sales", "store_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_ECOMMERCE",
        "domain": "E-commerce & Omnichannel",
        "blurb": "E-commerce inventory, instock, transactability, product content, fulfillment and returns for digital shelf and omnichannel performance analysis.",
        "tables": ["ecom_invt", "ecom_instock_pct", "fc_ecom_instock_pct", "digital_transactability", "ecom_prod_cntnt_score", "ecom_returns", "store_fulfillment", "hourly_store_fulfillment", "omni_sales", "kit_sales", "prod_dim", "omni_item_dim", "dc_dim", "store_dim"],
        "edges": [
            ("prod_dim", "ecom_invt", "catlg_item_id"), ("dc_dim", "ecom_invt", "fc_id"),
            ("prod_dim", "digital_transactability", "catlg_item_id"), ("prod_dim", "ecom_prod_cntnt_score", "catlg_item_id"),
            ("prod_dim", "ecom_returns", "catlg_item_id"), ("store_dim", "store_fulfillment", "store_nbr"),
            ("store_dim", "hourly_store_fulfillment", "store_nbr"),
        ],
    },
    {
        "const": "SCINTILLA_PRICING_FUNDING",
        "domain": "Pricing & Funding",
        "blurb": "Store-item markups and markdowns combined with cooperative trade and advertising funds for price-action and investment-effectiveness analysis.",
        "tables": ["sku_mumd", "coops", "item_dim", "store_dim", "calendar_dim", "store_sales"],
        "edges": [
            ("item_dim", "sku_mumd", "wm_item_nbr"), ("store_dim", "sku_mumd", "store_nbr"),
            ("item_dim", "store_sales", "wm_item_nbr"), ("store_dim", "store_sales", "store_nbr"),
        ],
    },
]


def query_columns():
    names = sorted({table for model in MODELS for table in model["tables"]})
    quoted = ",".join("'" + name + "'" for name in names)
    statement = (
        "SELECT table_name, column_name, data_type, ordinal_position "
        f"FROM {CATALOG}.information_schema.columns "
        f"WHERE table_schema = '{SCHEMA}' AND table_name IN ({quoted}) "
        "ORDER BY table_name, ordinal_position"
    )
    payload = json.dumps({"statement": statement, "warehouse_id": WAREHOUSE_ID, "format": "JSON_ARRAY", "wait_timeout": "50s"})
    result = subprocess.run(
        ["databricks", "api", "post", "/api/2.0/sql/statements/", f"--json={payload}", f"--profile={PROFILE}"],
        check=True, capture_output=True, text=True,
    )
    response = json.loads(result.stdout)
    if response.get("status", {}).get("state") != "SUCCEEDED":
        raise RuntimeError(response)
    columns = {}
    for table, column, data_type, _ in response["result"]["data_array"]:
        columns.setdefault(table, []).append((column, data_type.lower()))
    missing = sorted(set(names) - set(columns))
    if missing:
        raise RuntimeError(f"Missing tables: {', '.join(missing)}")
    return columns


def mermaid_type(data_type):
    if any(x in data_type for x in ("int", "decimal", "double", "float")):
        return "number"
    if "date" in data_type or "time" in data_type:
        return "date"
    if "bool" in data_type:
        return "boolean"
    return "string"


def select_columns(table, columns, edge_columns):
    preferred = []
    tokens = ("_id", "_nbr", "_dt", "_wk", "sales", "qty", "amt", "pct", "cost", "invt", "fcst", "status", "desc")
    for column, data_type in columns[table]:
        if column in edge_columns or any(token in column for token in tokens):
            preferred.append((column, data_type))
    for entry in columns[table]:
        if entry not in preferred:
            preferred.append(entry)
    return preferred[:6]


def build_model(spec, columns):
    valid_edges = []
    for parent, child, column in spec["edges"]:
        parent_columns = {c for c, _ in columns[parent]}
        child_columns = {c for c, _ in columns[child]}
        if column in parent_columns and column in child_columns:
            valid_edges.append((parent, child, column))
    edge_columns = {table: set() for table in spec["tables"]}
    for parent, child, column in valid_edges:
        edge_columns[parent].add(column)
        edge_columns[child].add(column)
    lines = ["erDiagram"]
    for parent, child, column in valid_edges:
        lines.append(f'  {parent} ||--o{{ {child} : "{column}"')
    for table in spec["tables"]:
        lines.append(f"  {table} {{")
        chosen = select_columns(table, columns, edge_columns[table])
        for column, data_type in chosen:
            suffix = " FK" if column in edge_columns[table] and any(child == table for _, child, col in valid_edges if col == column) else ""
            lines.append(f"    {mermaid_type(data_type)} {column}{suffix}")
        if len(columns[table]) > len(chosen):
            lines.append(f'    string note "{len(columns[table])} columns total"')
        lines.append("  }")
    domain = {
        "name": spec["domain"], "blurb": spec["blurb"], "tables": spec["tables"],
        "ghosts": [], "edges": len(valid_edges), "mermaid": "\n".join(lines),
    }
    tables = {table: {"cols": len(columns[table]), "domain": spec["domain"]} for table in spec["tables"]}
    return {"domains": [domain], "tables": tables, "hubRefs": {}, "totals": {"tables": len(tables), "edges": len(valid_edges)}}


def main():
    columns = query_columns()
    generated = [START]
    for spec in MODELS:
        generated.append(f"const {spec['const']} = {json.dumps(build_model(spec, columns), separators=(',', ':'))};")
    generated.append(END)
    block = "\n".join(generated) + "\n"
    current = OUTPUT.read_text()
    if START in current:
        before, rest = current.split(START, 1)
        _, after = rest.split(END, 1)
        current = before.rstrip() + "\n" + block + after.lstrip("\n")
    else:
        current = current.rstrip() + "\n\n" + block
    OUTPUT.write_text(current)
    print(f"Generated {len(MODELS)} Scintilla models from {len(columns)} UC tables")


if __name__ == "__main__":
    main()
