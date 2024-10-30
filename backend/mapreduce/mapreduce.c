/**
 * mapreduce
 * CS 341 - Fall 2024
 */
#include "core/utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
int main(int argc, char **argv) {
    //init args
    if(argc == 0){
    	print_usage();
	return 0;
    };//to get rid of the warning
    char * out = argv[2];
    char * map = argv[3];
    char * red = argv[4];
    int num = atoi(argv[5]) * 2;

    //printf("inp: %s, out: %s, map: %s, red: %s, num: %d\n", inp, out, map, red, num);
    // Create an input pipe for each mapper.
    int mapperPipe[num];
    for(int i = 0; i < num; i+=2){
    	pipe(mapperPipe + i);
    }
    // Create one input pipe for the reducer.
    int reducerPipe[2];
    pipe(reducerPipe);
    // Open the output file.
    FILE *outFile = fopen(out, "w");
    if(outFile == NULL){
    	exit(1);
    }
    // Start a splitter process for each mapper.
    pid_t spid[num/2];
    for(int i = 0; i < num; i+=2){
    	pid_t f = fork();
	spid[i/2] = f;
	if(f == -1){
	    exit(1);
	}else if(f == 0){
	    //exec splitter
	    close(mapperPipe[i]);
	    dup2(mapperPipe[i+1], STDOUT_FILENO);
	    char ns[16];
	    //sprintf(n, "%d", num / 2);
	    sprintf(ns, "%d", i/2);
	    if(execl("./splitter", "./splitter", argv[1], argv[5], ns, (char *)NULL) == -1){
	    	perror("execl failed for splitter");
    		exit(1);
	    };
	}else{
	    //do nothing?
	}
    }
    // Start all the mapper processes.
    pid_t mpid[num/2];
    for(int i = 1; i <= num; i+=2){
	close(mapperPipe[i]);
	pid_t f = fork();
	int b = i/2;
	mpid[b] = f;
	if(f == -1){
	    exit(1);
	}else if(f==0){
	    //exec mapper
	    close(reducerPipe[0]);
	    dup2(mapperPipe[i-1], 0);
	    dup2(reducerPipe[1], 1);
	    if (execl(map, map, (char *)NULL) == -1) {
    		perror("execl failed for mapper");
    		exit(1);
	    }
	}else{
	    //parent does nothing?
	}
    }
    for (int i = 0; i < num; i += 2) {
        close(mapperPipe[i + 1]);
    }
    close(reducerPipe[1]);
    // Start the reducer process.
    int f = fork();
    int s;
    if(f == -1){
    	exit(1);
    }else if (f == 0){
    	//exec something 
	dup2(reducerPipe[0], STDIN_FILENO);
	int outNo = fileno(outFile);
	dup2(outNo, STDOUT_FILENO);
	if(execl(red, red, (char*) NULL) == -1){
	    perror("execl failed for reducer");
	    exit(1);
        }
    }else{
    // Wait for the reducer to finish.
    // copied from shell mp
    }
    //printf("problem\n");
    for(int i = 0; i < num/2; i++){
        //printf("problem: %d\n", i);
	waitpid(spid[i], &s, 0);
	//printf("problem: %d\n", i);
	waitpid(mpid[i], &s, 0);
    }
    waitpid(f, &s, 0);
    // Count the number of lines in the output file.
    print_num_lines(out);
    close(reducerPipe[0]);
    fclose(outFile);
    return 0;
}
