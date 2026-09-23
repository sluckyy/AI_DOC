#!/usr/bin/env bash
# Deploys AI DOC's Azure resources with one command. Run it in Azure Cloud Shell
# (portal.azure.com, the terminal icon in the top bar, Bash) or anywhere the
# Azure CLI is signed in. It never prints a key: every secret goes into Key Vault
# and the container apps read it by managed identity.
#
#   ./infra/azure/deploy.sh <resource-group> [environment-name]
#
# Optional environment variables, set before running (never commit them):
#   DEMO_TRANSFER_NUMBER   the mobile the live transfer rings for the demo, E.164 (+614xxxxxxxx)
#   ACS_CALLER_ID_NUMBER   the phone number bought in the Communication Services resource
#   TELEPHONY_PROVIDER     acs once a caller id exists; fake until then (default fake)
set -euo pipefail

RG="${1:?usage: deploy.sh <resource-group> [environment-name]}"
ENV_NAME="${2:-demo}"
LOCATION="${LOCATION:-australiaeast}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Subscription: $(az account show --query name -o tsv)"
az group create --name "$RG" --location "$LOCATION" --output none
echo "Resource group $RG ready in $LOCATION"

az deployment group create \
  --resource-group "$RG" \
  --template-file "$HERE/main.bicep" \
  --parameters environmentName="$ENV_NAME" \
               telephonyProvider="${TELEPHONY_PROVIDER:-fake}" \
               acsCallerIdNumber="${ACS_CALLER_ID_NUMBER:-}" \
               demoTransferNumber="${DEMO_TRANSFER_NUMBER:-}" \
  --query "properties.outputs" -o table

cat <<'NEXT'

Deployed. What is left is done in the portal, not by this script:
  1. Azure OpenAI: if the subscription has no quota in Australia East, the gpt-4o
     deployment step fails with a quota message; request access, then re-run.
  2. Communication Services: buy one Australian phone number in the ACS resource
     (Phone numbers, Get), then re-run with ACS_CALLER_ID_NUMBER and
     TELEPHONY_PROVIDER=acs so the live transfer places real calls.
  3. Container images: the template points at placeholder images until a
     container registry is added; the API and web app run locally meanwhile.
NEXT
