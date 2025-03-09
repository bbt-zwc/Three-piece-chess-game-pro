#include "stm32f10x.h"
#include "Delay.h"

void Motor_Init(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);//����GPIOA��ʱ��
	
	GPIO_InitTypeDef  GPIO_InitStructure;
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_4 | GPIO_Pin_3| GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8|GPIO_Pin_11 | GPIO_Pin_12| GPIO_Pin_15;  //PA5->EN;PA4->DIR;PA3->PWM
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_Init(GPIOA, &GPIO_InitStructure);
  GPIO_SetBits(GPIOA, GPIO_Pin_5 | GPIO_Pin_4| GPIO_Pin_3| GPIO_Pin_6 | GPIO_Pin_7 | GPIO_Pin_8|GPIO_Pin_11 | GPIO_Pin_12| GPIO_Pin_15);	
}

//dir����1����0����numȦ����speed������ߵ͵�ƽʱ��
void Motor_Run_1(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==1)//��
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_4);		
		GPIO_SetBits(GPIOA, GPIO_Pin_7);		
	}
	
	if(dir==0)//��
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);	
		GPIO_ResetBits(GPIOA, GPIO_Pin_7);
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //��ƽ��ת2��Ϊһ�����壬������תһ����Ҫ3200�����壬
	{		
		Delay_us(speed);                   //�ߵ͵�ƽ����ʱ�䣬����Ƶ��
		GPIOA->ODR ^= GPIO_Pin_3; 
    GPIOA->ODR ^= GPIO_Pin_6;  		//��תPA3�����ƽ
	}	
}

void Motor_Run_2(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==0)//��
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_4);
		GPIO_SetBits(GPIOA, GPIO_Pin_7);		
	}
	
	if(dir==1)//��
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_4);	
		GPIO_ResetBits(GPIOA, GPIO_Pin_7);			
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //��ƽ��ת2��Ϊһ�����壬������תһ����Ҫ3200�����壬
	{		
		Delay_us(speed);                   //�ߵ͵�ƽ����ʱ�䣬����Ƶ��
		GPIOA->ODR ^= GPIO_Pin_6; 
    GPIOA->ODR ^= GPIO_Pin_3; 		//��תPA3�����ƽ
	}	
}

void Motor_Run_3(uint32_t dir,uint32_t num,uint32_t speed)  
{
	if(dir==1)//��
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_12);		
	}
	
	if(dir==0)//��
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_12);	
	}
	
	for(uint32_t i=0;i<=(num*100);i++)  //��ƽ��ת2��Ϊһ�����壬������תһ����Ҫ3200�����壬
	{		
		Delay_us(speed);                   //�ߵ͵�ƽ����ʱ�䣬����Ƶ��
		GPIOA->ODR ^= GPIO_Pin_11; 
    		//��תPA3�����ƽ
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





