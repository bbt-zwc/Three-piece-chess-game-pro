//20��λ������xy,����װ��2�������Զ�������Ͻ�Ϊԭ�㣬����x+������y+
#include "stm32f10x.h"
#include "Delay.h"
#include "position.h"
#include "math.h" 

#include "OLED.h"
             
#ifndef PI  
#define PI 3.14159265358979323846  
#endif  


int pxy[20][2] = {
	{0,0}, //*0������
	{121,97},//*1������
	{151,97},//*2������
	{182,97},//*3������
	{121,128},//*4������
	{151,128},//*5������
	{182,128,},//*6������
	{122,158},//*7������
	{152,158},//*8������
	{183,158},//*9������
	{79,80},//*10������
	{79,103},//*11������
	{79,127},//*12������
	{80,150},//*13������
	{80,173},//*14������
	{225,81},//*15������
	{225,104},//*16������
	{225,128},//*17������
	{226,151},//*18������
	{226,175}//*19������
};


void rotateCoordinates(int angleDegrees)
{
	//	              pxy[1][0]=pxy[1][0]-2;
    if  (angleDegrees<47&angleDegrees>43)
		{
		  angleDegrees=45;
		}
		
    float angleRadians = (90-(angleDegrees-45))* PI / 180.0;  
    
    for (int i = 1; i < 10; i++)
		{  
        if (i == 5) {  
            
            pxy[i][0] = 151;  
            pxy[i][1] = 128;  
        } 
				else 
				{  
					
            float relativeX = pxy[i][0] - 151;  
            float relativeY = pxy[i][1] - 128;  
            pxy[i][0] = relativeX * cos(angleRadians) - relativeY * sin(angleRadians) + 151;  
            pxy[i][1] = relativeX * sin(angleRadians) + relativeY * cos(angleRadians) + 128;
OLED_ShowNum(4, 10,pxy[1][0], 2);
OLED_ShowNum(4, 13,pxy[1][1], 2);					
        }  
    }  
}
	