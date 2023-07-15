#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} DynamicArray;

void initArray(DynamicArray *arr) {
    arr->data = NULL;
    arr->size = 0;
    arr->capacity = 0;
}

void append(DynamicArray *arr, int element) {
    if (arr->size == arr->capacity) {
        int newCapacity = (arr->capacity == 0) ? 1 : arr->capacity * 2;
        int *newData = (int*)realloc(arr->data, newCapacity * sizeof(int));

        if (newData == NULL) {
            printf("内存分配失败\n");
            return;
        }

        arr->data = newData;
        arr->capacity = newCapacity;
    }

    arr->data[arr->size] = element;
    arr->size++;
}

int get(DynamicArray *arr, int index) {
    if (index < 0 || index >= arr->size) {
        printf("索引越界\n");
        return -1;
    }

    return arr->data[index];
}

void removeItem(DynamicArray *arr, int index) {
    if (index < 0 || index >= arr->size) {
        printf("索引越界\n");
        return;
    }

    for (int i = index; i < arr->size - 1; i++) {
        arr->data[i] = arr->data[i + 1];
    }

    arr->size--;

    // 如果数组的大小变得很小，则缩小容量以节省内存
    if (arr->size > 0 && arr->size == arr->capacity / 4) {
        int newCapacity = arr->capacity / 2;
        int *newData = (int*)realloc(arr->data, newCapacity * sizeof(int));

        if (newData != NULL) {
            arr->data = newData;
            arr->capacity = newCapacity;
        }
    }
}

void freeArray(DynamicArray *arr) {
    free(arr->data);
    arr->data = NULL;
    arr->size = 0;
    arr->capacity = 0;
}

int main() {
    DynamicArray arr;
    initArray(&arr);

    append(&arr, 10);
    append(&arr, 20);
    append(&arr, 30);

    printf("数组元素为：");
    for (int i = 0; i < arr.size; i++) {
        printf("%d ", get(&arr, i));
    }

    printf("\n");

    removeItem(&arr, 1);

    printf("移除后的数组元素为：");
    for (int i = 0; i < arr.size; i++) {
        printf("%d ", get(&arr, i));
    }

    freeArray(&arr);

    return 0;
}
