// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX void CCursor_destroy(CCursor* cursor);

CRDFOX const CException* CCursor_getDataStoreConnection(CCursor* cursor, CDataStoreConnection** dataStoreConnection);

CRDFOX const CException* CCursor_getArgumentsBuffer(CCursor* cursor, const CResourceID** argumentsBuffer);

CRDFOX const CException* CCursor_isAskQuery(CCursor* cursor, bool* isAskQuery);

CRDFOX const CException* CCursor_getArity(CCursor* cursor, size_t* arity);

CRDFOX const CException* CCursor_getAnswerVariableName(CCursor* cursor, size_t variableIndex, const char** answerVariableName);

CRDFOX const CException* CCursor_getArgumentIndexes(CCursor* cursor, const CArgumentIndex** argumentIndexes);

CRDFOX const CException* CCursor_open(CCursor* cursor, size_t* multiplicity);

CRDFOX const CException* CCursor_canAdvance(CCursor* cursor, bool* canAdvance);

CRDFOX const CException* CCursor_advance(CCursor* cursor, size_t* multiplicity);

CRDFOX const CException* CCursor_stop(CCursor* cursor);

CRDFOX const CException* CCursor_getResourceValue(CCursor* cursor, const CResourceID resourceID, const byte_t** data, size_t* dataSize, const byte_t** prefixData, size_t* prefixDataSize, CDatatypeID* datatypeID, bool* resourceResolved);

CRDFOX const CException* CCursor_getResourceLexicalForm(CCursor* cursor, const CResourceID resourceID, char* buffer, size_t bufferSize, size_t* lexicalFormSize, CDatatypeID* datatypeID, bool* resourceResolved);

CRDFOX const CException* CCursor_getResourceTurtleLiteral(CCursor* cursor, const CResourceID resourceID, const CPrefixes* prefixes, char* buffer, size_t bufferSize, size_t* turtleLiteralSize, CDatatypeID* datatypeID, bool* resourceResolved);
