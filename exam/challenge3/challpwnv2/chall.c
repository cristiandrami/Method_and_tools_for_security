#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void getDateAndTime() {
    printf("the current system date and time is: \n");
    system("date");
}

// Function to construct an interesting command string
void constructHiddenCommand(char* buffer) {
    char cmd[] = {99, 97, 116, 32, 47, 116, 109, 112, 47, 102, 108, 97, 103, 46, 116, 120, 116, 0};
    for (int i = 0; i < sizeof(cmd); ++i) {
        buffer[i] = cmd[i];
    }
}

char hiddenCmdBuffer[23] __attribute__((section(".data")));

void vulnerableFunction() {
    char buffer[40];
    printf("Enter your name: ");
    fflush(stdout);
    read(STDIN_FILENO, buffer, 80); 
    printf("Hello user %s: ", buffer);
    getDateAndTime();
}

int main(int argc, char **argv) {
    constructHiddenCommand(hiddenCmdBuffer);
    // Disable buffering for stdout
    setbuf(stdout, NULL);
    vulnerableFunction();
    return 0;
}

