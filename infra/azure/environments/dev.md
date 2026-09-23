# Deployed environment: dev (resource group `aidoc-demo-rg`, Australia East)

Deployed by the product owner from the portal on 2026-09-23 using
`infra/azure/main.json`. Addresses only; keys live in the vault.

| Output | Value |
| --- | --- |
| API | https://aidocdev-api.happywater-ef7f200a.australiaeast.azurecontainerapps.io |
| Web | https://aidocdev-web.happywater-ef7f200a.australiaeast.azurecontainerapps.io |
| Key Vault | `aidocdev-kv-uxajkgagntjt` |
| Speech endpoint | https://aidocdev-speech-uxajkgagntjtk.cognitiveservices.azure.com/ |
| Azure OpenAI endpoint | https://aidocdev-openai-uxajkgagntjtk.openai.azure.com/ |
| OpenAI deployment name | `persona` (gpt-4o) |
| Speech region | `australiaeast` |

Secrets in the vault: `azure-openai-key`, `azure-speech-key`, `content-safety-key`,
`acs-connection-string`, and `demo-transfer-number` once supplied.

The two container apps run placeholder images until continuous deployment is
switched on (see `../README.md`, "Putting Dr Sam on the deployed apps").
