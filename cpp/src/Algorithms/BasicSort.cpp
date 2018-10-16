#include "../../include/Algorithms/sort.h"

void BasicSort::BubbleSort(int array[], int length) {
    for (int i = 0; i < length; i++) {
        for (int j = i; j < length; j++) {
            if (array[i] > array[j]) {
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
}

void BasicSort::InsertionSort(int array[], int length) {
    int index, value;
    for (int i = 1; i < length; i++) {
        value = array[i];
        index = i - 1;
        while (index > -1 && array[index] > value) {
            array[index + 1] = array[index];
            index = index - 1;
        }
        array[index + 1] = value;
    }
}
//  [Last modified: 2018 10 11 at 16:11:33 EDT]
