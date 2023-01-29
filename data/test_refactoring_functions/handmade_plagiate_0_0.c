#include <stdio.h>

int main(int argc, char *argv[])
{
  int sammelzaehler = 0;
  char kollektion[100] = "";
  for (int j = 1; j < argc; j++)
  {
    for (char *p = argv[j]; (*p) != '\0'; p++)
    {
      if ((*p != 'x') && (*p != 'y') && (*p != 'q') && (*p != 'X') && (*p != 'Y') && (*p != 'Q'))
      {
        kollektion[sammelzaehler] = *p;
        sammelzaehler++;
      }
    }
  }
  kollektion[sammelzaehler] = '\0';
  printf("x,y,q und X,Y,Q aussortiert: %s\n", kollektion);
  char neuerString[100] = "";
  int i = 0;
  for (; i < sammelzaehler; i += 3)
  {
    neuerString[i / 3] = kollektion[i];
  }
  neuerString[i / 3] = '\0';
  printf("Der neue String lautet: %s \n", neuerString);
}
