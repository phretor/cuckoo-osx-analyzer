#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
  int i;

  printf("Entering main\n");

  for (i = 0; i < 5; i++) {
    fprintf(stdout, "Hello %d %s\n", i, argv[1]);
    fprintf(stderr, "The hell is here %d %s\n", i, argv[1]);
    sleep(1);
  }
}
