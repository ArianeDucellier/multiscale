#include <stdio.h>

int main()
{
enum { BigEndian, LittleEndian };

//int endianness(void)
//{
    union
    {
        int  i;
        char b[sizeof(int)];
    } u;
    u.i = 0x01020304;
    if (0x04 == u.b[0])
        printf("Little endian\n");
    else if (0x01 == u.b[0])
        printf("Big endian\n");
//    return (u.b[0] == 0x01) ? LittleEndian : BigEndian;
//}

//int result;
//result = endianness();
//printf("%d", result);

return 0;
}

