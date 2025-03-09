#ifndef __MOTOR_H
#define __MOTOR_H

void Motor_Init(void);
void Motor_Run_1(uint32_t dir,uint32_t num,uint32_t speed);
void Motor_Run_2(uint32_t dir,uint32_t num,uint32_t speed);
void grasp_move(uint32_t motor_number);
void put_move(uint32_t motor_number);
void Motor_Run_3(uint32_t dir,uint32_t num,uint32_t speed);  
#endif
