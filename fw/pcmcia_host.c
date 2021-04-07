#include <avr/io.h>
#include <util/delay.h>

static inline unsigned char rx(void)
{
	while ( !(UCSR0A & (1<<RXC0)) );
	return UDR0;
}

static inline void tx(unsigned char byte)
{
	while ( !( UCSR0A & (1<<UDRE0)) );
	UDR0 = byte;
}

int main(void)
{
#define BAUD 76800
#include <util/setbaud.h>

	UBRR0H = UBRRH_VALUE;
	UBRR0L = UBRRL_VALUE;
	#if USE_2X
	UCSR0A |= (1 << U2X0);
	#else
	UCSR0A &= ~(1 << U2X0);
	#endif
	PORTA = 0x0F; // set 1 on OE,WE,CE1,CE2
	DDRA = 0x0F;
	DDRB = 0xFF; //A16-A23
	DDRC = 0xFF; //A8-A15
	PORTD = 0x8C; // set 1 on IORD,IOWR,REG
	DDRD = 0xFF;
	PORTE = 0xFF; // reset pullup
	DDRE = 0x02;
	DDRF = 0xFF; //A0-A7
	PORTH = 0xFF; // pullups
	DDRH = 0x00;
	DDRK = 0x00; // D8-D15
	DDRL = 0x00; // D0-D7
	while(1)
	{
		switch(rx())
		{
			default:
			case 0x00: //RESET_STATE
				break;
			case 0x01: //GET_CD_VS
				tx(PINH);
				break;
			case 0x02: //SET_RESET
				DDRE |= 1<<3;
				if(rx())
					PORTE&=~(1<<3); //CBI(RESET)
				else
					PORTE|=1<<3; //SBI(RESET)
				break;
			case 0x03: //GET_ATTR_MEMORY
				PORTD&=~(1<<2); //SBI(REG)
				PORTD = (PORTD&0xFC) | (rx()&0x03); // A24-A25
				PORTB = rx(); //A16-A23
				PORTC = rx(); //A8-A15
				PORTF = rx(); //A7-A0
				PORTA &=~(1<<2); //CE1=0
				PORTA |=1<<3; //CE2=1
				PORTA |=1<<0; //OE=1
				asm volatile("nop");
				asm volatile("nop");
				PORTA &=~(1<<0); //OE=0
				asm volatile("nop");
				while(!(PINA&(1<<7))); //loop  until !WAIT
				asm volatile("nop");				
				tx(PINL);
				PORTA |=(1<<0); //OE=1
				break;
			case 0x04: //SET_ATTR_MEMORY
				PORTD&=~(1<<2); //SBI(REG)
				PORTD = (PORTD&0xFC) | (rx()&0x03); // A24-A25
				PORTB = rx(); //A16-A23
				PORTC = rx(); //A8-A15
				PORTF = rx(); //A7-A0
				PORTA &=~(1<<2); //CE1=0
				PORTA |=1<<3; //CE2=1
				PORTA |=1<<0; //OE=1
				PORTL = rx(); //data
				DDRL = 0xFF; //enable output
				asm volatile("nop");
				asm volatile("nop");
				PORTA &=~(1<<1); //WE=0
				asm volatile("nop");
				while(!(PINA&(1<<7))); //loop  until !WAIT
				asm volatile("nop");				
				PORTA |=(1<<1); //WE=1
				asm volatile("nop");
				DDRL = 0x00; //disable output
				break;
			case 0x05: //PING
				tx(rx());
				break;
		}
	}
	return 0;
}
