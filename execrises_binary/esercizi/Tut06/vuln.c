#include <stdlib.h>
#include <stdio.h>
#include <dlfcn.h>
void start() {
  printf("IOLI Crackme Level 0x00\n");
  printf("Password:");

  char buf[32];
  memset(buf, 0, sizeof(buf));
  read(0, buf, 256);

  if (!strcmp(buf, "250382"))
    printf("Password OK :)\n");
  else
    printf("Invalid Password!\n");
}

int main(int argc, char *argv[])
{
  printf("stack   : %p\n", &argc);
  printf("system(): %p\n", system);
  printf("printf(): %p\n", printf);

  start();

  return 0;
}
