#include "stm32f10x.h"   
#include "Motor.h"   
#include "Delay.h" 
#include "Servo.h" 
#include "Serial.h" 
void saomiao()
{
if (GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)		
	{
		Delay_ms(20);		
		Motor_Run_1(1,0,70);
		Motor_Run_2(1,0,70);
	}			
	
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
	
	Motor_Run_1(1,50,70);
	 Delay_ms(1000);
	Motor_Run_2(0,50,70);
	 Delay_ms(1000);
	
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
	
}


void zhuaqizi(uint32_t num)
{
  if(num==1)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }

 if(num==2)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
 if(num==3)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
 if(num==4)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
 if(num==5)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
 if(num==6)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
 if(num==7)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  } 
	if(num==8)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
  if(num==9)
  {
	Motor_Run_1(1,50,70);//水平扫描
		Delay_ms(1000);
  Motor_Run_2(1,50,70);//竖直扫描
    Delay_ms(1000);
  }
}
void Key_Init2(void)//dui ying fuwei han shu
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);	

	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1 | GPIO_Pin_11;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOB, &GPIO_InitStructure);
}


void  fuwei(void)
{
 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_1) == 0)
 {
	Motor_Run_1(1,0,70);
 }
 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
 {
	Motor_Run_2(1,0,70);
 }
 
  Motor_Run_2(1,50,70);
  Motor_Run_1(1,50,70); 
}


void  huoer(uint32_t num)//gai guan jiao
{
	if(num==1)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)//gai pin 
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==2)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==3)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==4)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==5)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==6)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==7)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==8)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
		if(num==9)
	{
		 if(GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0)
     {
	  Servo_SetAngle(60);
     }
	}
	
	
}
void  zhuafang(void)	
{
	static uint8_t a = 0;
	static uint8_t b = 0;
if(Serial_RxPacket1[0]==1&&a==0)
{
  GPIO_ResetBits(GPIOA, GPIO_Pin_7);	//dianji guanbi
	
  GPIO_SetBits(GPIOA, GPIO_Pin_7);	//kaiqi dian ci tie 
	Delay_ms(500);
	a=1;
	b=1;//zhi zhixing yici
}
//Delay_ms(500);
  GPIO_SetBits(GPIOA, GPIO_Pin_7);//再次开启电机
if(b==1 && GPIO_ReadInputDataBit(GPIOB, GPIO_Pin_2) == 0 && Serial_RxPacket1[2]==9 )//fang
  {
   GPIO_ResetBits(GPIOA, GPIO_Pin_7);//关闭电机
   GPIO_SetBits(GPIOA, GPIO_Pin_7);//kaiqi dian ci tie
		b=0;
	}  
   GPIO_SetBits(GPIOA, GPIO_Pin_7);//再次开启电机
}


