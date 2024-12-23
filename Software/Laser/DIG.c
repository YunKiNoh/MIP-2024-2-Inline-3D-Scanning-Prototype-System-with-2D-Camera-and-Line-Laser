#include "stm32f411xe.h"
#include "math.h"
#include "ecPinNames.h"
#include "ecGPIO.h"
#include "ecSysTick.h"
#include "ecRCC.h"
#include "ecTIM.h"
#include "ecPWM.h"

// Definition PWM Port, Pin
#define PWM_PIN PA_1

// System clock frequency (84 MHz)
#define F_CLK 84000000  

// Desired PWM frequency (e.g., 400,000Hz)
#define F_PWM 90000   

void setup(void);

int main(void) {
    setup();   
    while (1) {
        // Main loop
    }
}

void setup(void) {   
    // System clock setting: frequency = 84 MHz
    RCC_PLL_init();

    // PWM pin setting
    GPIO_init(GPIOA, PWM_PIN, AF);         // Set PA1 as alternate function (AF)
    GPIO_otype(GPIOA, PWM_PIN, EC_PUSH_PULL);
    GPIO_pupd(GPIOA, PWM_PIN, 0);
    GPIO_ospeed(GPIOA, PWM_PIN, EC_FAST);
   
    // Timer settings for PWM
    TIM_TypeDef *TIMx = TIM2;              // Use TIM2
    int PSC = 0;                           // Prescaler (initial value)
    int ARR = (int)((F_CLK / (F_PWM * (PSC + 1))) - 1);  // Auto-reload value calculation

    // Check if ARR exceeds 65535 (16-bit timer limit)
    while (ARR > 65535) {
        PSC++;                             // Increase prescaler
        ARR = (int)((F_CLK / (F_PWM * (PSC + 1))) - 1);  // Recalculate ARR
    }

    // Apply calculated values to timer
    TIMx->PSC = PSC;                       // Set prescaler
    TIMx->ARR = ARR;                       // Set auto-reload value
    
    // Initialize PWM
    PWM_init(PWM_PIN);                     // Initialize PWM on the defined pin
    PWM_duty(PWM_PIN, 0.5);                // Set duty cycle to 50%
}
