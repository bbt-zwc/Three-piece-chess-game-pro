#include "stm32f10x.h"              
#include "Delay.h"
#include "Motor.h"
#include "Servo.h" 
#include "Serial.h" 
//dir是方向1，齧ou是距离
void x_move(uint32_t dir,uint32_t num,uint32_t speed)
{
	if(dir==1)//正
	{
		
		Motor_Run_1(1,num,speed);
		Motor_Run_2(1,num,speed);
	}
	
	if(dir==0)//反
	{
	Motor_Run_1(0,num,speed);
	Motor_Run_2(0,num,speed);
	}
	
}

void y_move(uint32_t dir,uint32_t num,uint32_t speed)
{
	if(dir==1)//正
	{
		Motor_Run_1(1,num,speed);
		Motor_Run_2(0,num,speed);
	}
	
	if(dir==0)//反
	{
	Motor_Run_1(0,num,speed);
	Motor_Run_2(1,num,speed);
	}
	
}



