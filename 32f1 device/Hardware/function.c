#include "stm32f10x.h"
#include "Delay.h"
#include "position.h"
#include "Motor.h"
#include "function.h"

int x,y,go1,go2;
int speed = 150;
extern int pxy[20][2];

void Elm_Init(void)
{
RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);
}

void Elm_open(int a)
{
	if(a==1)
	{
		GPIO_SetBits(GPIOA, GPIO_Pin_0);	
	}	
	if(a==0)
	{
		GPIO_ResetBits(GPIOA, GPIO_Pin_0);	
	}	
}

void take_qi(int b)
{
//Delay_ms(500);//*抖动
	Motor_Run_3(0,6,speed) ; 
	Elm_open(b);
  Delay_ms(300);//*抖动
	Motor_Run_3(1,6,speed) ; 
}	


void gogogo(int p11,int p12)
{
	
	Motor_Run_3(1,6,speed) ;
	
	//*从原点到p1位置
//	p11 = 19;
//		p12 = 13;
		x = pxy[p11][0];
		y = pxy[p11][1];
		go1 = 1;
		go2 = 1;
		Motor_Run_1(go1,x,speed);
		Motor_Run_2(go2,y,speed);
		take_qi(1);
		Delay_ms(300);
		//*再到p2位置
		if(pxy[p12][0]>=pxy[p11][0])
		{
			go1 = 1;
			x = pxy[p12][0] - pxy[p11][0];
		}
		if(pxy[p12][0]<pxy[p11][0])
		{
			go1 = 0;
			x = pxy[p11][0] - pxy[p12][0];
		}
		if(pxy[p12][1]>=pxy[p11][1])
		{
			go2 = 1;
			y = pxy[p12][1] - pxy[p11][1];
		}
		if(pxy[p12][1]<pxy[p11][1])
		{
			go2 = 0;
			y = pxy[p11][1] - pxy[p12][1];
		}
		Motor_Run_1(go1,x,speed);
		Motor_Run_2(go2,y,speed);
		take_qi(0);
		Delay_ms(300);
		//*再回到原点
		x = pxy[p12][0];
		y = pxy[p12][1];
		go1 = 0;
		go2 = 0;
		Motor_Run_1(go1,x,speed);
		Motor_Run_2(go2,y,speed);
		Delay_ms(300);
		Motor_Run_3(0,6,speed) ; 
	
}
