#include "stm32f10x.h"              
#include "Delay.h"
#include "Motor.h"
#include "Servo.h" 
#include "Serial.h" 
//dir�Ƿ���1���mou�Ǿ���
void x_move(uint32_t dir,uint32_t num,uint32_t speed)
{
	if(dir==1)//��
	{
		
		Motor_Run_1(1,num,speed);
		Motor_Run_2(1,num,speed);
	}
	
	if(dir==0)//��
	{
	Motor_Run_1(0,num,speed);
	Motor_Run_2(0,num,speed);
	}
	
}

void y_move(uint32_t dir,uint32_t num,uint32_t speed)
{
	if(dir==1)//��
	{
		Motor_Run_1(1,num,speed);
		Motor_Run_2(0,num,speed);
	}
	
	if(dir==0)//��
	{
	Motor_Run_1(0,num,speed);
	Motor_Run_2(1,num,speed);
	}
	
}



