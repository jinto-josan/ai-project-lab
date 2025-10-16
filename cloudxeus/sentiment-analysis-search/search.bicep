param searchServices_ai_search_900_name string = 'ai-search-900'

resource searchServices_ai_search_900_name_resource 'Microsoft.Search/searchServices@2025-05-01' = {
  name: searchServices_ai_search_900_name
  location: 'Central US'
  sku: {
    name: 'basic'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    endpoint: 'https://${searchServices_ai_search_900_name}.search.windows.net'
    hostingMode: 'default'
    computeType: 'Default'
    publicNetworkAccess: 'Enabled'
    networkRuleSet: {
      ipRules: []
      bypass: 'None'
    }
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
    dataExfiltrationProtections: []
    semanticSearch: 'free'
    upgradeAvailable: 'notAvailable'
  }
}
