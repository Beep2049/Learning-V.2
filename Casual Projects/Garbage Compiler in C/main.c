#include <stdio.h>
#include <stdlib.h>
#define STACK_MAX 256
#define INIT_GC_THRESHOLD 50 /*This number can be adjusted depending on the need to conserve memory*/


/* The Garbage Compiler*/

/*Creating a compiler that finds and eliminates objects that
are no longer in use/no longer necessary AKA "Garbage"*/

/*Criteria for Garbage:
    1. Any object that can't be referenced by a variable in scope
    2. Any object NOT referenced by another in-use object*/

/*An interpreter with two types of objects: Ints and Pairs(can pairs of anything: ints, strings, pairs)*/
typedef enum{
    OBJ_INT,
    OBJ_PAIR
}ObjectType;


/*We implement the PINT/Pair object with a Tagged Union*/
/*Tagged Union: a data structure that can  hold values that take several different, but fixed types*/
typedef struct sObject{
    ObjectType type;

    unsigned char marked; /*Label for marking objects*/

    struct sObject* next;/*The next object in the list of all objects*/

    union{
        /*OBJ_INT*/
        int value;

        /*OBJ_PAIR*/
        struct {
            struct sObject* head;
            struct sObject* tail;
        };
    };  
}Object;


/*Defining a Virtual Machine(VM). Used to store variables currently in scope*/
typedef struct{
    Object* stack[STACK_MAX];
    int stackSize;

    Object* firstObject; /*The first object in the list of all objects*/

    int numObjects; /*# of objects currently allocated*/

    int maxObjects; /*# of Objects required to trigger the collector*/
}VM;

/* Function for debugging*/

void assert(int condition, const char* message){
    if(!condition){
        printf("%s\n", message);
        exit(1);
    }
}

/*Intializing the VM*/
VM* newVM(){
    VM* vm = malloc(sizeof(VM));
    vm->stackSize = 0;
    vm->firstObject = NULL;
    vm->numObjects = 0;
    vm->maxObjects = INIT_GC_THRESHOLD; /*See comment at the top*/
    return vm;
}

/*Creating a way to manipulate the VM's Stack*/

/*Adding an element to the TOP of the stack*/
void push(VM* vm, Object* value){
    assert(vm->stackSize < STACK_MAX, "Stack Overflow!!");
    vm->stack[vm->stackSize++] = value;
}

/*Removing the top element from the Stack*/
Object* pop(VM* vm){
    assert(vm->stackSize > 0, "Stack Underflow!!");
    return(vm->stack[--vm->stackSize]);
}

/*Creating a function that marks objects*/
void mark(Object* object){

    if(object->marked) return;

    object->marked = 1;

    if(object->type == OBJ_PAIR){
        mark(object->head);
        mark(object->tail);
    }
}

/*Creating a function to mark all the reachable objects in memory*/
void markAll(VM* vm){
    for (int i = 0; i < vm->stackSize; i++){
        mark(vm->stack[i]);
    }
}

/*Creating a function to sweep throught the object list and delete
all the unmarked objects*/

void sweep(VM* vm){
    Object** object = &vm->firstObject;
    while(*object){
        if(!(*object)->marked){
            /*If the object wasn't reached, it is removed from the list
            freeing up memory*/
            Object* unreached = *object;

            *object = unreached->next;
            free(unreached);

            vm->numObjects--;
        }else{
            /*If the object was reached, it is unmarked and the functions moves
            to the next object on the list*/
            (*object)->marked = 0;
            object = &(*object)->next;
        }
    }
}

void gc(VM* vm){
    int numObjects = vm->numObjects;

    markAll(vm);
    sweep(vm);

    vm->maxObjects = vm->numObjects == 0 ? INIT_GC_THRESHOLD : vm->numObjects * 2;

    printf("Collected %d objects, %d remaining objects. \n,", numObjects - vm->numObjects, vm->numObjects);
}

/*Creating the VM's ability to create Objects*/
Object* newObject(VM* vm, ObjectType type){
    if(vm->numObjects == vm->maxObjects) gc(vm);

    /*Create Object*/

    Object* object = malloc(sizeof(Object));
    object->type = type;

    /*Insert the object into the list of allocated objects*/
    object->next = vm->firstObject;
    object->marked = 0;

    vm->firstObject = object;

    vm->numObjects++;

    return object;
}

/*Creating the VM's ability to push each kind of object(int and pairs) onto the stack*/
void pushInt(VM* vm, int intValue){
    Object* object = newObject(vm, OBJ_INT);
    object->value = intValue;
    push(vm, object);
}

Object* pushPair(VM* vm){
    Object* object = newObject(vm, OBJ_PAIR);
    object->head = pop(vm);
    object->tail = pop(vm);
    
    push(vm, object);
    return object;
}

void objectPrint(Object* object){
    switch(object->type){
        case OBJ_INT:
        printf("%d", object->value);
        break;

        case OBJ_PAIR:
        printf("(");
        objectPrint(object->head);
        printf(", ");
        objectPrint(object->tail);
        printf("(");
        break;
    }
}

/*Function to free the VM*/
void freeVM(VM* vm){
    vm->stackSize = 0;
    gc(vm);
    free(vm);
}


/* Test cases */

void test1(){
    printf("Test 1: Objects on the staack are preserved.\n");
    VM* vm = newVM();
    pushInt(vm, 1);
    pushInt(vm, 2);

    gc(vm);
    assert(vm->numObjects == 2, "Should have preserved objects");
    freeVM(vm);
}

void test2(){
    printf("Test 2: Unreache objects are colleced.\n");
    VM* vm = newVM();
    pushInt(vm, 1);
    pushInt(vm, 2);
    pop(vm);
    pop(vm);

    gc(vm);
    assert(vm->numObjects == 0, "Should ahve collected objects.");
    freeVM(vm);
}
void test3(){
    printf("Test 3: Reach nested objects.\n");
    VM* vm = newVM();
    pushInt(vm, 1);
    pushInt(vm, 2);
    pushPair(vm);
    pushInt(vm, 3);
    pushInt(vm, 4);
    pushPair(vm);
    pushPair(vm);

    gc(vm);
    assert(vm->numObjects == 7, "Should have reached objects");
    freeVM(vm);
}

void test4(){
    printf("Test 4: Handle cycles. \n");
    VM* vm = newVM();
    pushInt(vm, 1);
    pushInt(vm, 2);
    Object* a = pushPair(vm);
    pushInt(vm, 3);
    pushInt(vm, 4);
    Object* b = pushPair(vm);

    /*Set up a cycle, and also make 2 and 4 unreachable and collectible*/

    a->tail = b;
    b->tail = a;
    
    gc(vm);
    assert(vm->numObjects == 4, "Should have rcollected objects");
    freeVM(vm);
}

/*The Performance Test*/
void perfTest(){
    printf("Performance Test. \n");
    VM* vm = newVM();
    
    for(int i = 0; i < 1000; i++){
        for(int j = 0; j < 20; j++){
            pushInt(vm, i);
        }

        for(int k = 0; k < 20; k++){
            pop(vm);

        }
    }
    freeVM(vm);
}

/* Main */
int main(int argc, const char * argv[]){
    test1();
    test2();
    test3();
    test4();
    perfTest();

    return 0;
}

