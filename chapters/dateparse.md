# Dateparse example

The outputs from each phase of the OverHAuL process pertaining to the dateparse project: the static analysis report (@lst-static), sample function segments derived from dateparse (@lst-chunks), the generated compilation command (@lst-compilation), the bug-finding harness (@lst-harness), the identified crash input (@lst-input), and a portion of the harness output (@lst-output).

::: {#lst-static  fig-scap='Static analysis report'}

```text
Flawfinder version 2.0.19, (C) 2001-2019 David A. Wheeler.
Number of rules (primarily dangerous function names) in C/C++ ruleset: 222
Examining ./dateparse.c
Examining ./dateparse.h
Examining ./test.c

FINAL RESULTS:

./dateparse.c:405:  [4] (buffer) strcpy:
  Does not check for buffer overflows when copying to destination [MS-banned]
  (CWE-120). Consider using snprintf, strcpy_s, or strlcpy (warning: strncpy
  easily misused).

......

./dateparse.c:2192:  [1] (buffer) strlen:
  Does not handle strings that are not \0-terminated; if given one it may
  perform an over-read (it could cause a crash if unprotected) (CWE-126).

ANALYSIS SUMMARY:

Hits = 64
Lines analyzed = 2719 in approximately 0.04 seconds (61234 lines/second)
Physical Source Lines of Code (SLOC) = 1966
Hits@level = [0]  15 [1]  28 [2]  31 [3]   0 [4]   5 [5]   0
Hits@level+ = [0+]  79 [1+]  64 [2+]  36 [3+]   5 [4+]   5 [5+]   0
Hits/KSLOC@level+ = [0+] 40.1831 [1+] 32.5534 [2+] 18.3113 [3+] 2.54323
    [4+] 2.54323 [5+]   0
Dot directories skipped = 1 (--followdotdir overrides)
Minimum risk level = 1

Not every hit is necessarily a security vulnerability.
You can inhibit a report by adding a comment in this form:
// flawfinder: ignore
Make *sure* it's a false positive!
You can use the option --neverignore to show these.

There may be other security vulnerabilities; review your code!
See 'Secure Programming HOWTO'
(https://dwheeler.com/secure-programs) for more information.
```

Static analysis report (Flawfinder output) of dateparse.
:::

::: {#lst-chunks  fig-scap='Codebase oracle samples'}
```C
File: dateparse/dateparse.c
Signature: void (struct parser *, int, int)
Code:
static void setOffset(struct parser* p, int i, int len){
        strncpy(p->offsetbuf, p->datestr+i, len);
        p->offsetbuf[len] = 0;
}


File: dateparse/dateparse.c
Signature: void (struct parser *, char *)
Code:
static void setFullMonth(struct parser* p, char* month){
        strcpy(p->mobuf, month);
}


File: dateparse/dateparse.c
Signature: int (const char *, long long *, int *, int)
Code:
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

Sample chunks contained in dateparse's codebase oracle.
:::

::: {#lst-compilation fig-scap='Generated compilation command'}
```sh
# cat ./overhaul.sh
clang -g -fsanitize=fuzzer,address,undefined harnesses/harness.c -I . 
 dateparse.c -o harness
```

OverHAuL's generated compilation command for dateparse.
:::

::: {#lst-harness fig-scap='Sample dateparse harness'}
```C
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "dateparse.h"

// ...
struct parser {
	char mobuf[16];
};

// ...
static void setFullMonth(struct parser* p, char* month){
	strcpy(p->mobuf, month);
}

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
	// Allocate a parser instance on the heap.
	struct parser *p = (struct parser*)malloc(sizeof(struct parser));
	if (!p) {
		return 0;
	}
	// Initialize parser with zeros.
	memset(p, 0, sizeof(struct parser));
	// Prepare month string input: ensure null-terminated string for strcpy.
	char *month = (char*)malloc(size + 1);
	if (!month) {
		free(p);
		return 0;
	}
	memcpy(month, data, size);
	month[size] = '\0';  // Null terminate to avoid overread in strcpy.
	// Call the vulnerable function with fuzzed month string.
	setFullMonth(p, month);
	// Cleanup
	free(month);
	free(p);
	return 0;
}
```

A crash-finding harness for dateparse, generated through OverHAuL (some comments were removed).
:::

::: {#lst-input fig-scap='Sample dateparse crash input'}
```
00000000: 315e 5e5e 5e5e 5e5e 5e5e 5e5e 5e5e 5e5e  1^^^^^^^^^^^^^^^
00000010: 0a                                       .
```

An input string that crashes the harness in @lst-harness. What is shown is its `xxd` output.
:::

::: {#lst-output fig-scap='Sample dateparse harness output'}
``` text
INFO: Running with entropic power schedule (0xFF, 100).
INFO: Seed: 2365219758
INFO: Loaded 1 modules   (3723 inline 8-bit counters): 3723 [0x67ccc0,
      0x67db4b),
INFO: Loaded 1 PC tables (3723 PCs): 3723 [0x618d40,0x6275f0),
./harness: Running 1 inputs 1 time(s) each.
Running: crash-7fd6f4dd5d39420d6f7887ff995b4e855ae90c16
=================================================================
==10973==ERROR: AddressSanitizer: heap-buffer-overflow on address
0x7bcece9e00a0 at pc 0x000000526c0e bp 0x7fff3dc0aa20 sp 0x7fff3dc0a1d8
WRITE of size 18 at 0x7bcece9e00a0 thread T0
    #0 0x000000526c0d in strcpy
       (/home/kchou/Bin/Repos/kchousos/OverHAuL/output/dateparse/harness
       +0x526c0d) (BuildId: d658684b8726dc7e8e768089710d13c96cfc81f0)
    #1 0x000000585555 in setFullMonth
       /home/kchou/Bin/Repos/kchousos/OverHAuL/output/dateparse/harnesses
       /harness.c:18:2
    #2 0x0000005853fd in LLVMFuzzerTestOneInput
       /home/kchou/Bin/Repos/kchousos/OverHAuL/output/dateparse/harnesses
       /harness.c:41:2
...
SUMMARY: AddressSanitizer: heap-buffer-overflow
         (/home/kchou/Bin/Repos/kchousos/OverHAuL/output/dateparse/harness
         +0x526c0d) (BuildId: d658684b8726dc7e8e768089710d13c96cfc81f0) in
         strcpy
Shadow bytes around the buggy address:
  0x7bcece9dfe00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcece9dfe80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcece9dff00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcece9dff80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7bcece9e0000: fa fa 00 00 fa fa 00 fa fa fa 00 fa fa fa 00 fa
=>0x7bcece9e0080: fa fa 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
  0x7bcece9e0100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcece9e0180: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcece9e0200: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcece9e0280: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x7bcece9e0300: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
```

The output of the harness in @lst-harness when executed with @lst-input as input.
:::
