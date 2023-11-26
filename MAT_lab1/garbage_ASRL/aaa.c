#import <stdio.h>

int main(){
    char a[12];
    sprintf(a, "%p", &puts);
    puts(a);
}
