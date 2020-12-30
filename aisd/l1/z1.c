#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
  struct Node * next;
  int value;
} Node;

typedef struct Queue {
  struct Node * head;
  struct Node * tail;
  int size;
} Queue;

void enqueue(int value, Queue * q){

  Node* node = (Node *) malloc(sizeof(Node));
  node->next = NULL;
  node->value = value;
  if(q->head==NULL && q->tail==NULL){
    printf("First Enqueue\n");
    q->head = node;
    q->tail = node;
  } else {
    printf("Enqueueing\n");
    node->next = q->tail;
    q->tail = node;
  }
}

void dequeue(Queue * q){
  if(q->head==NULL && q->tail == NULL){
    printf("ERROR: EMPTY QUEUE\n");
  } else if(q->tail == q->head){
    printf("Dequeueing the last element in the queue.\n");
    q->head = NULL;
    q->tail = NULL;
  } else {
    printf("Dequeueing.\n");

    Node * temp = q->tail;
    while(temp->next != q->head){
      temp = temp->next;
    }
    q->head = NULL;
    q->head = temp;
  }
}

void test(Queue * q){

  dequeue(q);
  enqueue(1,q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  enqueue(2,q);
  enqueue(3,q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  dequeue(q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  enqueue(4,q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  dequeue(q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  dequeue(q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  dequeue(q);
  dequeue(q);
  enqueue(5,q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  enqueue(6,q);
    printf("Head Node's Value: %d\n", q->head->value);
    printf("Tail Node's Value: %d\n", q->tail->value);
  dequeue(q);
  dequeue(q);
}

int main(){

  Queue* q = (Queue *) malloc(sizeof(Queue));
  test(q);

  return 0;
}
