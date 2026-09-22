// AI DOC - Azure resources for the Dr Sam history-taking agent.
// Australia East. Adds to the MedExec Coach base (Container Apps, ACR, PostgreSQL,
// storage, Log Analytics): Azure OpenAI, Azure AI Speech, Azure AI Content Safety,
// Key Vault with a user-assigned identity, and blob containers.
//
// Deploy: az deployment group create -g <rg> -f infra/azure/main.bicep -p infra/azure/main.bicepparam
targetScope = 'resourceGroup'

@minLength(3)
@maxLength(12)
param namePrefix string = 'aidoc'
param environmentName string = 'dev'
param location string = 'australiaeast'

@description('Azure OpenAI model deployments for the persona and tone prompts.')
param openAiModelName string = 'gpt-4o'
param openAiModelVersion string = '2024-11-20'
param openAiCapacity int = 30

@description('Container image for the API; a placeholder until the deploy workflow pushes one.')
param backendImage string = 'mcr.microsoft.com/k8se/quickstart:latest'
param frontendImage string = 'mcr.microsoft.com/k8se/quickstart:latest'

var suffix = toLower('${namePrefix}${environmentName}')
var uniq = uniqueString(resourceGroup().id, suffix)
var storageName = toLower(take(replace('${suffix}st${uniq}', '-', ''), 24))
var kvName = take('${suffix}-kv-${uniq}', 24)

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: '${suffix}-logs'
  location: location
  properties: { sku: { name: 'PerGB2018' }, retentionInDays: 30 }
}

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: '${suffix}-id'
  location: location
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: kvName
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 30
  }
}

// Key Vault Secrets User for the container apps' identity
resource kvRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, identity.id, '4633458b-17de-408a-b874-0445c86b69e6')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '4633458b-17de-408a-b874-0445c86b69e6')
    principalId: identity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource openAi 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${suffix}-openai-${uniq}'
  location: location
  kind: 'OpenAI'
  sku: { name: 'S0' }
  properties: { customSubDomainName: '${suffix}-openai-${uniq}', publicNetworkAccess: 'Enabled' }
}

resource openAiPersona 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openAi
  name: 'persona'
  sku: { name: 'Standard', capacity: openAiCapacity }
  properties: { model: { format: 'OpenAI', name: openAiModelName, version: openAiModelVersion } }
}

resource speech 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${suffix}-speech-${uniq}'
  location: location
  kind: 'SpeechServices'
  sku: { name: 'S0' }
  properties: { customSubDomainName: '${suffix}-speech-${uniq}' }
}

resource contentSafety 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${suffix}-safety-${uniq}'
  location: location
  kind: 'ContentSafety'
  sku: { name: 'S0' }
  properties: { customSubDomainName: '${suffix}-safety-${uniq}' }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageName
  location: location
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: { minimumTlsVersion: 'TLS1_2', allowBlobPublicAccess: false }
}

resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2023-05-01' = {
  parent: storage
  name: 'default'
}

resource audioCache 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobServices
  name: 'audio-cache'
}

resource handovers 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  parent: blobServices
  name: 'handovers'
}

// Secrets: keys are written to Key Vault here so the apps never see them in Bicep params.
resource secretOpenAi 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-openai-key'
  properties: { value: openAi.listKeys().key1 }
}
resource secretSpeech 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'azure-speech-key'
  properties: { value: speech.listKeys().key1 }
}
resource secretSafety 'Microsoft.KeyVault/vaults/secrets@2023-07-01' = {
  parent: keyVault
  name: 'content-safety-key'
  properties: { value: contentSafety.listKeys().key1 }
}

resource containerEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: '${suffix}-env'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: { customerId: logAnalytics.properties.customerId, sharedKey: logAnalytics.listKeys().primarySharedKey }
    }
  }
}

resource api 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${suffix}-api'
  location: location
  identity: { type: 'UserAssigned', userAssignedIdentities: { '${identity.id}': {} } }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: { external: true, targetPort: 8000 }
      secrets: [
        { name: 'azure-openai-key', keyVaultUrl: secretOpenAi.properties.secretUri, identity: identity.id }
        { name: 'azure-speech-key', keyVaultUrl: secretSpeech.properties.secretUri, identity: identity.id }
        { name: 'content-safety-key', keyVaultUrl: secretSafety.properties.secretUri, identity: identity.id }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: backendImage
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: [
            { name: 'MODEL_PROVIDER', value: 'azure_openai' }
            { name: 'AZURE_OPENAI_ENDPOINT', value: openAi.properties.endpoint }
            { name: 'AZURE_OPENAI_DEPLOYMENT_PERSONA', value: openAiPersona.name }
            { name: 'AZURE_OPENAI_KEY', secretRef: 'azure-openai-key' }
            { name: 'TTS_PROVIDER', value: 'azure_rest' }
            { name: 'AZURE_SPEECH_REGION', value: location }
            { name: 'AZURE_SPEECH_KEY', secretRef: 'azure-speech-key' }
            { name: 'CONTENT_SAFETY_PROVIDER', value: 'azure' }
            { name: 'CONTENT_SAFETY_ENDPOINT', value: contentSafety.properties.endpoint }
            { name: 'CONTENT_SAFETY_KEY', secretRef: 'content-safety-key' }
            { name: 'PARAMETERS_DEPLOYMENT', value: 'sa_health_regional' }
          ]
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 3 }
    }
  }
}

resource web 'Microsoft.App/containerApps@2024-03-01' = {
  name: '${suffix}-web'
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: { ingress: { external: true, targetPort: 80 } }
    template: {
      containers: [
        { name: 'web', image: frontendImage, resources: { cpu: json('0.25'), memory: '0.5Gi' }, env: [ { name: 'API_BASE_URL', value: 'https://${api.properties.configuration.ingress.fqdn}' } ] }
      ]
      scale: { minReplicas: 1, maxReplicas: 2 }
    }
  }
}

output apiUrl string = 'https://${api.properties.configuration.ingress.fqdn}'
output webUrl string = 'https://${web.properties.configuration.ingress.fqdn}'
output keyVaultName string = keyVault.name
output speechEndpoint string = speech.properties.endpoint
output openAiEndpoint string = openAi.properties.endpoint
