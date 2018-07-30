#include <iostream>
#include "include/sort.h"

int main() {
    std::cout<<"Testing\n";
    int test[10] = {5,1,3,8,2,4,7,10,2};
    MySorting::BubbleSort(test, 10);
    for (int i = 0; i < 10; i++) {
        std::cout<<test[i]<<"\n";
    }
    return 0;
}
