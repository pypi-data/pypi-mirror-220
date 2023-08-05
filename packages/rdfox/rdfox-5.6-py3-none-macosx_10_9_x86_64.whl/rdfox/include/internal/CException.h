// Copyright 2021 by Oxford Semantic Technologies Limited.

CRDFOX const CException* CException_duplicate(const CException* sourceException, CException** resultException);

CRDFOX void CException_destroy(CException* exception);

CRDFOX const char* CException_what(const CException* exception);

CRDFOX bool CException_isRDFoxException(const CException* exception);

CRDFOX const char* CException_getExceptionName(const CException* exception);

CRDFOX const char* CRDFoxException_getMessage(const CException* exception);

CRDFOX size_t CRDFoxException_getNumberOfCauses(const CException* exception);

CRDFOX const CException* CRDFoxException_getCause(const CException* exception, size_t causeIndex);
