#include <stdio.h>
#include <stdlib.h>

void umdrehen(char *str)
{
  char tmp = 0;
  int strLen = 0;
  for (; str[strLen] != '\0'; strLen++)
    ;
  for (int i = 0; i < strLen / 2; i++)
  {
    tmp = str[i];
    str[i] = str[strLen - i - 1];
    str[strLen - i - 1] = tmp;
  }
}

void ersetzen(char *dest, int zahl, char *src)
{
  for (int i = 0; i < zahl; i++)
  {
    if (dest[i] == '\0' || src[i] == '\0')
      break;
    dest[i] = src[i];
  }
}

int main(int argc, char *argv[])
{
  char test[11] = "0123456789";
  printf("Das Original ist: %s \n", test);
  ersetzen(test, atoi(argv[1]), argv[2]);
  printf("Ersetzt : %s \n", test);
  umdrehen(test);
  printf("Rückwärts : %s \n", test);
}