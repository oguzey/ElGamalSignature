#include <stdio.h>
#include <linux/types.h>
#include "python2.7/Python.h"
#include <errno.h>

#include "Cypher.h"
#include "Hash.h"
#include "Log.h"

static size_t read_data(char **buff, const char *a_path)
{
    FILE *file = NULL;
    size_t size = 0;
    char *data = NULL;
    int i, c;

    if ((file = fopen(a_path, "r")) == NULL) {
        printf("Could not open file '%s'\n", a_path);
        perror("Error was");
        exit(1);
    }

    while (fgetc(file) != EOF) {
        size++;
    }
    fseek(file, 0, SEEK_SET);
    log("Will read %d bytes\n", (int)size);
    data = malloc(size);
    if (data == NULL) {
        perror("Error was");
        exit(1);
    }
    memset(data, 0, size);
    i = 0;
    while ((c = fgetc(file)) != EOF) {
        data[i++] = c;
    }
    *buff = data;
    fclose(file);
    return size;
}

static size_t get_data(__u64 **a_numbers, const char *a_path)
{
    char * data = NULL;
    size_t size = read_data(&data, a_path);
    size_t amount = size;
    if (size % 16 != 0) {
        amount = (size / 16);
        if (amount % 2 == 0) {
            amount = amount * 2 + 2;
        } else {
            amount = amount * 2 + 1;
        }
    }
    log("input size is %d\n", (int)size);
    log("pad size is %d\n", (int)(amount* 8 - size));
    log("size numbers is %d\n", (int)amount);
    __u64 *numbers = malloc(sizeof(__u64) * amount);
    memset(numbers, 0, sizeof(__u64) * amount);

    size_t i = 0, k = 0;

    for (i = 0; i < amount; ++i) {
        __u64 tmp;
        for (k = i * 8; k <(i + 1)*8 && k < size; ++k) {
            tmp = data[k];
            tmp <<= (7 - k % 8) * 8;
            numbers[i] += tmp;
        }

        if (k == size && k != (i + 1)*8 ) {
            tmp = 0x80;
            tmp <<= (7 - k % 8) * 8;
            numbers[i] += tmp;
            break;
        }
    }
    free(data);
    *a_numbers = numbers;
    return amount;
}

static __u64 wrap_hash_calculate(const char *a_path)
{
    __u64 *input = NULL;
    size_t size = get_data(&input, a_path);

    log("Input data is %s", "");
    int i = 0;
    for (; i < size; ++i) {
        log("%llx  ", input[i]);
    }
    log("\n%s", "");
    __u64 output = hash_calculate(input, size);

    log_hexlong(output);

    return output;
}

static PyObject* py_hash_calc(PyObject* self, PyObject* args)
{
    const char *path;

    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    log("Path provide '%s'\n", path);
    __u64 out = wrap_hash_calculate(path);
    return Py_BuildValue("K", out);
}

/*
 * Bind Python function names to our C functions
 */
static PyMethodDef hash_methods[] = {
  {"get_hash", py_hash_calc, METH_VARARGS, "Calculate hash!"},
  {NULL, NULL}
};

/*
 * Python calls this to let us initialize our module
 */
PyMODINIT_FUNC inithashModule(void)
{
  (void) Py_InitModule("hashModule", hash_methods);
}
