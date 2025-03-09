#include "stm32f10x.h"
#include "Delay.h"

void Motor_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);//开启GPIOA的时钟
	
	GPIO_InitTypeDef  GPIO_InitStructure;
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_4 | GPIO_Pin_3| GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8|GPIO_Pin_11 | GPIO_Pin_12| GPIO_Pin_15;  //PA5->EN;PA4->DIR;PA3->PWM
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  GPIO_SetBits(GPIOA, GPIO_Pin_5 | GPIO_Pin_4| GPIO_Pin_3| GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8|GPIO_Pin_11 | GPIO_Pin_12| GPIO_Pin_15);	
}

//dir方向，1正向0反向；num圈数；speed是脉冲高低电平时间
void Motor_Run_1(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==1)//左
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_4);		
		GPIO_SetBits(GPIOA, GPIO_Pin_7);		
	}
	
	if(dir==0)//右
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);	
		GPIO_ResetBits(GPIOA, GPIO_Pin_7);
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //电平翻转2次为一个脉冲，所以旋转一周需要3200个脉冲，
	{		
		Delay_us(speed);                   //高低电平持续时间，脉冲频率
		GPIOA->ODR ^= GPIO_Pin_3; 
    GPIOA->ODR ^= GPIO_Pin_6;  		//翻转PA3输出电平
	}	
}

void Motor_Run_2(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==0)//下
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);
		GPIO_SetBits(GPIOA, GPIO_Pin_7);		
	}
	
	if(dir==1)//上
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_4);	
		GPIO_ResetBits(GPIOA, GPIO_Pin_7);			
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //电平翻转2次为一个脉冲，所以旋转一周需要3200个脉冲，
	{		
		Delay_us(speed);                   //高低电平持续时间，脉冲频率
		GPIOA->ODR ^= GPIO_Pin_6; 
    GPIOA->ODR ^= GPIO_Pin_3; 		//翻转PA3输出电平
	}	
}

void Motor_Run_3(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==1)//上
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_12);		
	}
	
	if(dir==0)//下
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_12);	
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //电平翻转2次为一个脉冲，所以旋转一周需要3200个脉冲，
	{		
		Delay_us(speed);                   //高低电平持续时间，脉冲频率
		GPIOA->ODR ^= GPIO_Pin_11; 
    		//翻转PA3输出电平
	}	
}
void put_move(uint32_t motor_number)
{
   switch (motor_number)
	 {
		 case 1 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 2 :
		Motor_Run_1(1,1,80);
		Motor_Run_2(1,1,80);
		 break; 
			case 3 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
			case 4 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 5 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 6 :
		Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 7 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 8 :
				Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 9 :
				Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		 }	 
}
void grasp_move(uint32_t motor_number)
{
 switch (motor_number)
	{
	 case 10:
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 11 :
		Motor_Run_1(1,1,80);
		Motor_Run_2(1,1,80);
		 break; 
			case 12 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
			case 13:
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 14 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 15 :
		Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 16 :
			Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 17 :
				Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		  case 18 :
				Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
			  case 19 :
				Motor_Run_1(1,1,80);
			Motor_Run_2(1,1,80);
		 break;
		 }	 
		 
 }





