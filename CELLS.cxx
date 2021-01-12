#include <iostream>  
#include <string>  
#include <ctime>
#include <stdlib.h>
#include <cstdlib>
#include <SDL2/SDL.h>

using namespace std; 
const int code_size=8;
const int size=20;
const int sun=900;
const int commands_count=8;
int mod(int x,int N){
    return (x % N + N) %N;
}
class Point
{
    
    public:
        Point()
            {
            }
        Point(int newX, int newY,  int types)
            {
                this->x=newX;
                this->x=newY;
                this->type=types;
            }
         void setPos(int newX,int newY)
             {
                this->x=newX;
                this->y=newY;
             }
         void setCode(int newCode[code_size])
         {
             for( int i=0; i<code_size+1; i++)
                 {
                     this->code[i]=newCode[i];
                 }
         }
         int getX()
             {
                return x;
             }
         int getY()
             {
                 return y;
             }
         // Метод деления клетки
         void Divide(Point world[size][size])
             {
                 // У рождаемой клетки будет половина энергии родителя
                 int babyEnergy=energy/2;
                 
                 int plusX,plusY;
                 // Тут циклично выборка места рождения с помощью рандома
                 tuda:
                 plusX=-1+(rand()%3);
                 plusY=-1+(rand()%3);
                 if(plusX==0 and plusY==0)
                 {
                     goto tuda;
                     // Если получаемые значения - нули переходим tuda :D
                 }                                 
                 // Новый код это копия кода родителя
                 int newCode[code_size];
                 for(int i=0;i<code_size;i++)
                     {
                             newCode[i]=code[i];
                     }
                 // Мутация с шансом 20% в коде
                if(rand()%6==5)
                {
                     newCode[rand()%(code_size+1)]=rand()%commands_count;
                 }
                 // Устанавливаем все параметры клетки
                 
                 Point *place=&world[(mod(x+plusX,size+1))][mod((y+plusY),(size+1))];
                 if((*place).type==0)
                 {
                 this->energy/=2;
                 (*place).type=type;
                 (*place).setCode(newCode);
                 (*place).energy=babyEnergy;
                 }
                 
             }
        void setCounter(int newCounter)
        {
            this->counter=newCounter;
        }
        int cycle(Point world[size][size])
        {
            
            int i=code[counter];
            this->energy-=10;
            if(energy<200)
            {
                world[x][y].type=0;
                world[x][y].energy=0;
                world[x][y].counter=0;
            }
            if(energy>1000)
            {
                Divide(world);
            }
            if(i==0)
            {
               
                this->counter=mod(counter+1,code_size);
                this->energy+=sun/size*(size-y);
                return 1;
            }
            if(i<9 and i>0)
            {
                // Передвижение по поверхности тора
                int moves[8][2]={{-1,-1},{-1,0},{-1,1},{0,1},{1,1},{1,0},{1,-1}};
                this->counter=mod(counter+1,code_size);
                int newX=mod((x+moves[i-1][0]),size+1);
                int newY=mod((y+moves[i-1][1]),size+1);
                Point place=world[newX][newY];
                if(place.type==0)
                {
                    place.type=type;
                    place.energy=energy;
                    place.setCounter(counter);
                    place.setCode(code);
                    this->type=0;
                    this->energy=0;
                }
                return 1;
            }
        return 0;
        }
    public:
        int type;
        int energy;
        int code[code_size];
    private:
        int x;
        int y;
        int counter=0;
};
int main()  
{  
srand(time(nullptr));

Point world[size][size];
for(int i=0; i<size; i++){
    for(int j=0; j<size; j++){
        world[i][j].setPos(i,j);
        world[i][j].type=0;
                                       }
                            }
world[0][0].type=1;
world[0][0].energy=250;
int code[code_size];
for(int i=0;i<code_size+1;i++)
{
    code[i]=0;
}
world[0][0].setCode(code);
for(int cycle=0;;cycle++)
{
    system("clear");
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            //cout<<i<<" "<<j<<endl;
            if(world[i][j].type!=0)
            {
            world[i][j].cycle(world);
            }
        }
    }
    for(int i=0;i<size;i++)
    {
        for(int j=0;j<size;j++)
        {
            cout<<world[i][j].type;
        }
        cout<<endl;
    }
}
    
return 0;
}  
