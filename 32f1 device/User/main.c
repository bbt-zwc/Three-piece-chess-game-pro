#include "all.h"                  // Device header

uint8_t i,j,k;
uint8_t X=0;
uint8_t Y=0;
uint8_t qi[9];
int a,b,c,d,e,F;
int jiao;
int hh = 1;
 
extern int pxy[20][2];

int main(void)
{	
	OLED_Init();
	Motor_Init();
	Serial1_Init();	
  Serial3_Init();	
	Elm_Init();
	Key_Init();
	uint8_t KeyNum;
	Delay_ms(500);	
	
	
	Serial_TxPacket[0] = 1;
	Serial_TxPacket[1] = 0;
	Serial_TxPacket[2] = 0;
	Serial_TxPacket[3] = 0;

//Motor_Run_1(1,50,150);
//	Motor_Run_2(1,50,150);
	while(1)
	{
		Serial_TxPacket[0] = 1;
//		F=;
//	OLED_ShowNum(1, 4,F, 2);
	KeyNum = Key_GetNum();
	if (KeyNum == 1)			//????0
		{
		Serial_SendPacket();			//??
		}
	if (Serial_GetRxFlag1() == 0)	
		{
			Delay_ms(10);
		}	
if (Serial_GetRxFlag1() == 1)	
	{
		  OLED_ShowHexNum(1, 13, Serial_RxPacket1[10], 1);
			OLED_ShowHexNum(2, 1, Serial_RxPacket1[0], 2);	
			OLED_ShowHexNum(2, 4, Serial_RxPacket1[1], 2);
			OLED_ShowHexNum(2, 7, Serial_RxPacket1[2], 2);
			OLED_ShowHexNum(2, 10,Serial_RxPacket1[3], 2);
      OLED_ShowHexNum(2, 13,Serial_RxPacket1[4], 2);
			OLED_ShowHexNum(3, 1,Serial_RxPacket1[5], 2);
			OLED_ShowHexNum(3, 4,Serial_RxPacket1[6], 2);
			OLED_ShowHexNum(3, 7,Serial_RxPacket1[7], 2);
			OLED_ShowHexNum(3, 10,Serial_RxPacket1[8], 2);
			OLED_ShowHexNum(3, 13,Serial_RxPacket1[9], 2);
		  jiao=Serial_RxPacket1[9];
			F=Serial_RxPacket1[10];
//		if(hh == 1)
//			{
//	   	rotateCoordinates(jiao);
//				hh = 2;
//			}
	
	//*下棋程序
if (F == 1)
	{
		a=Serial_RxPacket1[0];b=Serial_RxPacket1[1];c=Serial_RxPacket1[2];d=Serial_RxPacket1[3];e=Serial_RxPacket1[4];
		OLED_ShowNum(4, 1, b, 2);OLED_ShowNum(4, 4, c, 2);
	if(a == 3)
	{
		OLED_ShowString(1,1,"???? fuck !!!!");
	}
	if(a != 3)
	{
			if(d==2)
		{
			Serial_TxPacket[0] = 2;
			OLED_ShowString(1,1,"black win");
			gogogo(b,c);
			Serial_SendPacket();			//??
		}
			if(d==1)
		{
			Serial_TxPacket[0] = 2;
			OLED_ShowString(1,1,"white win");
			gogogo(b,c);
			Serial_SendPacket();			//??
		}
			if(d==0)
		{
			Serial_TxPacket[0] = 2;
			OLED_ShowString(1,1,"draw");
			gogogo(b,c);
			Serial_SendPacket();			//??
		}
			if(d==3)
		{
			OLED_ShowString(1,1,"continue");
		gogogo(b,c);
		}
	}
  }

//*下棋结束，复位程序
if(F == 2)
{
	j=0;k=0;
	for(i=0;i<9;i++)
	{
		qi[i]=Serial_RxPacket1[i];
		b = 1+i;
		if(qi[i]==1)//白色
		{
		c = 15+j;
		OLED_ShowString(1,1,"resetting...");
		OLED_ShowNum(4, 1,b, 2);OLED_ShowNum(4, 4,c, 2);
	  gogogo(b,c);
			j++;
		}
		if(qi[i]==2)//黑色
		{
		c = 10+k;
		OLED_ShowString(1,1,"resetting...");
		OLED_ShowNum(4, 1,b, 2);OLED_ShowNum(4, 4,c, 2);
	  gogogo(b,c);
			k++;
		}
	}
	
		Serial_TxPacket[0] = 3;
		Serial_SendPacket();			//??
}
}
//		先复赋值再清零
	a = 0;b = 0;c = 0;d = 0;d = 0;e = 0; 
}
	
}

