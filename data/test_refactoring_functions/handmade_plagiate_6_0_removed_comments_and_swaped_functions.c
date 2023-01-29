#include <stdio.h>
#include <stdlib.h>

void cipher(char str[], int shift, int maxlength)
{
  for (int i = 0; i < maxlength; ++i)
    shiftChar(&str[i], shift);
}

void shiftChar(char *p_char, int shift)
{
  if ('A' <= *p_char && *p_char <= 'Z')
  {
    *p_char += shift;
    if (*p_char > 'Z')
      *p_char -= 26;
    if (*p_char < 'A')
      *p_char += 26;
  }
  else if ('a' <= *p_char && *p_char <= 'z')
  {
    if (*p_char + shift < 'a')
      shift += 26;
    if (*p_char + shift > 'z')
      shift -= 26;
    *p_char += shift;
  }
}

int main()
{
  char str[50] = "Froh zu sein bedarf es wenig";
  int shift = 5;
  printf("Original: ");
  printf("%s\n", str);

  cipher(str, shift, 50);
  printf("Verschluesselt: ");
  printf("%s\n", str);

  cipher(str, -shift, 50);
  printf("Entschluesselt: ");
  printf("%s\n", str);
}