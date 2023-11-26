#include <stdio.h>
#include <string.h>


void greet_me(){
  char name[200];
  gets(name);
  printf("Hi there %s !\n",name);
}

int main(int argc, char *argv[]){

  greet_me();
  return 0;
}

