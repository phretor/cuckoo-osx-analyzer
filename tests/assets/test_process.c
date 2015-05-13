#include <unistd.h>
#include <stdio.h>

void parent(void)
{
  pid_t pid;

  pid = getpid();

  printf("I'm the parent and my PID is %d\n", pid);
}

void child(void)
{
  pid_t pid;
  pid_t ppid;

  pid = getpid();
  ppid = getppid();

  printf("I'm the child and my PID is %d (parent PID is %d)\n", pid, ppid);
}

int main(int argc, char* argv[])
{
  pid_t p;

  p = fork();

  printf("Welcome to the args! %s %s", argv[1], argv[2]);

  if (p == 0) {
    child();
  } else {
    parent();
  }

  return 0;
}
