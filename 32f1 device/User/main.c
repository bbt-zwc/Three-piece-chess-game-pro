#include "all.h"                  // Device header

uint8_t flag=1;
uint8_t X=0;
uint8_t Y=0;
int a,b,c,d,e;
int main(void)
{	
	OLED_Init();
	Motor_Init();
	Serial1_Init();	
  Serial3_Init();	
	Elm_Init();
	Key_Init();
	uint8_t KeyNum;
	Delay_ms(1000);	
	
	
	Serial_TxPacket[0] = 1;
	Serial_TxPacket[1] = 0;
	Serial_TxPacket[2] = 0;
	Serial_TxPacket[3] = 0;

	
	while(1)
	{
	KeyNum = Key_GetNum();
	if (KeyNum == 1)			//????0
		{
		Serial_SendPacket();			//??
		}
	if (Serial_GetRxFlag1() == 0)	
		{
			Delay_ms(50);
		}	
	if (Serial_GetRxFlag1() == 1)	
		{
			OLED_ShowHexNum(2, 1, Serial_RxPacket1[1], 2);	
			OLED_ShowHexNum(2, 4, Serial_RxPacket1[2], 2);
			OLED_ShowHexNum(2, 7, Serial_RxPacket1[3], 2);
			OLED_ShowHexNum(2, 10,Serial_RxPacket1[4], 2);
      OLED_ShowHexNum(2, 13,Serial_RxPacket1[5], 2);
		
		a=Serial_RxPacket1[1];b=Serial_RxPacket1[2];c=Serial_RxPacket1[3];d=Serial_RxPacket1[4];e=Serial_RxPacket1[5];
		
		OLED_ShowNum(3, 1,b, 2);OLED_ShowNum(3, 4,c, 2);
	if(a == 3)
	{
		OLED_ShowString(1,1,"???? fuck !!!!");
	}
	if(a != 3)
	{
			if(d==2)
		{
			 OLED_ShowString(1,1,"black win");
		gogogo(b,c);
		}
			if(d==1)
		{
			 OLED_ShowString(1,1,"white win");
		gogogo(b,c);
		}
			if(d==0)
		{
			 OLED_ShowString(1,1,"draw");
		gogogo(b,c);
		}
			if(d==3)
		{
			OLED_ShowString(1,1,"continue");
		gogogo(b,c);
		}
		}
		}
//		先复赋值再清零
	a = 0;b = 0;c = 0;d = 0;d = 0;e = 0;
}
}
