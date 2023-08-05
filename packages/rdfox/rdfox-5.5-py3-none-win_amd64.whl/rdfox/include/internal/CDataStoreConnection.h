// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX void CDataStoreConnection_destroy(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_newDataStoreConnection(const char* dataStoreName, const char* roleName, const char* password, CDataStoreConnection** dataStoreConnection);

// Properties of the connection

// Operations on the connection

CRDFOX const CException* CDataStoreConnection_duplicate(CDataStoreConnection* dataStoreConnection, CDataStoreConnection** outputDataStoreConnection);

CRDFOX const CException* CDataStoreConnection_interrupt(CDataStoreConnection* dataStoreConnection);

// Connection role management

// Data store properties

CRDFOX const CException* CDataStoreConnection_getName(CDataStoreConnection* dataStoreConnection, const char** name);

CRDFOX const CException* CDataStoreConnection_getID(CDataStoreConnection* dataStoreConnection, CDataStoreID* dataStoreID);

CRDFOX const CException* CDataStoreConnection_getUniqueID(CDataStoreConnection* dataStoreConnection, const char** uniqueID);

CRDFOX const CException* CDataStoreConnection_getDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

// Tuple table management

// Data source management

// Statistics management

// Transaction management

CRDFOX const CException* CDataStoreConnection_setNextOperationMustMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getNextOperationMustMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_setNextOperationMustNotMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getNextOperationMustNotMatchDataStoreVersion(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getDataStoreVersionAfterLastOperation(CDataStoreConnection* dataStoreConnection, size_t* dataStoreVersion);

CRDFOX const CException* CDataStoreConnection_getTransactionState(CDataStoreConnection* dataStoreConnection, CTransactionState* transactionState);

CRDFOX const CException* CDataStoreConnection_transactionRequiresRollback(CDataStoreConnection* dataStoreConnection, bool* transactionRequiresRollback);

CRDFOX const CException* CDataStoreConnection_beginTransaction(CDataStoreConnection* dataStoreConnection, CTransactionType transactionType);

CRDFOX const CException* CDataStoreConnection_commitTransaction(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_rollbackTransaction(CDataStoreConnection* dataStoreConnection);

// Various operations on the data store

CRDFOX const CException* CDataStoreConnection_clear(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_clearFactsKeepRulesAxioms(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_clearRulesAxiomsExplicateFacts(CDataStoreConnection* dataStoreConnection);

CRDFOX const CException* CDataStoreConnection_compact(CDataStoreConnection* dataStoreConnection);

// Data import/export

CRDFOX const CException* CDataStoreConnection_exportData(CDataStoreConnection* dataStoreConnection, const CPrefixes* prefixes, const COutputStream* outputStream, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_exportDataToBuffer(CDataStoreConnection* dataStoreConnection, const CPrefixes* prefixes, char* buffer, size_t bufferSize, size_t* resultSize, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_exportDataToFile(CDataStoreConnection* dataStoreConnection, const CPrefixes* prefixes, const char* fileName, const char* formatName, const CParameters* parameters);

CRDFOX const CException* CDataStoreConnection_importData(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, CPrefixes* prefixes, const CInputStream* inputStream, const char* baseIRI, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromBuffer(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, CPrefixes* prefixes, const byte_t* buffer, size_t bufferLength, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromFile(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, CPrefixes* prefixes, const char* fileName, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importDataFromURI(CDataStoreConnection* dataStoreConnection, const char* defaultGraphName, CUpdateType updateType, CPrefixes* prefixes, const char* uri, const char* formatName);

CRDFOX const CException* CDataStoreConnection_importAxiomsFromTriples(CDataStoreConnection* dataStoreConnection, const char* sourceGraphName, bool translateAssertions, const char* destinationGraphName, CUpdateType updateType);

// Management of the axioms

// Management of the rules

// Management of the materialization

// Explanation

// Query & update evaluation

CRDFOX const CException* CDataStoreConnection_createCursor(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, CCursor** cursor);

CRDFOX const CException* CDataStoreConnection_evaluateQuery(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, const COutputStream* outputStream, const char* queryAnswerFormatName, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateQueryToBuffer(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, char* buffer, size_t bufferSize, size_t* resultSize, const char* queryAnswerFormatName, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateQueryToFile(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* queryText, const size_t queryTextLength, const CParameters* compilationParameters, const char* fileName, const char* queryAnswerFormatName, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateUpdate(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* updateText, const size_t updateTextLength, const CParameters* compilationParameters, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatement(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, const COutputStream* outputStream, const char* queryAnswerFormatName, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatementToBuffer(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, char* buffer, size_t bufferSize, size_t* resultSize, const char* queryAnswerFormatName, CStatementResult statementResult);

CRDFOX const CException* CDataStoreConnection_evaluateStatementToFile(CDataStoreConnection* dataStoreConnection, const char* baseIRI, CPrefixes* prefixes, const char* statementText, size_t statementTextLength, const CParameters* compilationParameters, const char* fileName, const char* queryAnswerFormatName, CStatementResult statementResult);

// Dictionary functions

CRDFOX const CException* CDataStoreConnection_getDictionaryVersion(CDataStoreConnection* dataStoreConnection, size_t* dictionaryVersion);

CRDFOX const CException* CDataStoreConnection_getDatatypeID(CDataStoreConnection* dataStoreConnection, CResourceID resourceID, CDatatypeID* datatypeID);

CRDFOX const CException* CDataStoreConnection_getResourceValue(CDataStoreConnection* dataStoreConnection, CResourceID resourceID, const byte_t** data, size_t* dataSize, const byte_t** prefixData, size_t* prefixDataSize, CDatatypeID* datatypeID, bool* resourceResolved);

CRDFOX const CException* CDataStoreConnection_getResourceLexicalForm(CDataStoreConnection* dataStoreConnection, CResourceID resourceID, char* buffer, size_t bufferSize, size_t* lexicalFormSize, CDatatypeID* datatypeID, bool* resourceResolved);

CRDFOX const CException* CDataStoreConnection_getResourceTurtleLiteral(CDataStoreConnection* dataStoreConnection, CResourceID resourceID, const CPrefixes* prefixes, char* buffer, size_t bufferSize, size_t* turtleLiteralSize, CDatatypeID* datatypeID, bool* resourceResolved);

// Saving to binary format
