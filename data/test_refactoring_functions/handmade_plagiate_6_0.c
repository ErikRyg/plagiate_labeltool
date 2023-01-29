#include <stdio.h>
#include <stdlib.h>

/*
 * Bekommt einen Pointer auf ein beliebiges Zeichen und einen Wert shift uebergeben.
 * Shiftet alle Zeichen aus dem Bereich a-z und A-Z um den Wert shift.
 * An den Wertebereichsgrenzen findet ein Umlauf statt (Beispielsweise:
 * nach Z folgt A, vor A liegt Z, nach z folgt a und vor a liegt z).
 * Zahlen ausserhalb des Bereichs werden unveraendert zurueckgegeben.
 * Veraendert das referenzierte Zeichen direkt.
 */
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
    //		if (*p_char > 'z') *p_char -= 26;
    //		if (*p_char < 'a') *p_char += 26;
    /* so funktioniert das leider nicht. Wenn man einen kleinen Buchstaben
     * zu weit verschiebt, dann ist dieser aus dem ASCII-Bereich draußen und
     * es kommt zu Fehlern beim Zurückschieben
     */
  }
}

/*
 * Bekommt einen beliebigen char-Array der Laenge maxlength uebergeben.
 * Fuehrt auf jedem Zeichen des Arrays die shiftChar-Funktion aus.
 * Das uebergebene originale Array wird dabei veraendert.
 */
void cipher(char str[], int shift, int maxlength)
{
  for (int i = 0; i < maxlength; ++i)
    shiftChar(&str[i], shift);
}

/*
 * Testprogramm, das Strings mit dem Caesar-Chiffre chiffrieren kann.
 * Es benutzt dazu die cipher-Funktion.
 */
int main()
{
  char str[50] = "Froh zu sein bedarf es wenig"; // Originaltext
  int shift = 5;
  printf("Original: ");
  printf("%s\n", str);

  // Verschluesseln
  cipher(str, shift, 50);
  printf("Verschluesselt: ");
  printf("%s\n", str);

  // Entschluesseln
  cipher(str, -shift, 50);
  printf("Entschluesselt: ");
  printf("%s\n", str);
}