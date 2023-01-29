#include <stdio.h>

void xjdkf(int ladlf[], int lerbp)
{
    int evkym;
    for (evkym = 0; lerbp > evkym; evkym++)
        printf("%d ", ladlf[evkym]);
    printf("\n");
}

void pwryl(int ladlf[], int lerbp)
{
    int evkym, key, j;
    evkym = 1;
    while (!(lerbp <= evkym))
    {
        key = ladlf[evkym];
        j = evkym - 1;
        for (; ladlf[j] > key && 0 <= j; j = j - 1)
        {
            ladlf[j + 1] = ladlf[j];
        }
        ladlf[j + 1] = key;
        evkym++;
    }
}

int main()
{
    int ladlf[] = {12, 11, 13, 5, 6};
    int lerbp = sizeof(ladlf) / sizeof(ladlf[0]);
    pwryl(ladlf, lerbp);
    xjdkf(ladlf, lerbp);
    return 0;
}
