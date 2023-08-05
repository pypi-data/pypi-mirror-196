#ifndef TILEDBSOMA_CARROW_H
#define TILEDBSOMA_CARROW_H
/* ************************************************************************ */
/*
 * Arrow C Data Interface
 * Apache License 2.0
 * source: https://arrow.apache.org/docs/format/CDataInterface.html
 */

#include <cinttypes>

#define ARROW_FLAG_DICTIONARY_ORDERED 1
#define ARROW_FLAG_NULLABLE 2
#define ARROW_FLAG_MAP_KEYS_SORTED 4

struct ArrowSchema {
    // Array type description
    const char* format;
    const char* name;
    const char* metadata;
    int64_t flags;
    int64_t n_children;
    struct ArrowSchema** children;
    struct ArrowSchema* dictionary;

    // Release callback
    void (*release)(struct ArrowSchema*);
    // Opaque producer-specific data
    void* private_data;
};

struct ArrowArray {
    // Array data description
    int64_t length;
    int64_t null_count;
    int64_t offset;
    int64_t n_buffers;
    int64_t n_children;
    const void** buffers;
    struct ArrowArray** children;
    struct ArrowArray* dictionary;

    // Release callback
    void (*release)(struct ArrowArray*);
    // Opaque producer-specific data
    void* private_data;
};
/* End Arrow C API */
/* ************************************************************************ */
#endif  // TILEDBSOMA_CARROW_H
