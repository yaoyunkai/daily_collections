#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int* data;      // 指向数组元素的指针
    int size;       // 数组的当前大小
    int capacity;   // 数组的容量
} DynamicArray;

// 初始化可变长数组
void initArray(DynamicArray* array, int initialCapacity) {
    array->data = (int*)malloc(initialCapacity * sizeof(int));
    array->size = 0;
    array->capacity = initialCapacity;
}

// 在数组末尾插入元素
void append(DynamicArray* array, int element) {
    if (array->size == array->capacity) {
        // 数组已满，需要扩容
        array->capacity *= 2;
        array->data = (int*)realloc(array->data, array->capacity * sizeof(int));
    }

    array->data[array->size++] = element;
}

// 访问数组元素
int get(DynamicArray* array, int index) {
    if (index >= 0 && index < array->size) {
        return array->data[index];
    } else {
        printf("索引越界\n");
        exit(1);
    }
}

// 删除数组中的元素
void removeElement(DynamicArray* array, int index) {
    if (index >= 0 && index < array->size) {
        // 将后面的元素往前移动
        for (int i = index; i < array->size - 1; i++) {
            array->data[i] = array->data[i + 1];
        }

        array->size--;

        // 如果数组过大且使用率低于一定阈值，缩小容量
        if (array->size <= array->capacity / 4) {
            array->capacity /= 2;
            array->data = (int*)realloc(array->data, array->capacity * sizeof(int));
        }
    } else {
        printf("索引越界\n");
        exit(1);
    }
}

// 释放数组内存
void freeArray(DynamicArray* array) {
    free(array->data);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
}

int main() {
    DynamicArray array;
    initArray(&array, 5);

    append(&array, 10);
    append(&array, 20);
    append(&array, 30);

    printf("数组元素为：");
    for (int i = 0; i < array.size; i++) {
        printf("%d ", get(&array, i));
    }
    printf("\n");

    removeElement(&array, 1);

    printf("删除元素后的数组：");
    for (int i = 0; i < array.size; i++) {
        printf("%d ", get(&array, i));
    }
    printf("\n");

    freeArray(&array);

    return 0;
}
