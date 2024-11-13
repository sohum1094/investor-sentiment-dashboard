/**
 * mapreduce
 * CS 341 - Fall 2024
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "mapper.h"

void replace_chars(char *str) {
    while (*str) {
        // Replace specific special characters with space before handling ':'
        if (*str == ')' || *str == '(' || *str == '|' || *str == '&' || *str == '!' ||
            *str == '@' || *str == '#' || *str == '^' || *str == '*' || *str == '-' ||
            *str == '+' || *str == '~' || *str == '"' || *str == ';' || *str == '.' ||
            *str == ',' || *str == '?' || *str == '/' || *str == '_' || *str == '[' ||
	    *str == ']' || *str == ':' ) {
            *str = ' ';
        } else if (*str == ':') {
            *str = ';';
        } else if (*str == '\n') {
            *str = ' ';
        } else if (*str >= 'A' && *str <= 'Z') {
            *str = *str + ('a' - 'A');
        }
        str++;
    }
}

void mapper(const char *data, FILE *output) {
    char *data_copy = strdup(data);
    if (data_copy)
        replace_chars(data_copy);
    char *datum = strtok(data_copy, " ");
    while (datum) {
        // the difference is just a few pixels :-)
        fprintf(output, "%s: 1\n", datum);
        datum = strtok(NULL, " ");
    }

    free(data_copy);
}

MAKE_MAPPER_MAIN(mapper)
