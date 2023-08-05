// Copyright 2021 by Oxford Semantic Technologies Limited.

#ifndef CRDFOX_H_
#define CRDFOX_H_

#include <inttypes.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

#ifdef _WIN64
    #ifdef CRDFOX_EXPORT
        #define CRDFOX __declspec(dllexport)
    #else
        #define CRDFOX __declspec(dllimport)
    #endif
#else
    #define CRDFOX
#endif

typedef uint8_t byte_t;
typedef uint32_t CDataStoreID;
typedef uint8_t CDatatypeID;
typedef uint32_t CArgumentIndex;
typedef uint64_t CResourceID;

extern const char* const GUESS_FORMAT_NAME;

typedef enum { UPDATE_TYPE_ADDITION = 0, UPDATE_TYPE_DELETION = 11 } CUpdateType;

typedef enum { TRANSACTION_TYPE_READ_ONLY, TRANSACTION_TYPE_READ_WRITE } CTransactionType;

typedef enum { TRANSACTION_STATE_NONE, TRANSACTION_STATE_READ_ONLY, TRANSACTION_STATE_READ_WRITE } CTransactionState;

typedef size_t CStatementResult[2];

typedef struct {
    unsigned char __dummy;
} CException;

typedef struct {
    unsigned char __dummy;
} CPrefixes;

typedef struct {
    unsigned char __dummy;
} CParameters;

typedef struct {
    unsigned char __dummy;
} CServerConnection;

typedef struct {
    unsigned char __dummy;
} CDataStoreConnection;

typedef struct {
    unsigned char __dummy;
} CCursor;

typedef struct COutputStream {
    void* context;
    bool (*flushFn)(void* context);
    bool (*writeFn)(void* context, const void* data, size_t numberOfBytesToWrite);
} COutputStream;

typedef struct CInputStream {
    void* context;
    bool (*rewindFn)(void* context);
    bool (*readFn)(void* context, void* data, size_t numberOfBytesToRead, size_t* bytesRead);
} CInputStream;

extern const COutputStream* const RDFOX_STDOUT;

#include "internal/CException.h"
#include "internal/CParameters.h"
#include "internal/CPrefixes.h"
#include "internal/CServer.h"
#include "internal/CServerConnection.h"
#include "internal/CDataStoreConnection.h"
#include "internal/CCursor.h"

#ifdef __cplusplus
}

template<class T, void (*destroyer)(T*)>
class CObjectPtr {
    
protected:
    
    T* m_object;
    
    struct AddressWrapper {
        CObjectPtr<T, destroyer>* m_objectPointer;
        T* m_temporary;
        
        inline explicit AddressWrapper(CObjectPtr<T, destroyer>* const objectPointer) noexcept :
            m_objectPointer(objectPointer),
            m_temporary(objectPointer->m_object)
        {
        }
        
        AddressWrapper(const AddressWrapper& other) = delete;

        inline AddressWrapper(AddressWrapper&& other) :
            m_objectPointer(other.m_objectPointer),
            m_temporary(other.m_temporary)
        {
            other.m_objectPointer = nullptr;
            other.m_temporary = nullptr;
        }

        AddressWrapper& operator=(const AddressWrapper& other) = delete;

        AddressWrapper& operator=(AddressWrapper&& other) = delete;

        inline ~AddressWrapper() {
            if (m_objectPointer == nullptr)
                destroyer(m_temporary);
            else if (m_temporary != m_objectPointer->m_object) {
                destroyer(m_objectPointer->m_object);
                m_objectPointer->m_object = m_temporary;
            }
        }
        
        inline operator T**() && noexcept {
            return &m_temporary;
        }
        
        inline operator CObjectPtr<T, destroyer>*() const {
            return m_objectPointer;
        }

    };
    
public:
    
    inline explicit CObjectPtr(T* object = nullptr) noexcept :
        m_object(object)
    {
    }
    
    inline CObjectPtr(const CObjectPtr<T, destroyer>& other) = delete;

    inline CObjectPtr(CObjectPtr<T, destroyer>&& other) noexcept : m_object(other.m_object) {
        other.m_object = nullptr;
    }

    CObjectPtr<T, destroyer>& operator=(const CObjectPtr<T, destroyer>& other) = delete;

    inline CObjectPtr<T, destroyer>& operator=(CObjectPtr<T, destroyer>&& other) noexcept {
        if (&m_object != &other.m_object) {
            destroyer(m_object);
            m_object = other.m_object;
            other.m_object = nullptr;
        }
        return *this;
    }

    inline ~CObjectPtr() {
        destroyer(m_object);
    }
    
    inline void swap(CObjectPtr<T, destroyer>& other) noexcept {
        T* object = m_object;
        m_object = other.m_object;
        other.m_object = object;
    }
    
    inline void reset(T* const object = nullptr) noexcept {
        destroyer(m_object);
        m_object = object;
    }

    inline T* release() noexcept {
        T* object = m_object;
        m_object = nullptr;
        return object;
    }

    inline T* get() const noexcept {
        return m_object;
    }

    inline operator T*() const noexcept {
        return m_object;
    }

    inline AddressWrapper operator&() noexcept {
        return AddressWrapper(this);
    }
    
    inline explicit operator bool() const noexcept {
        return m_object != nullptr;
    }
    
};

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator==(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() == object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator!=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() != object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator<(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() < object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator<=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() <= object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator>(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() > object2.get();
}

template<class T1, void (*destroyer1)(T1*), class T2, void (*destroyer2)(T2*)>
inline bool operator>=(const CObjectPtr<T1, destroyer1>& object1, const CObjectPtr<T2, destroyer2>& object2) {
    return object1.get() >= object2.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator==(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() == nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator==(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr == object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator!=(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() != nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator!=(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr != object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator<(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() < nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator<(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr < object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator<=(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() <= nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator<=(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr <= object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator>(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() > nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator>(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr > object.get();
}

template<class T, void (*destroyer)(T*)>
inline bool operator>=(const CObjectPtr<T, destroyer>& object, nullptr_t) {
    return object.get() >= nullptr;
}

template<class T, void (*destroyer)(T*)>
inline bool operator>=(nullptr_t, const CObjectPtr<T, destroyer>& object) {
    return nullptr >= object.get();
}

namespace std {

    template<class T, void (*destroyer)(T*)>
    inline void swap(CObjectPtr<T, destroyer>& pointer1, CObjectPtr<T, destroyer>& pointer2) noexcept {
        pointer1.swap(pointer2);
    }

}

typedef CObjectPtr<CException, CException_destroy> CExceptionPtr;
typedef CObjectPtr<CPrefixes, CPrefixes_destroy> CPrefixesPtr;
typedef CObjectPtr<CParameters, CParameters_destroy> CParametersPtr;
typedef CObjectPtr<CServerConnection, CServerConnection_destroy> CServerConnectionPtr;
typedef CObjectPtr<CDataStoreConnection, CDataStoreConnection_destroy> CDataStoreConnectionPtr;
typedef CObjectPtr<CCursor, CCursor_destroy> CCursorPtr;

#endif

#endif // CRDFOX_H_
