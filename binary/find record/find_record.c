#include <stdio.h>
#include <string.h>

typedef struct {
    char name[50];
    int age;
    char address[100];
} Record;

Record database[] = {
    {"Alice", 25, "123 Main St"},
    {"Bob", 30, "456 Elm St"},
    {"Charlie", 35, "789 Oak St"}
};

void secret_function() {
    printf("Access granted to sensitive data!\n");
}

void find_record(char *name) {
    char buffer[50];
    strcpy(buffer, name);
    
    for (int i = 0; i < 3; i++) {
        if (strcmp(buffer, database[i].name) == 0) {
            printf("Record found: %s, %d, %s\n", database[i].name, database[i].age, database[i].address);
            return;
        }
    }
    printf("No record found for %s\n", buffer);
}

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Usage: %s <name>\n", argv[0]);
        return 1;
    }
    find_record(argv[1]);
    return 0;
}

