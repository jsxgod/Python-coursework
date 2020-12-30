#include <stdio.h>
#include <stdlib.h>
#include <time.h>

clock_t start, end;
double cpu_time_used;

typedef struct Node {
  struct Node * next;
  int value;
} Node;

typedef struct LinkedList {
  struct Node * head;
  struct Node * tail;
  int size;
} LinkedList;

Node * add(LinkedList * list, int value){

  Node* node = (Node *) malloc(sizeof(Node));
  node->next = NULL;
  node->value = value;
  if(list->head==NULL && list->tail==NULL){
    printf("Adding first element.\n");
    list->head = node;
    list->tail = node;
    list->size++;
  } else {
    printf("Adding: %d.\n", value);
    list->head->next = node;
    list->head = node;
    list->size++;
  }
  return node;
}

void delete(LinkedList * list, Node * node){
  if(node == list->tail){
    printf("Deleting Tail element.\n");
    Node * temp = list->tail->next;
    free(list->tail);
    list->size--;
    list->tail = temp;
  } else if(node == list->head){
      printf("Deleting Head element.\n");
      Node * temp = list->tail;
      while(temp->next != list->head){
        temp = temp->next;
      }
      free(list->head);
      list->head = temp;
  } else {
    printf("Deleting.\n");
    Node * temp = list->tail;
    while(temp->next != node){
      temp = temp->next;
    }
    temp->next = node->next;
    free(node);
    list->size--;
  }
}

void merge(LinkedList * list1, LinkedList * list2){
  list1->head->next = list2->tail;
  list1->head = list2->head;

  list1->size += list2->size;
}

Node * search(LinkedList * list, int index){
  printf("Searching on index %d.\n", index);
  if(index == 0){
    return list->tail;
  } else if(index == list->size-1){
      return list->head;
  } else if(index >= list->size){
    printf("Index out of bounds.");
    return NULL;
  } else {
      Node * temp = list->tail;
      int i = 0;
      while(i < index){
        temp = temp->next;
        i++;
      }
      return temp;
    }
}

Node * quiet_search(LinkedList * list, int index){
  if(index == 0){
    return list->tail;
  } else if(index == list->size-1){
      return list->head;
  } else if(index >= list->size){
    printf("Index out of bounds.");
    return NULL;
  } else {
      Node * temp = list->tail;
      int i = 0;
      while(i < index){
        temp = temp->next;
        i++;
      }
      return temp;
    }
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


void test(LinkedList * list){

  Node * first  =   add(list,1);
  Node * second =   add(list,2);
  Node * last   =   add(list,3);
  //delete(list,first);
  //delete(list,second);
  //delete(list, last);
  printf("%d\n", list->tail->value);
  printf("%d\n", list->tail->next->value);
  printf("%d\n", list->head->value);
  printf("s1: %d\n", search(list,0)->value);
  printf("s2: %d\n", search(list,1)->value);
  printf("s3: %d\n", search(list,2)->value);
}

void test1000(LinkedList * list){
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

void testMerge(LinkedList * l1, LinkedList * l2){
  for(int i = 0; i<10; i++){
    add(l1,i);
    add(l2,i+100);
  }

  merge(l1,l2);

  printValue(search(l1,0));
  printValue(search(l1,9));
  printValue(search(l1,10));
  printValue(search(l1,19));

}

int main(){
  LinkedList * list = (LinkedList *) malloc(sizeof(LinkedList));

  LinkedList * list1 = (LinkedList *) malloc(sizeof(LinkedList));
  LinkedList * list2 = (LinkedList *) malloc(sizeof(LinkedList));

  //test(list);
  test1000(list);
  //testMerge(list1, list2);

  return 0;
}
