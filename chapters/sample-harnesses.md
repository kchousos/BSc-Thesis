# Sample Generated Harnesses

## Buffer

harness

``` C
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "buffer.h"

/*
 * LLVMFuzzerTestOneInput harness to fuzz the function buffer_appendf.
 *
 * The fuzzing input data is treated as a format string argument to buffer_appendf.
 * This targets potential format string vulnerabilities and buffer resizing issues
 * within buffer_appendf as flagged by static analysis.
 *
 * We create a fresh buffer_t instance with buffer_new(), then call buffer_appendf()
 * with the fuzz input as the format string. We do not supply additional variadic
 * arguments as the input is a single buffer.
 *
 * After the call, we free the buffer_t instance to avoid memory leaks.
 */
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        // No data to test; skip
        return 0;
    }

    // Allocate a writable null-terminated string for the format input
    // We add one byte for the null terminator
    char *fmt = (char *)malloc(size + 1);
    if (!fmt) return 0; // Allocation failed, skip

    // Copy input and null terminate
    memcpy(fmt, data, size);
    fmt[size] = '\0';

    // Create a new buffer instance
    buffer_t *buf = buffer_new();
    if (!buf) {
        free(fmt);
        return 0;
    }

    // Call buffer_appendf with user-controlled format string
    // No additional arguments are supplied
    (void)buffer_appendf(buf, fmt);

    // Cleanup
    buffer_free(buf);
    free(fmt);

    return 0;
}
```

function

```C
int buffer_appendf(buffer_t *self, const char *format, ...) {
  va_list ap;
  va_list tmpa;
  char *dst = NULL;
  int length = 0;
  int required = 0;
  int bytes = 0;

  va_start(ap, format);

  length = buffer_length(self);

  // First, we compute how many bytes are needed
  // for the formatted string and allocate that
  // much more space in the buffer.
  va_copy(tmpa, ap);
  required = vsnprintf(NULL, 0, format, tmpa);
  va_end(tmpa);
  if (-1 == buffer_resize(self, length + required)) {
    va_end(ap);
    return -1;
  }

  // Next format the string into the space that we
  // have made room for.
  dst = self->data + length;
  bytes = vsnprintf(dst, 1 + required, format, ap);
  va_end(ap);

  return bytes < 0
    ? -1
    : 0;
}
```

Crash input (xxd output) which triggers an exception in `buffer_appendf()`>`vsnprintf()`.

```
00000000: 1b2d 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d  .---------------
00000010: 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d  ----------------
00000020: 2d2d 2d2d 2d2d 2d2d 2d2d 2d25 2d2d 2d2d  -----------%----
00000030: 2d2d 2d2d 2d2d 2d2d 2d2d 2d2d 2d         -------------
```

## Cbuffer

harness

```C
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "cbuffer.h"

// New improved fuzzer harness for cbuf_offer with multiple writes and boundary tests
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) {
        // allow zero-size input to test zero-length write
        cbuf_t *cbuf = cbuf_new(12);
        if (cbuf == NULL)
            return 0;
        // calling offer with zero length should be tested
        (void)cbuf_offer(cbuf, NULL, 0);
        cbuf_free(cbuf);
        return 0;
    }

    cbuf_t *cbuf = cbuf_new(12);
    if (cbuf == NULL)
        return 0;

    // Split input roughly into two parts; first fills the buffer partially,
    // second part is used for fuzzing cbuf_offer calls
    size_t split = size / 2;
    const uint8_t *prefix_data = data;
    size_t prefix_size = split;
    const uint8_t *main_data = data + split;
    size_t main_size = size - split;

    // Initially fill the buffer partially with prefix_data to simulate used space
    if (prefix_size > 0) {
        int space = cbuf_unusedspace(cbuf);
        int to_write = prefix_size < (size_t)space ? (int)prefix_size : space - 1;
        if (to_write > 0) {
            (void)cbuf_offer(cbuf, prefix_data, to_write);
        }
    }

    // Now fuzz cbuf_offer with main_data
    // Derive write size from first byte of main_data if available, else zero.
    int write_size = 0;
    if (main_size > 0) {
        write_size = main_data[0];
        // Allow write size to be zero (edge case) and up to larger than buffer size to test rejection path
        // Normalize write_size to a range: 0 to 2 * cbuf->size to test boundary and overflow cases clearly
        int max_test_size = (int)(cbuf->size * 2);
        write_size = (write_size % (max_test_size + 1)); // allows 0 to max_test_size inclusive
    }

    // Pointer to data for writing is after first byte in main_data if exists
    const uint8_t *write_data = main_data + 1;
    size_t write_data_len = (main_size > 0) ? main_size - 1 : 0;

    // Clamp write_size to write_data_len but allow write_size > write_data_len to simulate out of bounds sizes
    // by assigning write_data_len as is -- note cbuf_offer will only read up to write_size bytes anyway
    // but fuzzing with invalid sizes tests boundary conditions.

    if ((size_t)write_size > write_data_len) {
        // We keep write_size as is for boundary fuzzing (even if it overflows input),
        // but avoid buffer overflow by passing smaller data pointer as NULL if no data available
        if (write_data_len == 0) {
            write_data = NULL;
        }
    }

    // Call cbuf_offer with fuzz parameters (including zero and oversized writes)
    (void)cbuf_offer(cbuf, write_data, write_size);

    // Additionally try a zero length call explicitly to test that edge case
    (void)cbuf_offer(cbuf, NULL, 0);

    // Optionally perform a few repeated calls with no data to simulate further state changes
    (void)cbuf_offer(cbuf, NULL, 0);
    (void)cbuf_offer(cbuf, NULL, 0);

    cbuf_free(cbuf);
    return 0;
}
```

crash input which triggers an exception in `cbuf_offer()`>`memcpy()`.

```
00000000: 0a                                       .
```

fuzzed function

```C
int cbuf_offer(cbuf_t *me, const unsigned char *data, const int size)
{
    /* prevent buffer from getting completely full or over commited */
    if (cbuf_unusedspace(me) <= size)
        return 0;

    int written = cbuf_unusedspace(me);
    written = size < written ? size : written;
    memcpy(me->data + me->tail, data, written);
    me->tail += written;
    if (me->size < me->tail)
        me->tail %= me->size;
    return written;
}
```

## chfreq.c

harness

```C
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Include the project's header file that declares chfreq
#include "chfreq.h"

// Helper function to free the matrix returned by chfreq
static void free_chfreq_matrix(uint32_t **mat) {
    if (!mat) return;
    for (int i = 0; mat[i] != NULL; i++) {
        free(mat[i]);
    }
    free(mat);
}

// libFuzzer entry point
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Defensive: If input size is zero, nothing to do
    if (size == 0) {
        return 0;
    }

    // Allocate a buffer to hold the input as a null-terminated string
    // Use heap allocation to avoid stack overflow issues with large inputs
    char *input_str = (char *)malloc(size + 1);
    if (!input_str) {
        // Allocation failed, return gracefully
        return 0;
    }

    // Copy fuzz input into buffer
    memcpy(input_str, data, size);

    // Null-terminate the input as chfreq expects a C string
    input_str[size] = '\0';

    // Call the function under test
    uint32_t **result = chfreq(input_str);

    // Free the dynamically allocated matrix returned by chfreq
    free_chfreq_matrix(result);

    // Free the input buffer
    free(input_str);

    return 0;
}
```

crash input which triggers a heap buffer overflow in `chfreq()`>`realloc()`.

```
00000000: 0a                                       .
```

fuzzed function

```C
uint32_t **
chfreq (const char *src) {
  uint32_t **mat = NULL;
  char ch = 0;
  size_t size = 1;
  int pos = 0;
  int i = 0;
  int idx = -1;

  // alloc
  mat = (uint32_t **) calloc(size, sizeof(uint32_t *));
  if (NULL == mat) { return NULL; }

  // build
  while ('\0' != (ch = src[i++])) {
    idx = find(mat, ch);
    if (-1 == idx) {
      idx = pos++;
      mat = (uint32_t **) realloc(mat, sizeof(uint32_t *) * ssize(src));
      mat[idx] = (uint32_t *) calloc(2, sizeof(uint32_t));
      mat[idx][0] = ch;
      mat[idx][1] = 1;
      size++;
    } else {
      mat[idx][1]++;
    }
  }

  mat[size] = NULL;

  return mat;
}
```

## Dateparse

harness

```C
#include <stddef.h>
#include <stdint.h>
#include "dateparse.h"

// LibFuzzer entry point
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size == 0) return 0;

    date_t parsed_date = 0;
    int offset = 0;

    // Pass the input data directly without copying
    (void)dateparse((const char *)data, &parsed_date, &offset, (int)size);

    return 0;
}
```

Crash input that causes a heap buffer overflow in `dateparse()`>`parseTime()`>`setMonth()`>`strncpy()`.

```
00000000: 6632 2066                                f2 f
```

fuzzed function

```C
int dateparse(const char* datestr, date_t* t, int *offset, int stringlen){
	struct parser p;
	*t = 0;
	if (!stringlen)
		stringlen = strlen(datestr);
	if (parseTime(datestr, &p, stringlen))
		return -1;
	return parse(&p, t, offset);
}
```

## Libbacon

harness

```C
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "bacon.h" // assuming this is the main project header defining bacon_decode and constants

// LibFuzzer entry point
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Defensive: bacon_decode expects null-terminated string, but inputs from fuzzer not guaranteed null-terminated.
    // Allocate a buffer one byte larger, copy data and append null terminator to safely create input string.
    char *input = (char *)malloc(size + 1);
    if (!input) {
        return 0; // allocation failed, skip this input
    }
    memcpy(input, data, size);
    input[size] = '\0';

    // Call bacon_decode with default alphabet by passing NULL
    char *decoded = bacon_decode(input, NULL);

    // Free decoded string if returned
    if (decoded) {
        free(decoded);
    }

    free(input);

    return 0;
}
```

crash input that causes heap buffer overflow in `bacon_decode()`>`malloc()`.

```
00000000: 4141 4141 41                             AAAAA
```

fuzzed function

```C
char *
bacon_decode (const char *src, const char *alpha) {
  char *dec = (char *) malloc(sizeof(char));
  char buf[5];
  char ch = 0;
  size_t size = 0;
  size_t len = (size_t) strlen(src);
  size_t alen = 0;
  size_t bsize = 0; // buffer size
  int i = -1; // source index
  int sep = 0;
  int idx = -1;
  int custom = 0;

  if (NULL == dec) { return NULL; }

  // use default
  if (NULL == alpha) {
    alpha = BACON_ALPHA;
  } else { custom = 1; }

  // alpha length
  alen = (size_t) strlen(alpha);

  // parse and decode
  while ((++i) < len) {
    // read symbol and convert
    // to uppercase just in case
    ch = toupper(src[i]);

    // store symbols in buffer
    if (BACON_A == ch || BACON_B == ch) {
      buf[bsize++] = ch;
    } else {
      // oob - needs space
      sep = 1;
    }

    if (5 == bsize) {
      // accumulate
      idx = (
          (buf[0] == BACON_A ? 0 : 0x10) +
          (buf[1] == BACON_A ? 0 : 0x08) +
          (buf[2] == BACON_A ? 0 : 0x04) +
          (buf[3] == BACON_A ? 0 : 0x02) +
          (buf[4] == BACON_A ? 0 : 0x01) 
       );

      // append space if needed and
      // is not first char yieled
      if (1 == sep && size > 0) {
        dec[size++] = ' ';
      }

      // append char from alphabet
      // uppercased
      dec[size++] = toupper(alpha[idx]);

      // reset
      bsize = 0;
      sep = 0;
    }
  }

  // cap
  dec[size] = '\0';

  return dec;
}
```

## Libbeaufort

harness

```C
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "beaufort.h"

// libFuzzer entry point for fuzz testing beaufort_decrypt function.
// This harness splits input bytes into two strings: src and key.
// It calls beaufort_decrypt with those strings and NULL mat,
// which triggers internal tableau setup.
// The output buffer is freed after use to avoid leaks.

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // If input is zero size, no meaningful test possible, return early.
    if (size == 0) {
        return 0;
    }

    // Allocate buffer to hold a copy of input plus one byte for null terminator.
    // We'll create two null-terminated strings inside this buffer.
    char *buf = (char *)malloc(size + 2); // +2 to be safe for two terminators.
    if (!buf) {
        return 0; // Allocation failure, skip this input.
    }

    // Copy data to buf and ensure it's not modified outside.
    memcpy(buf, data, size);
    buf[size] = '\0'; // Null-terminate at end for safety.
    buf[size+1] = '\0';

    // Find split position for src and key strings.
    // Strategy: Find first 0 byte inside input to split; if none, split in half.
    size_t split_pos = 0;
    for (; split_pos < size; split_pos++) {
        if (buf[split_pos] == '\0') {
            break;
        }
    }

    // If no null byte found, split input roughly in half.
    if (split_pos == size) {
        split_pos = size / 2;
    }

    // Null terminate src at split_pos, ensure key string starts at split_pos+1.
    buf[split_pos] = '\0';

    char *src = buf;
    char *key = buf + split_pos + 1;

    // To avoid passing a key pointer beyond buffer end, if no key data,
    // set key to empty string.
    if (key >= buf + size + 2) {
        key = "";
    }

    // Call beaufort_decrypt with src, key, and NULL mat (default matrix).
    char *dec = beaufort_decrypt(src, key, NULL);

    // Free returned decrypted string buffer if not NULL.
    if (dec) {
        free(dec);
    }

    // Free the duplicated input buffer.
    free(buf);

    return 0;
}
```

crash input that causes a heap buffer overflow in `beaufort_decrypt()`>`beaufort_tableau()`>`calloc()`.

```
00000000: 0a                                       .
```

fuzzed function

```C

char *
beaufort_decrypt (const char *src, const char *key, char **mat) {
  char *dec = NULL;
  char ch = 0;
  char k = 0;
  size_t ksize = 0;
  size_t size = 0;
  size_t rsize = 0;
  size_t len = 0;
  int i = 0;
  int x = 0;
  int y = 0;
  int j = 0;
  int needed = 1;

  if (NULL == mat) {
    mat = beaufort_tableau(BEAUFORT_ALPHA);
    if (NULL == mat) { return NULL; }
  }

  ksize = ssize(key);
  len = ssize(src);
  rsize = ssize(mat[0]);
  dec = (char *) malloc(sizeof(char) * len + 1);

  if (NULL == dec) { return NULL; }

  for (; (ch = src[i]); ++i) {
    needed = 1;

    // find column with char
    for (y = 0; y < rsize; ++y) {
      if (ch == mat[y][0]) { needed = 1; break; }
      else { needed = 0; }
    }

    // if not needed append
    // char and continue
    if (0 == needed) {
      dec[size++] = ch;
      continue;
    }

    // determine char in `key'
    k = key[(j++) % ksize];

    for (x = 0; x < rsize; ++x)  {
      if (k == mat[y][x]) { needed = 1; break; }
      else { needed = 0; }
    }

    // append current char if not
    // needed and decrement unused
    // modulo index
    if (0 == needed) {
      dec[size++] = ch;
      j--;
      continue;
    }

    dec[size++] = mat[0][x];
  }

  dec[size] = '\0';

  return dec;
}
```

## Mpc

harness

```C
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// We need these macros from original source; assumed defaults from retrieved code
#define MPC_INPUT_STRING 1
#define MPC_INPUT_PIPE 2
#define MPC_INPUT_FILE 3
#define MPC_INPUT_MARKS_MIN 4
#define MPC_INPUT_MEM_NUM 256

// Minimal mpc_state_t for marks array, mirroring original usage (only pos needed)
typedef struct {
  size_t pos;
} mpc_state_t;

// Updated definition of mpc_input_t struct based on full context and usage.
typedef struct {
  int type;
  int backtrack;
  int marks_num;
  int marks_slots;

  // String input data
  const char *string;

  // State tracking position
  mpc_state_t state;

  // Memory pool for mpc_malloc
  char mem[MPC_INPUT_MEM_NUM];
  char mem_full[MPC_INPUT_MEM_NUM];
  size_t mem_index;

  // Marks arrays for backtracking
  mpc_state_t *marks;
  char *lasts;
  char last;

  // File pointer for FILE/PIPE input type - unused here
  FILE *file;

  // Buffer for PIPE input type - unused here
  char *buffer;

  // Filename field used in real input (omitted here as irrelevant)
  char *filename;

  // Suppress flag (unused, set 0)
  int suppress;

} mpc_input_t;

// Forward declarations with external linkage; these are adapted from internal static versions

// Mark the current input position for backtracking
void mpc_input_mark(mpc_input_t *i) {
  if (i->backtrack < 1) { return; }
  i->marks_num++;
  if (i->marks_num > i->marks_slots) {
    i->marks_slots = i->marks_num + i->marks_num/2;
    i->marks = (mpc_state_t*)realloc(i->marks, sizeof(mpc_state_t) * i->marks_slots);
    i->lasts = (char*)realloc(i->lasts, sizeof(char) * i->marks_slots);
  }
  i->marks[i->marks_num-1] = i->state;
  i->lasts[i->marks_num-1] = i->last;
  if (i->type == MPC_INPUT_PIPE && i->marks_num == 1) {
    i->buffer = calloc(1, 1);
  }
}

// Undo the last mark (pop backtracking point)
void mpc_input_unmark(mpc_input_t *i) {
  if (i->backtrack < 1) { return; }
  if (i->marks_num > 0)
    i->marks_num--;
  if (i->marks_slots > i->marks_num + i->marks_num/2 && i->marks_slots > MPC_INPUT_MARKS_MIN) {
    i->marks_slots = i->marks_num > MPC_INPUT_MARKS_MIN ? i->marks_num : MPC_INPUT_MARKS_MIN;
    i->marks = (mpc_state_t*)realloc(i->marks, sizeof(mpc_state_t) * i->marks_slots);
    i->lasts = (char*)realloc(i->lasts, sizeof(char) * i->marks_slots);
  }
  if (i->type == MPC_INPUT_PIPE && i->marks_num == 0) {
    for (int j = (int)strlen(i->buffer) - 1; j >= 0; j--)
      ungetc(i->buffer[j], i->file);
    free(i->buffer);
    i->buffer = NULL;
  }
}

// Rewind input to the last mark, then remove that mark
void mpc_input_rewind(mpc_input_t *i) {
  if (i->backtrack < 1) { return; }
  if (i->marks_num > 0) {
    i->state = i->marks[i->marks_num - 1];
    i->last = i->lasts[i->marks_num - 1];
    if (i->type == MPC_INPUT_FILE) {
      fseek(i->file, i->state.pos, SEEK_SET);
    }
  }
  mpc_input_unmark(i);
}

// Provide a small memory allocator using the internal pool or standard malloc
void *mpc_malloc(mpc_input_t *i, size_t n) {
  size_t j;
  char *p;
  if (n > sizeof(i->mem)) {
    return malloc(n);
  }
  j = i->mem_index;
  do {
    if (!i->mem_full[i->mem_index]) {
      p = (void*)(i->mem + i->mem_index);
      i->mem_full[i->mem_index] = 1;
      i->mem_index = (i->mem_index + 1) % MPC_INPUT_MEM_NUM;
      return p;
    }
    i->mem_index = (i->mem_index + 1) % MPC_INPUT_MEM_NUM;
  } while (j != i->mem_index);
  return malloc(n);
}

// Check if input is at end (terminated)
int mpc_input_terminated(mpc_input_t *i) {
  // terminated if current pos points to '\0'
  if (i->string == NULL) return 1;
  return i->string[i->state.pos] == '\0';
}

// Get current input character advancing position, or '\0' if terminated
char mpc_input_getc(mpc_input_t *i) {
  if (mpc_input_terminated(i)) { return '\0'; }
  char c = i->string[i->state.pos];
  i->state.pos++;
  i->last = c;
  return c;
}

// On success, optionally output char and return 1
int mpc_input_success(mpc_input_t *i, char c, char **o) {
  (void)i; (void)c; // unused in this simplified stub
  if (o) *o = NULL;
  return 1;
}

// On failure, handle ungetc or other cleanup and return 0
int mpc_input_failure(mpc_input_t *i, char c) {
  switch (i->type) {
    case MPC_INPUT_STRING: {
      // Nothing special
      break;
    }
    case MPC_INPUT_FILE:
      fseek(i->file, -1, SEEK_CUR);
      break;
    case MPC_INPUT_PIPE: {
      if (!i->buffer) { ungetc(c, i->file); }
      else {
        // Conceptually check range, simplified here just break
      }
      break;
    }
    default: break;
  }
  return 0;
}
// Parser a single character c if matches input, else failure
int mpc_input_char(mpc_input_t *i, char c, char **o) {
  char x;
  if (mpc_input_terminated(i)) { return 0; }
  x = mpc_input_getc(i);
  return (x == c) ? mpc_input_success(i, x, o) : mpc_input_failure(i, x);
}

// Primary function under test with external linkage
int mpc_input_string(mpc_input_t *i, const char *c, char **o) {
  const char *x = c;
  mpc_input_mark(i);
  while (*x) {
    if (!mpc_input_char(i, *x, NULL)) {
      mpc_input_rewind(i);
      return 0;
    }
    x++;
  }
  mpc_input_unmark(i);
  *o = (char *)mpc_malloc(i, strlen(c) + 1);
  strcpy(*o, c);
  return 1;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
  // Defensive: ignore if no data to parse
  if (size == 0) { return 0; }

  // Allocate and initialize input struct
  mpc_input_t *input = (mpc_input_t *)calloc(1, sizeof(mpc_input_t));
  if (!input) { return 0; }

  // Initialize fields for string input
  input->type = MPC_INPUT_STRING;
  input->backtrack = 1;
  input->marks_num = 0;
  input->marks_slots = MPC_INPUT_MARKS_MIN;
  input->marks = (mpc_state_t *)calloc(input->marks_slots, sizeof(mpc_state_t));
  input->lasts = (char *)calloc(input->marks_slots, sizeof(char));
  input->last = '\0';
  input->mem_index = 0;
  memset(input->mem_full, 0, sizeof(input->mem_full));

  // Copy input data into a null-terminated string for safety
  char *null_terminated_str = (char *)malloc(size + 1);
  if (!null_terminated_str) {
    free(input->marks);
    free(input->lasts);
    free(input);
    return 0;
  }
  memcpy(null_terminated_str, data, size);
  null_terminated_str[size] = '\0';

  // Set string field
  input->string = null_terminated_str;
  input->state.pos = 0;

  char *output = NULL;

  // Call the fuzz target function
  (void)mpc_input_string(input, null_terminated_str, &output);

  // Free output if allocated by mpc_malloc (it uses malloc fallback)
  if (output != NULL) {
    free(output);
  }

  free(null_terminated_str);
  free(input->marks);
  free(input->lasts);
  free(input);
  return 0;
}
```

crash input that causes `free()` call in non-`malloc()`-ed address in [`LLVMFuzzerTestOneInput`]{.mark}!!

```
00000000: 0a                                       .
```

fuzzed function

```C

static int mpc_input_string(mpc_input_t *i, const char *c, char **o) {

  const char *x = c;

  mpc_input_mark(i);
  while (*x) {
    if (!mpc_input_char(i, *x, NULL)) {
      mpc_input_rewind(i);
      return 0;
    }
    x++;
  }
  mpc_input_unmark(i);

  *o = mpc_malloc(i, strlen(c) + 1);
  strcpy(*o, c);
  return 1;
}
```

## Progress.c

harness

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "progress.h"

/*
 * LibFuzzer harness for progress_write(progress_t *progress).
 *
 * This fuzz target creates a progress_t structure with fuzz-controlled fields:
 * - value, total, width, elapsed
 * - fmt string, bar_char string, bg_bar_char string
 *
 * These fields influence internal strcpy/strcat calls and replace_str usage,
 * which may have buffer overflow issues due to lack of bounds checking.
 * 
 * The harness carefully extracts varying length strings and numeric values from
 * the input data, ensuring they are plausible and safe to use. Any input length
 * less than required will return early.
 */

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Minimum size needed for minimal fields:
    // reserve some bytes for integers and doubles, then strings
    if (size < 20) return 0;

    // Allocate progress struct
    progress_t *progress = (progress_t *)malloc(sizeof(progress_t));
    if (!progress) return 0;

    // Extract integers and double from input safely
    // value: int32_t (4 bytes)
    int32_t value = 0;
    memcpy(&value, data, sizeof(int32_t));
    // total: int32_t (4 bytes)
    int32_t total = 0;
    memcpy(&total, data + 4, sizeof(int32_t));
    // width: int32_t (4 bytes)
    int32_t width = 0;
    memcpy(&width, data + 8, sizeof(int32_t));
    // elapsed: double (8 bytes)
    double elapsed = 0.0;
    memcpy(&elapsed, data + 12, sizeof(double));

    // Clamp total to >= 1 to avoid div by zero
    if (total <= 0) total = 1;
    // Clamp width to [1, 1024]
    if (width <= 0) width = 1;
    if (width > 1024) width = 1024;
    // Clamp value to [0, total]
    if (value < 0) value = 0;
    if (value > total) value = total;
    // Clamp elapsed to a sensible range like [0, 100000] milliseconds
    if (elapsed < 0) elapsed = 0;
    if (elapsed > 100000) elapsed = 100000;

    // Setup progress_t fields
    progress->value = value;
    progress->total = total;
    progress->width = width;
    progress->elapsed = elapsed;

    // Set started/finished and listener_count to zero/false
    progress->started = 0;
    progress->finished = 0;
    progress->listener_count = 0;

    // Now extract strings from remaining input for fmt, bar_char, bg_bar_char
    // Split remaining fuzz data into 3 parts approximately
    size_t remaining = size - 20;
    size_t fmt_len = remaining / 3;
    size_t bar_char_len = remaining / 3;
    size_t bg_bar_char_len = remaining - fmt_len - bar_char_len;

    // Allocate strings with +1 for null terminator
    char *fmt_str = malloc(fmt_len + 1);
    char *bar_char_str = malloc(bar_char_len + 1);
    char *bg_bar_char_str = malloc(bg_bar_char_len + 1);
    if (!fmt_str || !bar_char_str || !bg_bar_char_str) {
        free(progress);
        free(fmt_str);
        free(bar_char_str);
        free(bg_bar_char_str);
        return 0;
    }

    // Copy and null terminate
    memcpy(fmt_str, data + 20, fmt_len);
    fmt_str[fmt_len] = '\0';

    memcpy(bar_char_str, data + 20 + fmt_len, bar_char_len);
    bar_char_str[bar_char_len] = '\0';

    memcpy(bg_bar_char_str, data + 20 + fmt_len + bar_char_len, bg_bar_char_len);
    bg_bar_char_str[bg_bar_char_len] = '\0';

    // Avoid zero-length bar_char or bg_bar_char by forcing at least one char
    if (bar_char_len == 0) {
      strcpy(bar_char_str, "=");
    }
    if (bg_bar_char_len == 0) {
      strcpy(bg_bar_char_str, "-");
    }

    // Assign strings to progress
    // According to the code, these are treated as const char* and assumed null-terminated
    progress->fmt = fmt_str;
    progress->bar_char = bar_char_str;
    progress->bg_bar_char = bg_bar_char_str;

    // Now call progress_write, the function under test
    progress_write(progress);

    // Free allocated strings and struct
    free(fmt_str);
    free(bar_char_str);
    free(bg_bar_char_str);
    free(progress);

    return 0;
}
```

crash input that causes a heap buffer overflow in [`LLVMFuzzerTestOneInput`]{.mark}>`malloc()`

```
00000000: 0000 0000 00ff ffff ffff ffff 0000 0000  ................
00000010: 0000 002a                                ...*
```

fuzzed function

```C
void
progress_write (progress_t *progress) {
  int i = 0;
  int width = (int) progress->width;
  int percent = 100 * ((double) progress->value / (double) progress->total);
  int complete = (width * ((double) progress->value / (double) progress->total));
  int incomplete = width - (complete);
  double elapsed = progress->elapsed;
  char *fmt = malloc(512 * sizeof(char));
  char *bar = malloc((complete + incomplete) * sizeof(char));
  char *percent_str = malloc(sizeof(char)*20);
  char *elapsed_str = malloc(sizeof(char)*20);

  sprintf(percent_str, "%d%%", percent);
  if (elapsed > 1000) {
    sprintf(elapsed_str, "%.2fs", elapsed/1000);
  } else {
    sprintf(elapsed_str, "%.0fms", elapsed);
  }
  

  strcpy(fmt, "");
  strcat(fmt, progress->fmt);
  strcpy(bar, "");

  if (complete) {
    for (i = 0; i < complete; ++i) {
      bar[i] = *progress->bar_char;
    }
  }

  if (incomplete) {
    for (; i < complete + incomplete; ++i) {
       bar[i] = *progress->bg_bar_char;
    }
  }

  bar[i] = '\0';

  fmt = replace_str(fmt, ":bar", bar);
  fmt = replace_str(fmt, ":percent", percent_str);
  fmt = replace_str(fmt, ":elapsed", elapsed_str);

  printf("%c[2K", 27);
  printf("\r%s", fmt);

  fflush(stdout);
  free(bar);
  free(percent_str);
  free(elapsed_str);
  free(fmt);
}
```

## Semver.c

harness

```C
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include "semver.h"

// Enhanced fuzzer harness for semver_parse including calls to semver_numeric and semver_render
// to help increase coverage and trigger more bugs faster.
// Dynamically allocates input buffer with no size limit other than system memory.
// Frees allocated semver_t string members after use.
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Allocate buffer dynamically to handle any input size.
    char *input_str = (char *)malloc(size + 1);
    if (input_str == NULL) {
        return 0;
    }
    memcpy(input_str, data, size);
    input_str[size] = '\0';

    semver_t ver;
    memset(&ver, 0, sizeof(ver));

    // Parse the semver string.
    (void)semver_parse(input_str, &ver);

    // Call semver_numeric to exercise more code paths.
    (void)semver_numeric(&ver);

    // Call semver_render with buffer large enough for rendered output.
    // Typical semantic version strings are short, but use a buffer of size size+20 to be safe.
    char *render_buf = (char *)malloc(size + 20);
    if (render_buf != NULL) {
        memset(render_buf, 0, size + 20);
        semver_render(&ver, render_buf);
        free(render_buf);
    }

    // Free dynamically allocated members inside semver_t.
    if (ver.prerelease) {
        free(ver.prerelease);
        ver.prerelease = NULL;
    }
    if (ver.metadata) {
        free(ver.metadata);
        ver.metadata = NULL;
    }

    free(input_str);
    return 0;
}
```

crash input that causes a stack buffer overflow in `semver_render()`>`concat_char()`>`sprintf()`.

```
00000000: 392d 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b  9-++++++++++++++
00000010: 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b  ++++++++++++++++
00000020: 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b  ++++++++++++++++
00000030: 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b 2b2b  ++++++++++++++++
00000040: 2b2b 2b2b 2b2b 2b46 4c                   +++++++FL
```

fuzzed functions

```C
/**
 * Parses a string as semver expression.
 *
 * Returns:
 *
 * `0` - Parsed successfully
 * `-1` - In case of error
 */

int
semver_parse (const char *str, semver_t *ver) {
  int valid, res;
  size_t len;
  char *buf;
  valid = semver_is_valid(str);
  if (!valid) return -1;

  len = strlen(str);
  buf = (char*)calloc(len + 1, sizeof(*buf));
  if (buf == NULL) return -1;
  strcpy(buf, str);

  ver->metadata = parse_slice(buf, MT_DELIMITER[0]);
  ver->prerelease = parse_slice(buf, PR_DELIMITER[0]);

  res = semver_parse_version(buf, ver);
  free(buf);
#if DEBUG > 0
  printf("[debug] semver.c %s = %d.%d.%d, %s %s\n", str, ver->major, ver->minor, ver->patch, ver->prerelease, ver->metadata);
#endif
  return res;
}

//...

/**
 * Render a given semver as string
 */

void
semver_render (semver_t *x, char *dest) {
  concat_num(dest, x->major, NULL);
  concat_num(dest, x->minor, DELIMITER);
  concat_num(dest, x->patch, DELIMITER);
  if (x->prerelease) concat_char(dest, x->prerelease, PR_DELIMITER);
  if (x->metadata) concat_char(dest, x->metadata, MT_DELIMITER);
}
```

## Torrent-reader

harness

```C
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include "torrent_reader.h"

// Dummy callback that accepts event key strings, does nothing and returns 0
static int dummy_cb_event(void* udata, const char* key) {
    (void)udata;
    (void)key;
    return 0;
}

// Dummy callback that accepts event key and string value with length, does nothing and returns 0
static int dummy_cb_event_str(void* udata, const char* key, const char* val, int len) {
    (void)udata;
    (void)key;
    (void)val;
    (void)len;
    return 0;
}

// Dummy callback that accepts event key and int value, does nothing and returns 0
static int dummy_cb_event_int(void* udata, const char* key, int val) {
    (void)udata;
    (void)key;
    (void)val;
    return 0;
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Guard against null or zero length input, just return early
    if (!data || size == 0) {
        return 0;
    }

    // tfr_t is an opaque struct hidden inside torrent_reader.c
    // The tfr_new function returns void* instead of tfr_t*,
    // so we treat ctx as void* here following the library interface.
    void* ctx = tfr_new(dummy_cb_event, dummy_cb_event_str, dummy_cb_event_int, NULL);
    if (!ctx) {
        // Allocation failed, skip this input
        return 0;
    }

    // Use ctx as void* in tfr_read_metainfo calls
    tfr_read_metainfo(ctx, (const char *)data, (int)size);

    // Free context allocated by tfr_new using standard free
    free(ctx);

    return 0;
}
```

crash input that causes a runtime assertion error (applying zero offset to null pointer) to function of the dependency  "heapless-benocde": `tfr_read_metainfo()`>`bencode_dict_get_next()`>`__iterate_to_next_string_pos()`>`bencode_is_string()`>`__assert()`.

```
00000000: 6464 6464 6464 642e                      ddddddd.
```

fuzzed function

```C
void tfr_read_metainfo(
    void *me,
    const char *buf,
    const int len
)
{
    bencode_t ben;

    bencode_init(&ben, buf, len);

    if (!bencode_is_dict(&ben))
    {
        return;
    }

    while (bencode_dict_has_next(&ben))
    {
        int klen;
        const char *key;
        bencode_t benk;

        bencode_dict_get_next(&ben, &benk, &key, &klen);

        if (!strncmp(key, "announce", klen))
        {
            int len;
            const char *val;

            bencode_string_value(&benk, &val, &len);
            tfr_event_str(me, "announce", val, len);
        }
        else if (!strncmp(key, "announce-list", klen))
        {
            /*  loop through announce list */

            assert(bencode_is_list(&benk));

            while (bencode_list_has_next(&benk))
            {
                bencode_t innerlist;

                bencode_list_get_next(&benk, &innerlist);
                while (bencode_list_has_next(&innerlist))
                {
                    bencode_t benlitem;
                    const char *backup;
                    int len;

                    bencode_list_get_next(&innerlist, &benlitem);
                    bencode_string_value(&benlitem, &backup, &len);
                    tfr_event_str(me, "tracker_backup", backup, len);
                }
            }
        }
        else if (!strncmp(key, "comment", klen))
        {
            int len;
            const char *val;

            bencode_string_value(&benk, &val, &len);
        }
        else if (!strncmp(key, "created by", klen))
        {
            int len;
            const char *val;

            bencode_string_value(&benk, &val, &len);
        }
        else if (!strncmp(key, "creation date", klen))
        {
            long int date;

            bencode_int_value(&benk, &date);
        }
        else if (!strncmp(key, "encoding", klen))
        {
            int len;
            const char *val;

            bencode_string_value(&benk, &val, &len);
        }
        else if (!strncmp(key, "info", klen))
        {
            __do_info_dict(me, &benk);
        }
    }
}
```

