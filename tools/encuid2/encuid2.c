#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>
#include <errno.h>
#include <limits.h>
#include <endian.h>
#include <unistd.h>
#include <inttypes.h>
#include <assert.h>

#include "aes.h"

typedef struct {
    const char *aeskey;
    size_t ptlen;
    int shr;
    bool obf;
} algo_ctx_t;

static const algo_ctx_t ALGOS[] = {
    {"59494F4754fff00\0", AES_BLOCKLEN,     32, false},
    { "S@gi0PneW^#*T1Zb", AES_BLOCKLEN * 2, 26,  true},
    { "$Fl0R0kmKh1*Jkme", AES_BLOCKLEN * 2,  0,  true}
};

void show_usage(const char *prog) {
    fprintf(stderr, "Usage: %s [-a] <uid>\n", prog);
    fputs("Options:\n", stderr);
    fputs("\t-a\talgorithm 0|1|2 (default: 1)\n", stderr);
    fputs("\t-v\tenable verbose mode\n", stderr);
    fputs("\t<uid> 16-char hex value\n", stderr);
}

static uint64_t parse_uid(const char *uid) {
    uint64_t val = 0;
    size_t len = strlen(uid);

    if (len != AES_KEYLEN) {
        fputs("Error: invalid uid length\n", stderr);
        goto end;
    }

    for (size_t i = 0; i < len; i++) {
        if (!isxdigit(uid[i])) {
            fputs("Error: uid contains non-hex char\n", stderr);
            goto end;
        }
    }

    char *endptr = NULL;
    val = strtoull(uid, &endptr, 16);

    if (endptr != uid + len || errno == ERANGE) {
        fputs("Error: uid conversion failed or out of range\n", stderr);
        goto end;
    }

end:
    return val;
}

static uint8_t *gen_plaintext(const algo_ctx_t *ctx, const uint64_t uid) {
    uint8_t *buf = calloc(1, ctx->ptlen);

    assert(buf != NULL);

    size_t n = 0;

    if (ctx->shr) {
        n = snprintf(buf, 9, "%08" PRIx32, (uint32_t)(uid >> ctx->shr));
    } else {
        n = snprintf(buf, 17, "%016" PRIx64, uid);
    }

    while (n < ctx->ptlen) {
        size_t chunk = (ctx->ptlen - n) < n ? ctx->ptlen - n : n;
        memcpy(buf + n, buf, chunk);
        n += chunk;
    }

    if (ctx->obf) {
        buf[0]  = '@'; buf[3]  = '#'; buf[7]  = 'x';
        buf[9]  = 'N'; buf[11] = '?'; buf[15] = 'a';
        buf[17] = '*'; buf[20] = ')'; buf[24] = 't';
        buf[26] = 'C'; buf[29] = '?'; buf[30] = 'P';
    }

    return buf;
}

int main(int argc, char *argv[]) {
    const algo_ctx_t *algo = &ALGOS[1];
    bool verbose = false;
    int opt;

    while ((opt = getopt(argc, argv, "a:vh")) != -1) {
        switch (opt) {
            case 'a':
                int val = atoi(optarg);
                if (val < 0 || val > 2) {
                    fputs("Error: algorithm must be 0, 1, or 2\n", stderr);
                    return EXIT_FAILURE;
                }
                algo = &ALGOS[val];
                break;
            case 'v':
                verbose = true;
                break;
            case 'h':
            case '?':
                show_usage(argv[0]);
                return EXIT_FAILURE;
        }
    }

    if (optind >= argc) {
        show_usage(argv[0]);
        return EXIT_FAILURE;
    }

    const uint64_t uid = parse_uid(argv[optind]);

    if (uid == ULLONG_MAX || uid == 0) {
        return EXIT_FAILURE;
    }

    uint8_t *buf = gen_plaintext(algo, uid);

    if (verbose) {
        printf("Key: %.*s\n", AES_KEYLEN, algo->aeskey);
        printf("Plain-text: %.*s\n", algo->ptlen, buf);
    }

    struct AES_ctx aes = {0};

    AES_init_ctx(&aes, algo->aeskey, !algo->obf);

    for (size_t n = 0; n < algo->ptlen; n += AES_BLOCKLEN) {
        AES_ECB_encrypt(&aes, buf + n);
    }

    size_t outlen = !algo->obf ? algo->ptlen >> 1 : algo->ptlen;

    for (size_t n = 0; n < outlen; n++) {
        printf("%02hhx", !algo->obf ? buf[n] : buf[n] ^ (n % 16));
    }

    putchar('\n');

    free(buf);

    return EXIT_SUCCESS;
}