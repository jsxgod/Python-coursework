#include <stdio.h>
#include <stdlib.h>
#include <time.h>

clock_t start, end;
double cpu_time_used;

typedef struct Node {
  struct Node * next;
  struct Node * prev;
  int value;
} Node;

typedef struct CDLinkedList {
  struct Node * head;
  struct Node * tail;
  int size;
} CDLinkedList;

Node * add(CDLinkedList * list, int value){
  Node* node = (Node *) malloc(sizeof(Node));
  node->value = value;
  if(list->head==NULL && list->tail==NULL){
    printf("Adding first element: %d.\n", value);
    node->prev = node;
    node->next = node;
    list->head = node;
    list->tail = node;
    list->size++;
  } else if(list->head == list->tail){
    printf("Adding: %d.\n", value);
    node->prev = list->head;
    node->next = list->tail;
    list->head = node;
    list->tail->prev = list->head;
    list->tail->next = node;
    list->size++;
  } else {
    printf("Adding: %d.\n", value);
    node->prev = list->head;
    node->next = list->tail;
    list->head->next = node;
    list->tail->prev = node;

    list->head = node;
    list->size++;
  }
  return node;
}

void delete(CDLinkedList * list, Node * node){
  if(node == list->tail){
    printf("Deleting Tail element.\n");
    Node * temp = list->tail->next;
    list->head->next = temp;
    free(list->tail);
    list->size--;
    list->tail = temp;
  } else if(node == list->head){
      printf("Deleting Head element.\n");
      Node * temp = list->head->prev;
      temp->next = list->tail;
      free(list->head);
      list->head = temp;
  } else {
    printf("Deleting.\n");
    node->prev->next = node->next;
    node->next->prev = node->prev;
    free(node);
    list->size--;
  }
}

Node * search(CDLinkedList * list, int index){
  printf("Searching on index %d.\n", index);
  if(index == 0){
    return list->tail;
  } else if(index == list->size-1){
      return list->head;
  } else if(index >= list->size){
    printf("Index out of bounds.");
    return NULL;
  } else {
      if(index < list->size/2){
        Node * temp = list->tail;
        int i = 0;
        while(i < index){
          temp = temp->next;
          i++;
        }
        return temp;
      } else {
        Node * temp = list->head;
        int i = list->size-1;
        while(i > index){
          temp = temp->prev;
          i--;
        }
        return temp;
      }
    }
}
Node * quiet_search(CDLinkedList * list, int index){
  if(index == 0){
    return list->tail;
  } else if(index == list->size-1){
      return list->head;
  } else if(index >= list->size){
    return NULL;
  } else {
      if(index < list->size/2){
        Node * temp = list->tail;
        int i = 0;
        while(i < index){
          temp = temp->next;
          i++;
        }
        return temp;
      } else {
        Node * temp = list->head;
        int i = list->size-1;
        while(i > index){
          temp = temp->prev;
          i--;
        }
        return temp;
      }
    }
}

void merge(CDLinkedList * list1, CDLinkedList * list2){
  list1->head->next = list2->tail;
  list1->head = list2->head;
  list2->head->next = list1->tail;
  list1->tail->prev = list2->head;
  list1->size += list2->size;
}

void printValue(Node* node){
  if(node == NULL){
    printf("ERROR: Specified Node is NULL.\n");
  } else {
    printf("Value: %d\n", node->value);
  }
}

double calculateAverage(double array[], int size){
  double average = 0;
  for(int i = 0; i < size; i++){
    average += array[i];
  }

  return average / size;
}

void test1000(CDLinkedList * list){
  for(int i = 0; i < 1000; i++){
    add(list, i);
  }

  printf("------------\n");
  printf("Testing time on static index search. 100 searches.\n");
  int j = 0;
  double times[100];
  while(j < 100){
    start = clock();
    quiet_search(list, 500);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    times[j] = cpu_time_used;
    j++;
  }

  printf("Testing time on random index search. 100 searches.\n");
  int k = 0;
  double times2[100];
  srand(time(NULL));
  while(k < 100){
    int r = rand() % 1000;
    start = clock();
    quiet_search(list, r);
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    times2[k] = cpu_time_used;
    k++;
  }


  printf("Static times average: %f.\n", calculateAverage(times, 100));
  printf("Random times average: %f.\n", calculateAverage(times2, 100));
}

void testLink(CDLinkedList * list){
  for(int i = 0; i < 5; i++){
    add(list, i);
  }

  printf("Tail->value: %d\n", list->tail->value);
  printf("Head->value: %d\n", list->head->value);
  printf("Head->next->value: %d\n", list->head->next->value);
  printf("Tail->prev->value: %d\n", list->tail->prev->value);
}

void testMerge(CDLinkedList * l1, CDLinkedList * l2){
  for(int i = 0; i<10; i++){
    add(l1,i);
    add(l2,i+100);
  }

  merge(l1, l2);

  for(int j = 0; j < l1->size; j++){
    printValue(search(l1, j));
  }
}

int main(){

  CDLinkedList * list = (CDLinkedList *) malloc(sizeof(CDLinkedList));
  CDLinkedList * list1 = (CDLinkedList *) malloc(sizeof(CDLinkedList));
  CDLinkedList * list2 = (CDLinkedList *) malloc(sizeof(CDLinkedList));

  test1000(list);
  //testLink(list);
  //testMerge(list1, list2);

  return 0;
}
