#!/usr/bin/env bash
# Assuming only_uuids.json looks like: ["file1","file2",...]
ids=( $(jq -r '.[]' only_uuids.json) )

GDC_CLIENT="$/gdc-client" #path to gdc-client

"$GDC_CLIENT" download "${ids[@]}" --config my-dtt-config.dtt #config file to specify download location
