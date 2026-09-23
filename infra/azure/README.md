# Deploying to Azure

Everything Dr Sam needs in Azure is one Bicep template. You do not need to
install anything: Azure Cloud Shell in the portal has the Azure CLI, Bicep and
git already signed in as you.

## Step by step, first time

1. Sign in at https://portal.azure.com with the account that owns the
   subscription (or has Contributor on it).
2. Click the Cloud Shell icon in the top bar (the `>_` terminal symbol, left of
   the notifications bell). Choose **Bash** if asked. The first time, it asks
   to create a small storage account for the shell; accept the defaults.
3. In the shell, get the code and run the deployment:

   ```bash
   git clone https://github.com/sluckyy/AI_DOC.git
   cd AI_DOC
   git checkout feature/phase-1-vertical-slice
   ./infra/azure/deploy.sh aidoc-demo-rg
   ```

   The first argument is the name of a new resource group; choose any name.
   The run takes about ten minutes. It prints the API and web URLs, the Key
   Vault name and the Speech and OpenAI endpoints. It never prints a key.

4. For the live transfer, set the demo number in the shell before running,
   so it goes straight into Key Vault:

   ```bash
   export DEMO_TRANSFER_NUMBER=+614xxxxxxxx
   ./infra/azure/deploy.sh aidoc-demo-rg
   ```

   Re-running the script is safe; it updates what changed.

## No terminal: the portal form instead

The same template can be deployed from a portal form, with drop-downs. Do not
use **Import From GitHub** or **Web App**: those wizards deploy one app onto App
Service and cannot create the AI services. Use the custom template deployment:

1. Download `infra/azure/main.json` from GitHub (open the file, then **Download
   raw file**). It is the compiled copy of `main.bicep`; regenerate it with
   `bicep build main.bicep` after any change.
2. In the portal search box type **Deploy a custom template** and open it.
3. Choose **Build your own template in the editor**, then **Load file** and
   pick `main.json`. Click **Save**.
4. Fill the form: Subscription; Resource group **Create new** (for example
   `aidoc-demo-rg`); Region **Australia East**. Leave the other parameters as
   they are; `demoTransferNumber` can be set now or later.
5. **Review + create**, then **Create**. About ten minutes.

If the Subscription drop-down is empty, the account has no subscription yet.
Search **Subscriptions** in the portal and add one (free trial or pay as you
go), or ask whoever owns the organisation's Azure to add you as Contributor on
theirs. Nothing can be created without one.

## What the template creates, all in Australia East

| Resource | Used for |
| --- | --- |
| Azure OpenAI with a gpt-4o deployment | Slot extraction and re-wording |
| Azure AI Speech | Dr Sam's voice, later real-time recognition |
| Azure AI Content Safety | Screens every spoken turn |
| Azure Communication Services | Live transfer to the duty GP |
| Key Vault and a managed identity | Holds every key; the apps read them at start |
| Storage account | Audio cache and handover exports |
| Log Analytics | Container logs |
| Container Apps environment with the API and the web app | Runs the service |

## Three things the template cannot do

- **OpenAI quota.** A subscription that has never used Azure OpenAI in
  Australia East may need quota requested once; the deployment says so and can
  be re-run after approval.
- **A phone number.** Australian PSTN numbers are bought inside the
  Communication Services resource in the portal, after the subscription is
  verified for calling. Until then the transfer panel shows the configured
  number and a call button instead of dialling.
- **Container images.** The apps run from placeholder images until a container
  registry and a build step are added. Running the API and web app locally with
  the Azure keys in `backend/.env` is the intended path for the demo.

## Running locally against the deployed services

Open the Key Vault in the portal, read the secrets you need, and put them in
`backend/.env` on the demo laptop (copy `backend/.env.example` first). Anything
left blank falls back to its fake, so a partial set still runs.
