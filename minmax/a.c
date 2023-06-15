#include <pthread.h>
#include <stdio.h>

void *thread_function(void *arg) {
  printf("Hello from the new thread!\n");
  return NULL;
}

int main() {
  pthread_t thread;
  int result = pthread_create(&thread, NULL, thread_function, NULL);
  if (result != 0) {
    printf("Error creating thread\n");
    return 1;
  }

  printf("Hello from the main thread!\n");
  pthread_join(thread, NULL);

  return 0;
}
